# Generated by Django 3.1 on 2020-09-05 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scraper',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]