from rest_framework import serializers


from otomoto.models import (
    Car,
    CarBrand,
    CarCategory,
    CarModel,
    CarOffer,
    Color
)


class CarOfferSerializer(serializers.ModelSerializer):

    car = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    def get_car(self, caroffer):
        return {
            'brand': caroffer.car.brand.name,
            'category': caroffer.car.category.name,
            'model': caroffer.car.model.name,
        }

    def get_color(self, caroffer):
        return {
            'id': caroffer.color_id,
            'name':caroffer.color.name,
        }

    class Meta:
        model = CarOffer
        fields = (
            'id',
            'otomoto_id',
            'link',
            'photo',
            'year',
            'price',
            'color',
            'mileage',
            'horsepower',
            'isnew',
            'car',

        )