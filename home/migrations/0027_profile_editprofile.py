# Generated by Django 4.0.8 on 2022-11-14 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_discussionboard_studysession_messagess'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='editProfile',
            field=models.BooleanField(default=False),
        ),
    ]
