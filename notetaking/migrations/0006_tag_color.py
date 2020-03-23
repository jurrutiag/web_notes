# Generated by Django 3.0.4 on 2020-03-20 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notetaking', '0005_note_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='color',
            field=models.ForeignKey(default='Gray', on_delete=django.db.models.deletion.CASCADE, to='notetaking.Color'),
        ),
    ]
