# Generated by Django 4.0 on 2022-10-24 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_class_students_profile_classes'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='class_name',
            field=models.CharField(default='N/A', max_length=150),
            preserve_default=False,
        ),
    ]