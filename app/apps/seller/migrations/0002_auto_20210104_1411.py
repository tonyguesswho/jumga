# Generated by Django 3.1.4 on 2021-01-04 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='country_code',
            field=models.CharField(default='NG', max_length=3, verbose_name='alpha 2 country code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seller',
            name='currency',
            field=models.CharField(default='usd', max_length=3, verbose_name='currency'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='is_active',
            field=models.BooleanField(default=False, help_text='Designates whether this seller should be treated asactive.', verbose_name='Active'),
        ),
    ]
