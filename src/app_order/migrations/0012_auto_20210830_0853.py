# Generated by Django 3.2.5 on 2021-08-30 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_order', '0011_auto_20210830_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areas',
            name='area_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='Стоимость доставки'),
        ),
        migrations.AlterField(
            model_name='areas',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='products',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='Slug'),
        ),
    ]
