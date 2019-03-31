from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CarOfferViewSet,
    CarViewSet,
    ColorViewSet,
    CarCategoryViewSet,
    CarModelViewSet,
    CarBrandViewSet,
)

router = DefaultRouter(trailing_slash=False)
router.register('caroffers', CarOfferViewSet)
router.register('cars', CarViewSet)
router.register('colors', ColorViewSet)
router.register('car-categories', CarCategoryViewSet)
router.register('models', CarModelViewSet)
router.register('brands', CarBrandViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
