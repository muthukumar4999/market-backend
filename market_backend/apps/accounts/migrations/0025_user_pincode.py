# Generated by Django 2.1.5 on 2019-07-03 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20190629_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pincode',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
