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

class CarSerializer(serializers.ModelSerializer):

    car = serializers.SerializerMethodField()

    def get_car(self, car):
        return {
            'brand': car.brand.name,
            'category': car.category.name,
            'model': car.model.name,
        }

    class Meta:
        model = Car
        fields = (
            'id',
            'car',
        )

class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = (
            'id',
            'name',
        )

class CarCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CarCategory
        fields = (
            'id',
            'name',
        )

class CarModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModel
        fields = (
            'id',
            'name',
        )

class CarBrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarBrand
        fields = (
            'id',
            'name',
        )