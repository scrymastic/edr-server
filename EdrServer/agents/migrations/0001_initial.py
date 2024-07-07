# Generated by Django 5.0.6 on 2024-07-05 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('ip', models.GenericIPAddressField(primary_key=True, serialize=False)),
                ('hostname', models.CharField(max_length=50)),
                ('os', models.CharField(max_length=50)),
                ('version', models.CharField(max_length=50)),
                ('mac', models.CharField(max_length=50)),
                ('last_seen', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]