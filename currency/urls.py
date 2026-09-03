from django.urls import include, path
from rest_framework import routers

from currency.views.currency_view_set import CurrencyViewSet
from currency.views.exchange_rate_detail_view_set import ExchangeRateDetailViewSet
from currency.views.exchange_rate_view_set import ExchangeRateViewSet
from currency.views.rate_category_view_set import RateCategoryViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"currencies/currencies", CurrencyViewSet)
router.register(r"currencies/rate-categories", RateCategoryViewSet)
router.register(r"currencies/exchange-rates", ExchangeRateViewSet)
router.register(r"currencies/exchange-rate-details", ExchangeRateDetailViewSet)

urlpatterns = [path("", include(router.urls))]