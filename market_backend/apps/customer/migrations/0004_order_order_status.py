# Generated by Django 2.1.5 on 2019-07-02 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20190625_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('PACKED', 'PACKED'), ('PICKUPED', 'PICKUPED'), ('DELIVERED', 'DELIVERED')], default='PENDING', max_length=30, null=True),
        ),
    ]
