# Generated by Django 3.0.4 on 2020-04-25 02:51

from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20200419_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='picture_location',
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=store.models.get_image_filename, verbose_name='Image')),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='store.Product')),
            ],
        ),
    ]