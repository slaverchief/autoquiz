# Generated by Django 5.2.2 on 2025-06-09 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
