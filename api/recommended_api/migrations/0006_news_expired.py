# Generated by Django 3.1 on 2021-05-24 01:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recommended_api', '0005_auto_20210519_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='expired',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
