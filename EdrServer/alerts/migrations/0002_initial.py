# Generated by Django 5.0.6 on 2024-07-05 01:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alerts', '0001_initial'),
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utils.eventitem'),
        ),
        migrations.AddField(
            model_name='alert',
            name='rule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utils.ruleitem'),
        ),
    ]
