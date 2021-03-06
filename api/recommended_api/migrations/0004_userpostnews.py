# Generated by Django 3.1 on 2021-05-19 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_api', '0001_initial'),
        ('recommended_api', '0003_auto_20210516_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPostNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommended_api.news')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_api.userprofile')),
            ],
            options={
                'db_table': 'userpost_news',
                'ordering': ['-id'],
            },
        ),
    ]
