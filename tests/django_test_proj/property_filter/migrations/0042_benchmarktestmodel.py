# Generated by Django 3.0.8 on 2020-08-31 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_filter', '0041_multifiltertestmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='BenchmarkTestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('date_time', models.DateTimeField()),
                ('is_true', models.BooleanField(null=True)),
                ('number', models.IntegerField(null=True)),
                ('text', models.CharField(max_length=32)),
                ('duration', models.DurationField()),
            ],
        ),
    ]
