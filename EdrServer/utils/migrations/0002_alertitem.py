# Generated by Django 5.0.6 on 2024-06-14 04:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0001_initial'),
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertItem',
            fields=[
                ('alert_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='alerts.alert')),
            ],
            bases=('alerts.alert',),
        ),
    ]
