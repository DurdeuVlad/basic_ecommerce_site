# Generated by Django 5.0.1 on 2024-01-30 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_product_category_product_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='additional_info',
            field=models.CharField(default='', max_length=600),
        ),
        migrations.AlterField(
            model_name='product',
            name='desc',
            field=models.CharField(default='', max_length=100),
        ),
    ]