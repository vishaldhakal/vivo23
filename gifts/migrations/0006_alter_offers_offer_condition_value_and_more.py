# Generated by Django 4.1 on 2023-09-30 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0005_rechargecardoffer_offers_phone_price_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offers',
            name='offer_condition_value',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='rechargecardoffer',
            name='offer_condition_value',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
