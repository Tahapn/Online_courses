# Generated by Django 5.0.3 on 2024-04-05 08:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_coursefiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1000)]),
        ),
    ]
