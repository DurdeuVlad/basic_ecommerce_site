# Generated by Django 5.0.1 on 2024-02-04 01:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0032_calltoaction_fontawesomeicon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calltoaction',
            old_name='fontAwesomeIcon',
            new_name='fontAwesomeIconClassName',
        ),
    ]
