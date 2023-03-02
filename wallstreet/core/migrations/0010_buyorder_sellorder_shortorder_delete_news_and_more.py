# Generated by Django 4.1.3 on 2023-03-02 05:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_merge_20230302_1128'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_placed', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('bid_price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SellOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_placed', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('ask_price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ShortOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('time_placed', models.DateTimeField(auto_now_add=True)),
                ('closed_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='News',
        ),
        migrations.DeleteModel(
            name='Security',
        ),
        migrations.AddField(
            model_name='company',
            name='last_traded_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='listing_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='shortorder',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.company'),
        ),
        migrations.AddField(
            model_name='shortorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sellorder',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.company'),
        ),
        migrations.AddField(
            model_name='sellorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='buyorder',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.company'),
        ),
        migrations.AddField(
            model_name='buyorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
