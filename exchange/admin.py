from django.contrib import admin
from .models import Symbol, MarketPrice

# Register your models here.
@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = ("id", "code",)
    search_fields = ("code",)
    ordering = ("code",)

@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ("id", "symbol", "last_price", "updated_at",)
    list_filter = ("symbol",)
    search_fields = ("symbol__code",)
    ordering = ("symbol__code", "-updated_at")

    readonly_fields = ("updated_at",)