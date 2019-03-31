from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CarOfferViewSet

router = DefaultRouter(trailing_slash=False)
router.register('all', CarOfferViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
