# Generated by Django 5.0.1 on 2024-01-30 22:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0017_category_product_category_subcategory_delete_subtype_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category_id',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='ecommerce.category'),
        ),
    ]
