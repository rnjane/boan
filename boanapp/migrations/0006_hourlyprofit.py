# Generated by Django 2.2.3 on 2019-09-16 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boanapp', '0005_valuescomplete'),
    ]

    operations = [
        migrations.CreateModel(
            name='HourlyProfit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dtime', models.DateTimeField()),
                ('profits', models.IntegerField()),
            ],
        ),
    ]
