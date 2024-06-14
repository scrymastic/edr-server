# Generated by Django 5.0.6 on 2024-06-05 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('title', models.CharField(blank=True, default='', max_length=200)),
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('related', models.JSONField(blank=True, default=list)),
                ('status', models.CharField(blank=True, default='', max_length=200)),
                ('description', models.TextField(blank=True, default='')),
                ('references', models.JSONField(blank=True, default=list)),
                ('author', models.CharField(blank=True, default='', max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('tags', models.JSONField(blank=True, default=list)),
                ('logsource', models.JSONField(blank=True, default=dict)),
                ('detection', models.JSONField(blank=True, default=dict)),
                ('falsepositives', models.JSONField(blank=True, default=list)),
                ('level', models.CharField(blank=True, default='', max_length=200)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]