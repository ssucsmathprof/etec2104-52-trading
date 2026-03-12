from django.db import models
from django.conf import settings
from exchange.models import Symbol

# Create your models here.
class Trader(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    cash = models.DecimalField(max_digits=14, decimal_places=2,
                               default=1e6)

    def __str__(self):
        return f"{self.user.username} (${self.cash})"


class Position(models.Model):
    id = models.AutoField(primary_key=True)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE,
                               related_name='trader_position')
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE,
                        related_name='symbol_position')
    shares = models.IntegerField(default=0)

    class Meta:
        unique_together = ("trader", "symbol",)

    def __str__(self):
        return f"{self.trader.user.username} {self.symbol.code}: {self.shares}"


class Order(models.Model):
    SIDE_BUY = "BUY"
    SIDE_SELL = "SELL"
    SIDES = [(SIDE_BUY, "Buy"), (SIDE_SELL, "Sell")]

    id = models.AutoField(primary_key=True)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE,
                               related_name="trader_order")
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE,
                               related_name="symbol_order")
    side = models.CharField(max_length=4, choices=SIDES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.IntegerField()
    remaining = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trader.user.username} {self.side} " \
               f"{self.symbol.code} {self.quantity}@{self.price}"


class Trade(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE,
                               related_name="symbol_trade")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.IntegerField()
    buyer = models.ForeignKey(Trader, on_delete=models.CASCADE,
                              related_name='buyer_trade')
    seller = models.ForeignKey(Trader, on_delete=models.CASCADE,
                              related_name='seller_trade')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trade {self.symbol.code} Buyer:{self.buyer.user.username} " \
               f"Seller:{self.seller.user.username} {self.quantity}@{self.price}"
