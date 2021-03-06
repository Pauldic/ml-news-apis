# Generated by Django 3.1 on 2021-04-20 01:15

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=500)),
                ('source', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=100, null=True)),
                ('title', models.CharField(max_length=500)),
                ('small_description', models.TextField(null=True)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=500)),
                ('url', models.CharField(max_length=500)),
                ('urltoimage', models.CharField(max_length=500, null=True)),
                ('publishedat', models.DateTimeField(auto_now_add=True)),
                ('updatedat', models.DateTimeField(auto_now_add=True)),
                ('entities', models.JSONField(blank=True, default=dict)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ('liked', models.PositiveIntegerField(default=0)),
                ('unliked', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'news',
            },
        ),
    ]
