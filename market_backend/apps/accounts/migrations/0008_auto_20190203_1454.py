# Generated by Django 2.1.5 on 2019-02-03 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20190203_1316'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wholesalerproduct',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='category',
            name='image_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
