# Generated by Django 3.0.8 on 2020-08-01 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_filter', '0038_orderingfiltermodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoubleIntModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('number', models.IntegerField()),
            ],
        ),
    ]