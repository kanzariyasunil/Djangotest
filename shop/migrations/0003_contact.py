# Generated by Django 5.1.1 on 2024-10-07 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_category_product_image_product_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('Email', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(default='', max_length=50)),
                ('desc', models.CharField(max_length=100)),
            ],
        ),
    ]