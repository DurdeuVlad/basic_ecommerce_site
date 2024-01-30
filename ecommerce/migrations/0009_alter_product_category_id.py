# Generated by Django 5.0.1 on 2024-01-30 22:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0008_category_remove_product_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='ecommerce.category'),
        ),
    ]
