from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from exchange.models import Symbol
from .models import Trader, Order, Trade, Position
from .serializers import (
    TraderSerializer, OrderSerializer, TradeSerializer, PlaceOrderSerializer
)
from .matching import match_symbol

def get_trader(user):
    return Trader.objects.get(user=user)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    trader = get_trader(request.user)
    trader = Trader.objects.prefetch_related("positions__symbol").get(id=trader.id)
    return Response(TraderSerializer(trader).data)

@api_view(["POST"])
#@permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def place_order(request):
    serializer = PlaceOrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    symbol_code = serializer.validated_data["symbol"].upper()
    side = serializer.validated_data["side"]
    price = serializer.validated_data["price"]
    quantity = serializer.validated_data["quantity"]

    symbol = Symbol.objects.get(code=symbol_code)
    trader = get_trader(request.user)

    # basic checks: no short selling
    if side == "SELL":
        #pos = Position.objects.get(trader=trader, symbol=symbol, side=side)
        pos = trader.trader_position.get(symbol=symbol) if trader.trader_position.filter(symbol=symbol).exists() else None
        shares = pos.shares if pos else 0
        #if shares < quantity:
        #    return Response({"error": "Not enough shares to sell."}, status=status.HTTP_400_BAD_REQUEST)

    order = Order.objects.create(
        trader=trader,
        symbol=symbol,
        side=side,
        price=price,
        quantity=quantity,
        remaining=quantity,
    )

    # run matching for that symbol
    match_symbol(symbol_code)

    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
#@permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def open_orders(request):
    trader = get_trader(request.user)
    qs = Order.objects.filter(trader=trader, remaining__gt=0).select_related("symbol").order_by("-created_at")
    return Response(OrderSerializer(qs, many=True).data)

@api_view(["GET"])
#@permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def recent_trades(request):
    qs = Trade.objects.select_related("symbol", "buyer__user", "seller__user").order_by("-created_at")[:50]
    return Response(TradeSerializer(qs, many=True).data)

