# Generated by Django 5.0.1 on 2024-01-30 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0013_remove_product_category_id_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
