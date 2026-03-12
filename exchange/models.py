from django.db import models

# Create your models here.
class Symbol(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.code


class MarketPrice(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE,
                               related_name='symbol_marketprice')
    last_price = models.DecimalField(max_digits=12, decimal_places=2,
                                     default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("symbol",)

    def __str__(self):
        return f"{self.symbol.code} @ {self.last_price}"