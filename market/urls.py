"""
URL configuration for market project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from exchange.views import market_prices
from trading.views import me, open_orders, recent_trades, place_order


urlpatterns = [
    path('admin/', admin.site.urls),

    # exchange
    path("api/market/", market_prices),

    # trading
    path("api/me", me),
    path("api/orders", place_order),
    path("api/orders/open", open_orders),
    path("api/trades/recent", recent_trades)

]
