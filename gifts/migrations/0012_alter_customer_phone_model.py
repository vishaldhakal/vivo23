# Generated by Django 4.1 on 2023-10-05 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0011_offers_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_model',
            field=models.CharField(max_length=400),
        ),
    ]
