# Generated by Django 4.0 on 2022-10-25 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_class_class_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='classes',
            field=models.ManyToManyField(blank=True, to='home.Class'),
        ),
    ]