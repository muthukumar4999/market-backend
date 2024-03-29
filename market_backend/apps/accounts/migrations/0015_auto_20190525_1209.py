# Generated by Django 2.1.5 on 2019-05-25 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_consumerproduct_ordercart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumerproduct',
            name='product',
        ),
        migrations.RemoveField(
            model_name='consumerproduct',
            name='wholesaler_product',
        ),
        migrations.RemoveField(
            model_name='ordercart',
            name='consumer',
        ),
        migrations.RemoveField(
            model_name='ordercart',
            name='consumer_product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sub_category',
        ),
        migrations.RemoveField(
            model_name='wholesalerproduct',
            name='product',
        ),
        migrations.RemoveField(
            model_name='wholesalerproduct',
            name='sub_category',
        ),
        migrations.RemoveField(
            model_name='wholesalerproduct',
            name='wholesaler',
        ),
        migrations.AddField(
            model_name='subcategory',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Media'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='is_color_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='is_picture_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='is_type_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='unit',
            field=models.CharField(choices=[('Kg', 'Kg'), ('g', 'g'), ('No(s)', 'No(s)'), ('l', 'l')], default='No(s)', max_length=20),
        ),
        migrations.DeleteModel(
            name='ConsumerProduct',
        ),
        migrations.DeleteModel(
            name='OrderCart',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='WholesalerProduct',
        ),
    ]
