# Generated by Django 3.0.7 on 2020-06-24 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property_filter', '0018_timefiltermodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TimeClass',
            new_name='TimeRangeModel',
        ),
    ]