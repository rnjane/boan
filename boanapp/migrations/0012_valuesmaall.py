# Generated by Django 2.2.3 on 2019-11-18 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boanapp', '0011_valueslen25_valueslen7'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValuesMAAll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min', models.DecimalField(decimal_places=8, max_digits=15)),
                ('max', models.DecimalField(decimal_places=8, max_digits=15)),
                ('greenred', models.IntegerField()),
                ('timer', models.DateTimeField(db_index=True)),
                ('open', models.DecimalField(decimal_places=8, max_digits=15)),
                ('close', models.DecimalField(decimal_places=8, max_digits=15)),
                ('pair', models.CharField(max_length=10)),
                ('ma14', models.DecimalField(decimal_places=8, max_digits=15)),
                ('ma25', models.DecimalField(decimal_places=8, max_digits=15)),
                ('ma7', models.DecimalField(decimal_places=8, max_digits=15)),
                ('ignore', models.BooleanField()),
                ('money', models.IntegerField(db_index=True)),
            ],
        ),
    ]
