# Generated by Django 5.0.1 on 2024-04-27 13:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_listing_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
