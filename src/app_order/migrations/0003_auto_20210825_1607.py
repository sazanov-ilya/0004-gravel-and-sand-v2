# Generated by Django 3.2.5 on 2021-08-25 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_order', '0002_alter_orders_order_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='areas',
            options={'ordering': ['area_id', 'area_name'], 'verbose_name': 'Район', 'verbose_name_plural': 'Районы'},
        ),
        migrations.AlterModelOptions(
            name='orders',
            options={'ordering': ['order_id', 'order_name'], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='orderstatus',
            options={'ordering': ['status_id', 'status_name'], 'verbose_name': 'Статус заказа', 'verbose_name_plural': 'Статусы заказов'},
        ),
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ['product_id', 'product_name'], 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='area_id',
            new_name='area',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='status_id',
            new_name='status',
        ),
        migrations.AlterField(
            model_name='areas',
            name='area_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='status_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
