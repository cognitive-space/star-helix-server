# Generated by Django 4.0.1 on 2022-01-04 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stash', '0005_remove_log_logfile_logchunk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='process',
        ),
    ]
