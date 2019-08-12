# Generated by Django 2.1.5 on 2019-06-23 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20190602_0910'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=20)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_item', models.IntegerField()),
                ('address', models.TextField()),
                ('delivery_time', models.CharField(max_length=20)),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('contact', models.CharField(max_length=10)),
                ('is_delivered', models.BooleanField()),
                ('delivered_time', models.DateTimeField(null=True)),
                ('paid_by', models.CharField(choices=[('CASH', 'CASH'), ('UPI', 'UPI'), ('CARD', 'CARD'), ('OTHERS', 'OTHERS')], max_length=30, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_user', to=settings.AUTH_USER_MODEL)),
                ('delivery_boy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderedProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=10)),
                ('price_per_item', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Product')),
            ],
        ),
    ]
