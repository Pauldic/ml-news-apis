# Generated by Django 3.1 on 2021-05-19 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_api', '0001_initial'),
        ('recommended_api', '0004_userpostnews'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users_api.userprofile'),
        ),
        migrations.DeleteModel(
            name='UserPostNews',
        ),
    ]