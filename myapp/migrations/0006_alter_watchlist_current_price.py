# Generated by Django 5.1.2 on 2024-10-16 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_remove_watchlist_added_at_watchlist_current_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='current_price',
            field=models.FloatField(),
        ),
    ]
