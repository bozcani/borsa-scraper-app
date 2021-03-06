# Generated by Django 3.0.2 on 2020-04-29 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BasicApp', '0014_auto_20200427_1838'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ohlcv',
            old_name='stock_symbol',
            new_name='symbol',
        ),
        migrations.AlterUniqueTogether(
            name='ohlcv',
            unique_together={('date', 'symbol')},
        ),
    ]
