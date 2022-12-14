# Generated by Django 4.0 on 2022-11-28 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_profile_editprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(default='Remote', max_length=150)),
                ('date', models.TextField(default='Remote', max_length=150)),
            ],
        ),
        migrations.RemoveField(
            model_name='studysession',
            name='messagess',
        ),
        migrations.DeleteModel(
            name='DiscussionBoard',
        ),
        migrations.AddField(
            model_name='message',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.studysession'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='home.profile'),
        ),
    ]
