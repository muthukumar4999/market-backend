# Generated by Django 2.1.5 on 2019-07-07 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_auto_20190706_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pickup_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='upi_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]