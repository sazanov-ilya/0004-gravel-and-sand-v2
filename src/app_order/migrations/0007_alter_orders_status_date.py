# Generated by Django 3.2.5 on 2021-08-27 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_order', '0006_orders_status_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='status_date',
            field=models.DateTimeField(verbose_name='Дата статуса'),
        ),
    ]
