# Generated by Django 3.1.4 on 2021-01-05 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_auto_20210104_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='currency',
            field=models.CharField(default='USD', max_length=3, verbose_name='currency'),
        ),
    ]
