# Generated by Django 2.1.7 on 2019-03-30 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otomoto', '0002_auto_20190330_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='caroffer',
            name='horsepower',
            field=models.PositiveIntegerField(default=100),
        ),
        migrations.AddField(
            model_name='caroffer',
            name='isnew',
            field=models.BooleanField(default=True),
        ),
    ]
