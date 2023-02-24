# Generated by Django 4.1.3 on 2023-02-12 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_security_iposubscription_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('high_cap', models.IntegerField(default=0)),
                ('low_cap', models.IntegerField(default=0)),
                ('lot_allowed', models.IntegerField(default=0)),
                ('total_volume', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(default=-1)),
                ('no_of_shares', models.IntegerField(default=0)),
                ('cash', models.IntegerField(default=200000)),
                ('net_worth', models.IntegerField(default=0)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('offer_bid', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='user',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='security',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
        migrations.RemoveField(
            model_name='company',
            name='ipo_face_value',
        ),
        migrations.RemoveField(
            model_name='company',
            name='ipo_lot_max_val',
        ),
        migrations.RemoveField(
            model_name='company',
            name='ipo_lot_min_val',
        ),
        migrations.RemoveField(
            model_name='company',
            name='ipo_lot_size',
        ),
        migrations.RemoveField(
            model_name='company',
            name='listing_price',
        ),
        migrations.RemoveField(
            model_name='company',
            name='share_price',
        ),
        migrations.DeleteModel(
            name='IPOSubscription',
        ),
        migrations.DeleteModel(
            name='Portfolio',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
        migrations.AddField(
            model_name='subscription',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.company'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ipo',
            name='company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.company'),
        ),
        migrations.AddField(
            model_name='ipo',
            name='subscribers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
