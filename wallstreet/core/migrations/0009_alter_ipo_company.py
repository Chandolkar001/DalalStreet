# Generated by Django 4.1.3 on 2023-05-05 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_company_company_id_alter_ipo_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipo',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.company', to_field='company_id'),
        ),
    ]
