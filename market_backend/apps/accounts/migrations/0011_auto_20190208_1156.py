# Generated by Django 2.1.5 on 2019-02-08 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20190208_1117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wholesalerproduct',
            name='category',
        ),
        migrations.AddField(
            model_name='wholesalerproduct',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.SubCategory'),
        ),
    ]
