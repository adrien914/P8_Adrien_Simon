# Generated by Django 3.1.2 on 2020-10-23 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_substitute_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='aliment',
            name='url',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='substitute',
            name='url',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
