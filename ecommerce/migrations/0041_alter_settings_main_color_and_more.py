# Generated by Django 5.0.1 on 2024-02-07 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0040_settings_navbar_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='main_color',
            field=models.CharField(default='607D8B', max_length=100),
        ),
        migrations.AlterField(
            model_name='settings',
            name='navbar_color',
            field=models.CharField(default='FFFFFF', max_length=100),
        ),
        migrations.AlterField(
            model_name='settings',
            name='secondary_color',
            field=models.CharField(default='0000FF', max_length=100),
        ),
    ]
