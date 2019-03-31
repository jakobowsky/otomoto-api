from django.db import models


class CarBrand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CarCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Car(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    category = models.ForeignKey(CarCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.brand.name} {self.model.name}'


class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CarOffer(models.Model):
    otomoto_id = models.CharField(unique=True, max_length=30)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    link = models.CharField(max_length=150)
    photo = models.CharField(max_length=300)
    year = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    mileage = models.PositiveIntegerField(default=0)
    horsepower = models.PositiveIntegerField(default=100)
    isnew = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.otomoto_id} {self.car.brand.name} {self.car.model.name}'
