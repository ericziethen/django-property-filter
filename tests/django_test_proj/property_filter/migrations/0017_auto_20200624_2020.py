# Generated by Django 3.0.7 on 2020-06-24 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property_filter', '0016_numberfiltermodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NumberClass',
            new_name='RangeFilterModel',
        ),
    ]