# Generated by Django 5.0.1 on 2024-02-03 23:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0029_remove_settings_stripe_live_public_key_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='facebook_link',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='instagram_link',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='twitter_link',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='youtube_link',
        ),
        migrations.CreateModel(
            name='SocialMediaLinks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('link', models.CharField(default='https://www.facebook.com/', max_length=100)),
                ('icon', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('instagram', 'Instagram'), ('youtube', 'Youtube'), ('tiktok', 'Tiktok'), ('linkedin', 'Linkedin'), ('pinterest', 'Pinterest'), ('snapchat', 'Snapchat'), ('reddit', 'Reddit'), ('tumblr', 'Tumblr'), ('whatsapp', 'Whatsapp'), ('telegram', 'Telegram'), ('discord', 'Discord'), ('skype', 'Skype')], default='facebook', max_length=50)),
                ('putInHeader', models.BooleanField(default=False)),
                ('putInFooter', models.BooleanField(default=True)),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.settings')),
            ],
        ),
    ]
