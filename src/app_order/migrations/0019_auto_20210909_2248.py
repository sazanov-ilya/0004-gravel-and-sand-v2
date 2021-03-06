# Generated by Django 3.2.5 on 2021-09-09 19:48

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app_order', '0018_auto_20210909_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.ForeignKey(db_column='status_id', default=2, on_delete=django.db.models.deletion.PROTECT, to='app_order.orderstatus'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 9, 19, 48, 39, 16815, tzinfo=utc), verbose_name='Дата статуса'),
        ),
    ]
