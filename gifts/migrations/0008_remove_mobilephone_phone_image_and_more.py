# Generated by Django 4.1 on 2023-10-04 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0007_remove_rechargecardoffer_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobilephone',
            name='phone_image',
        ),
        migrations.RemoveField(
            model_name='mobilephone',
            name='phone_price',
        ),
        migrations.RemoveField(
            model_name='offers',
            name='phone_price_type',
        ),
        migrations.AddField(
            model_name='customer',
            name='amount_of_card',
            field=models.IntegerField(default=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='ntc_recharge_card',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='profession',
            field=models.CharField(default='None', max_length=400),
        ),
    ]