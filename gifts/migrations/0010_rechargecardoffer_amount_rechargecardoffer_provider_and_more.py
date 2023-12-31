# Generated by Django 4.1 on 2023-10-04 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0009_alter_customer_recharge_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='rechargecardoffer',
            name='amount',
            field=models.IntegerField(choices=[(50, '50'), (100, '100'), (200, '200'), (500, '500')], default=50),
        ),
        migrations.AddField(
            model_name='rechargecardoffer',
            name='provider',
            field=models.CharField(choices=[('Ncell', 'Ncell'), ('Ntc', 'Ntc'), ('Smart Cell', 'Smart Cell'), ('Others', 'Others')], default='Ncell', max_length=400),
        ),
        migrations.AlterField(
            model_name='rechargecard',
            name='amount',
            field=models.IntegerField(choices=[(50, '50'), (100, '100'), (200, '200'), (500, '500')]),
        ),
    ]
