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

from .serializers import (
    CarOfferSerializer, 
    CarSerializer,
    ColorSerializer,
    CarCategorySerializer,
    CarModelSerializer,
    CarBrandSerializer
)


class CarOfferViewSet(viewsets.ModelViewSet):

    queryset = CarOffer.objects.all()
    serializer_class = CarOfferSerializer

    filter_fields = (
        'car__brand__name',
        'car__model__name',
        'car__category__name',
        'color__name',
        'price',
        'year',
        'mileage',
        'horsepower',
        'isnew',
    )

    search_fields = (
        'car__brand__name',
        'car__model__name',
        'car__category__name',
    )


class CarViewSet(viewsets.ModelViewSet):

    queryset = Car.objects.all()
    serializer_class = CarSerializer

    filter_fields = (
        'brand__name',
        'model__name',
        'category__name'
        
    )

    search_fields = (
        'brand__name',
        'model__name',
        'category__name'
    )

class ColorViewSet(viewsets.ModelViewSet):

    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class CarCategoryViewSet(viewsets.ModelViewSet):

    queryset = CarCategory.objects.all()
    serializer_class = CarCategorySerializer

class CarModelViewSet(viewsets.ModelViewSet):

    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer

class CarBrandViewSet(viewsets.ModelViewSet):

    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer





