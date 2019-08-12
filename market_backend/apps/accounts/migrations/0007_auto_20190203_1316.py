# Generated by Django 2.1.5 on 2019-02-03 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_wholesalerproduct'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='wholesalerproduct',
            name='unit',
            field=models.CharField(choices=[('Kg', 'Kg'), ('g', 'g'), ('No(s)', 'No(s)'), ('l', 'l')], max_length=20),
        ),
    ]