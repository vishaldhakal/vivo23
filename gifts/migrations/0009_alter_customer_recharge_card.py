# Generated by Django 4.1 on 2023-10-04 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0008_remove_mobilephone_phone_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='recharge_card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recharge_card', to='gifts.rechargecard'),
        ),
    ]
