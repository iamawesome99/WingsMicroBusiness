# Generated by Django 3.0.4 on 2020-04-01 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='base_price',
            field=models.IntegerField(default=0),
        ),
    ]
