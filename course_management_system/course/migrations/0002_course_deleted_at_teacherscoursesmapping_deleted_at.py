# Generated by Django 5.0.1 on 2025-03-19 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='deleted_at',
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name='teacherscoursesmapping',
            name='deleted_at',
            field=models.DateTimeField(default=None),
        ),
    ]
