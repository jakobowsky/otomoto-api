from django.shortcuts import render

from rest_framework import viewsets

from otomoto.models import (
    Car,
    CarBrand,
    CarCategory,
    CarModel,
    CarOffer,
    Color
)

from .serializers import CarOfferSerializer

def home(request):
    return 1


class CarOfferViewSet(viewsets.ModelViewSet):

    queryset = CarOffer.objects.all()
    serializer_class = CarOfferSerializer

    filter_fields = (
        # 'car__brand__name',
        # 'car__brand__model',
        'year',
    )