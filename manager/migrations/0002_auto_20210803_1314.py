# Generated by Django 3.2.6 on 2021-08-03 13:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='axie',
            old_name='owner',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='owner',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='owner',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 8, 3, 13, 13, 53, 203706, tzinfo=utc)),
        ),
    ]