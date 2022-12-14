# Generated by Django 4.0 on 2022-11-07 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_remove_profile_friend'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='friendsList',
            field=models.ManyToManyField(blank=True, to='home.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(blank=True, to='home.Friends'),
        ),
    ]
