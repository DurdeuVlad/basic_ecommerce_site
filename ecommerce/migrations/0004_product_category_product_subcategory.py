# Generated by Django 5.0.1 on 2024-01-30 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_rename_money_earned_product_money_earned_do_not_modify_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.CharField(default='', max_length=50),
        ),
    ]