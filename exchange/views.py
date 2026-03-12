from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from .models import MarketPrice
from .serializers import MarketPriceSerializer

# Create your views here.

@api_view(["GET"])
@permission_classes([AllowAny])
def market_prices(request):
    qs = MarketPrice.objects.select_related("symbol").all().order_by("symbol__code")
    return Response(MarketPriceSerializer(qs, many=True).data)