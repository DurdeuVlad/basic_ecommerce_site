# Generated by Django 5.0.1 on 2024-02-10 19:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0043_settings_checkout_delete_button_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextLanguage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='English', max_length=100)),
                ('checkout_delete_button_text', models.CharField(default='Delete', max_length=100)),
                ('product_last_chance_text', models.CharField(default='Last chance', max_length=100)),
                ('product_best_seller_text', models.CharField(default='Best seller', max_length=100)),
                ('buy_button_text', models.CharField(default='Buy now', max_length=100)),
                ('product_new_text', models.CharField(default='New', max_length=100)),
                ('product_featured_text', models.CharField(default='Featured', max_length=100)),
                ('product_out_of_stock_text', models.CharField(default='Out of stock', max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='settings',
            name='buy_button_text',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='checkout_delete_button_text',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='product_best_seller_text',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='product_featured_text',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='product_last_chance_text',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='product_new_text',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='product_out_of_stock_text',
        ),
        migrations.AddField(
            model_name='settings',
            name='textLanguages',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='ecommerce.textlanguage'),
        ),
    ]
