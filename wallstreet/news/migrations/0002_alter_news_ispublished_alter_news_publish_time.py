# Generated by Django 4.1.3 on 2023-02-27 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='isPublished',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='news',
            name='publish_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]