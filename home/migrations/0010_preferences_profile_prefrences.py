# Generated by Django 4.0 on 2022-10-31 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_profile_bio_alter_profile_classes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite_location', models.CharField(max_length=150)),
                ('in_person', models.BooleanField()),
                ('remote', models.BooleanField()),
                ('revision', models.BooleanField()),
                ('cramming', models.BooleanField()),
                ('quizzing', models.BooleanField()),
                ('quiet_study', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='prefrences',
            field=models.ManyToManyField(blank=True, to='home.Preferences'),
        ),
    ]
