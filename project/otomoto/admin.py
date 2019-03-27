from django.contrib import admin

from .models import (
    CarBrand,
    CarCategory,
    CarModel,
    CarOffer,
    Car,
    Color
)

admin.site.register(CarOffer)
admin.site.register(CarBrand)
admin.site.register(CarCategory)
admin.site.register(CarModel)
admin.site.register(Car)
admin.site.register(Color)