# Generated by Django 5.0.1 on 2024-02-10 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0044_textlanguage_remove_settings_buy_button_text_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='settings',
            old_name='textLanguages',
            new_name='textLanguage',
        ),
    ]