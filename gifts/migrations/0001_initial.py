# Generated by Django 4.1 on 2023-09-29 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('image_url', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='IMEINO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imei_no', models.CharField(max_length=400)),
                ('used', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MobilePhone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_model', models.CharField(max_length=400)),
                ('phone_image', models.ImageField(upload_to='')),
                ('phone_price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RechargeCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardno', models.CharField(max_length=400)),
                ('provider', models.CharField(max_length=400)),
                ('amount', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='recharge_card_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_count', models.IntegerField(default=0)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('type_of_offer', models.CharField(choices=[('After every certain sale', 'After every certain sale'), ('At certain sale position', 'At certain sale position')], max_length=800)),
                ('offer_condition_value', models.CharField(max_length=500)),
                ('gift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gifts.gift')),
            ],
            options={
                'ordering': ('start_date',),
            },
        ),
        migrations.CreateModel(
            name='FixOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imei_no', models.CharField(max_length=400)),
                ('quantity', models.IntegerField()),
                ('gift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gifts.gift')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=400)),
                ('shop_name', models.TextField()),
                ('sold_area', models.CharField(max_length=800)),
                ('phone_number', models.CharField(max_length=400)),
                ('sale_status', models.CharField(default='SOLD', max_length=400)),
                ('prize_details', models.CharField(default='Happy Sales Carnival', max_length=900)),
                ('imei', models.CharField(max_length=400)),
                ('date_of_purchase', models.DateField(auto_now_add=True)),
                ('how_know_about_campaign', models.CharField(choices=[('Facebook Ads', 'Facebook Ads'), ('Reatil Shop', 'Reatil Shop'), ('Google Ads', 'Google Ads'), ('Others', 'Others')], max_length=800)),
                ('gift', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gifts.gift')),
                ('phone_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gifts.mobilephone')),
                ('recharge_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gifts.rechargecard')),
            ],
            options={
                'ordering': ('-date_of_purchase',),
            },
        ),
    ]
