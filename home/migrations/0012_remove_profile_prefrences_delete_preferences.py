# Generated by Django 4.0 on 2022-11-02 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_remove_preferences_cramming_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='prefrences',
        ),
        migrations.DeleteModel(
            name='Preferences',
        ),
    ]
