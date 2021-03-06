# Generated by Django 3.1.2 on 2020-10-09 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliment',
            name='nutrition_grades',
            field=models.CharField(blank=True, default=None, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='aliment',
            name='product_name',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='aliment',
            name='stores',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='substitute',
            name='nutrition_grades',
            field=models.CharField(blank=True, default=None, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='substitute',
            name='product_name',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='substitute',
            name='stores',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
    ]
