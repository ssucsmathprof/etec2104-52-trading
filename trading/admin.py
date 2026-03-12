from django.contrib import admin
from .models import Trader, Position, Order, Trade
# Register your models here.
@admin.register(Trader)
class TraderAdmin(admin.ModelAdmin):
    list_display = ("id", "user__username", "cash")

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "trader", "symbol", "shares",)

@admin.register(Order)
class TraderAdmin(admin.ModelAdmin):
    list_display = ("id", "trader", "symbol", "side",
                    "price", "quantity", "remaining",
                    "created_at",)

@admin.register(Trade)
class TraderAdmin(admin.ModelAdmin):
    list_display = ("id", "symbol", "price", "quantity",
                    "buyer", "seller", "created_at")

