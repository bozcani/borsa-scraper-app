# Generated by Django 3.0.2 on 2020-04-27 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BasicApp', '0013_auto_20200306_1414'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ohlcv',
            unique_together={('date', 'stock_symbol')},
        ),
    ]
