# Generated by Django 5.0.6 on 2024-07-08 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebooks', '0002_notebook_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notebookcell',
            name='content',
            field=models.TextField(blank=True, max_length=2000),
        ),
    ]
