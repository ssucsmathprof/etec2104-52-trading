from rest_framework import serializers
from .models import Symbol, MarketPrice

class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = ["id", "code"]

class MarketPriceSerializer(serializers.ModelSerializer):
    symbol = SymbolSerializer()

    class Meta:
        model = MarketPrice
        fields = ["id", "symbol", "last_price", "updated_at"]

