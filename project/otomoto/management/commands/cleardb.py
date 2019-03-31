from django.core.management import BaseCommand

from otomoto.models import (
    Car,
    CarBrand,
    CarCategory,
    CarModel,
    CarOffer,
    Color
)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        print(CarOffer.objects.all().delete())
        print(Car.objects.all().delete())
        print(CarBrand.objects.all().delete())
        print(CarCategory.objects.all().delete())
        print(CarModel.objects.all().delete())
        print(Color.objects.all().delete())
