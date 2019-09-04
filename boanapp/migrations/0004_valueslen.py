# Generated by Django 2.2.3 on 2019-09-04 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boanapp', '0003_auto_20190821_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValuesLen',
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
                ('money', models.IntegerField(db_index=True)),
                ('ignore', models.BooleanField()),
            ],
        ),
    ]