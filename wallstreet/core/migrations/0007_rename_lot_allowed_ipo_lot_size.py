# Generated by Django 4.1.3 on 2023-05-04 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_company_company_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ipo',
            old_name='lot_allowed',
            new_name='lot_size',
        ),
    ]