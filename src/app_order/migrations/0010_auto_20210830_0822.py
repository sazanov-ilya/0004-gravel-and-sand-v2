# Generated by Django 3.2.5 on 2021-08-30 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_order', '0009_auto_20210829_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderstatus',
            name='slug',
            field=models.SlugField(max_length=200, null=True, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_date_published',
            field=models.DateTimeField(verbose_name='Дата публикации'),
        ),
    ]
