from rest_framework import serializers
from .models import Trader, Position, Order, Trade

class PositionSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(source="symbol.code")

    class Meta:
        model = Position
        fields = ["id", "symbol", "shares"]


class PlaceOrderSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    side = serializers.ChoiceField(choices=["BUY", "SELL"])
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    quantity = serializers.IntegerField(min_value=1)


class TraderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    positions = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = Trader
        fields = ["id", "user", "cash", "positions"]


class OrderSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(source="symbol.code")
    trader = serializers.CharField(source="trader.user.username")

    class Meta:
        model = Order
        fields = ["id", "trader", "symbol", "side",
                  "price", "quantity", "remaining",
                  "created_at"]

class TradeSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(source="symbol.code")
    buyer = serializers.CharField(source="buyer.user.username")
    seller = serializers.CharField(source="seller.user.username")

    class Meta:
        model = Trade
        fields = ["id", "symbol", "price", "quantity",
                  "buyer", "seller", "created_at"]