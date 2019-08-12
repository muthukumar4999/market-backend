# Generated by Django 2.1.5 on 2019-06-25 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20190602_0910'),
        ('customer', '0002_order_orderedproducts'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Media'),
        ),
        migrations.AddField(
            model_name='orderedproducts',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Media'),
        ),
    ]
