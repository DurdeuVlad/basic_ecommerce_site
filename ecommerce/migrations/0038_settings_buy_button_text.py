# Generated by Django 5.0.1 on 2024-02-07 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0037_settings_items_per_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='buy_button_text',
            field=models.CharField(default='Buy now', max_length=100),
        ),
    ]