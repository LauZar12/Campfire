# Generated by Django 5.1.2 on 2024-11-13 01:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='desciption',
            new_name='description',
        ),
    ]
