# Generated by Django 5.0.1 on 2024-01-30 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0005_product_additional_info_alter_product_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_best_seller',
            field=models.BooleanField(default=False),
        ),
    ]
