# Generated by Django 5.0.6 on 2024-06-27 14:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebooks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notebook',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
