# Generated by Django 5.0.1 on 2024-02-07 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0036_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='items_per_page',
            field=models.IntegerField(default=12),
        ),
    ]