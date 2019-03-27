from django.db import models


class CarBrand(models.Model):
    name = models.CharField(max_length=50)

class CarModel(models.Model):
    name = models.CharField(max_length=50)

class CarCategory(models.Model):
    name = models.CharField(max_length=50)

class Car(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    category = models.ForeignKey(CarCategory, on_delete=models.CASCADE)

class CarOffer(models.Model):
    pass
