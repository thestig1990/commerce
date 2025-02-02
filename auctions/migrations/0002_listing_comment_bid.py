# Generated by Django 5.0.1 on 2024-04-01 20:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('description', models.TextField()),
                ('starting_bid', models.IntegerField()),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('category', models.CharField(blank=True, choices=[('DR', 'Drones'), ('EL', 'Electronics'), ('FA', 'Fashion'), ('HO', 'Home'), ('TO', 'Toys')], default='DR', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing', to='auctions.listing')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.IntegerField()),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auction', to='auctions.listing')),
            ],
        ),
    ]
