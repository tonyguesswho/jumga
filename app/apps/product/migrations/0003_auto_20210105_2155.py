# Generated by Django 3.1.4 on 2021-01-05 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0003_auto_20210105_2035'),
        ('product', '0002_auto_20210105_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='seller.seller'),
            preserve_default=False,
        ),
    ]
