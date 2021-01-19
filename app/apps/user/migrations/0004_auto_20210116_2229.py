# Generated by Django 3.1.4 on 2021-01-16 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='seller',
        ),
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seller_account', to=settings.AUTH_USER_MODEL),
        ),
    ]
