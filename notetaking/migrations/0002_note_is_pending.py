# Generated by Django 3.0.4 on 2020-03-19 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notetaking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='is_pending',
            field=models.BooleanField(default=True),
        ),
    ]
