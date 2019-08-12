# Generated by Django 2.1.5 on 2019-02-20 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20190209_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumerProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_drafted', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Product')),
                ('wholesaler_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.WholesalerProduct')),
            ],
        ),
        migrations.CreateModel(
            name='OrderCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('consumer_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.ConsumerProduct')),
            ],
        ),
    ]
