# Generated by Django 4.1.3 on 2023-05-05 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_company_company_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_id',
            field=models.CharField(default=101, max_length=255, unique=True),
        ),
    ]
