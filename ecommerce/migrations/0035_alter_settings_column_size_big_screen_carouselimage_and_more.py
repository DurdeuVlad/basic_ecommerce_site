# Generated by Django 5.0.1 on 2024-02-04 18:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0034_settings_column_size_big_screen_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='column_size_big_screen',
            field=models.IntegerField(default=5),
        ),
        migrations.CreateModel(
            name='CarouselImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(default='', upload_to='ecommerce/images')),
                ('order', models.IntegerField(default=0)),
                ('title', models.CharField(default='Title', max_length=100)),
                ('subtitle', models.CharField(default='Subtitle', max_length=100)),
                ('description', models.CharField(default='Description', max_length=100)),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.settings')),
            ],
        ),
        migrations.AddField(
            model_name='calltoaction',
            name='carouselImage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.carouselimage'),
        ),
    ]
