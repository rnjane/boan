from django.db import models


class Values(models.Model):
    min = models.DecimalField(max_digits=15, decimal_places=8)
    max = models.DecimalField(max_digits=15, decimal_places=8)
    greenred = models.IntegerField()
    timer = models.DateTimeField()
    open = models.DecimalField(max_digits=15, decimal_places=8)
    close = models.DecimalField(max_digits=15, decimal_places=8)
    pair = models.CharField(max_length=10)


class ValuesTest(models.Model):
    min = models.DecimalField(max_digits=15, decimal_places=8)
    max = models.DecimalField(max_digits=15, decimal_places=8)
    greenred = models.IntegerField()
    timer = models.DateTimeField()
    open = models.DecimalField(max_digits=15, decimal_places=8)
    close = models.DecimalField(max_digits=15, decimal_places=8)
    pair = models.CharField(max_length=10)


class ValuesMA(models.Model):
    min = models.DecimalField(max_digits=15, decimal_places=8)
    max = models.DecimalField(max_digits=15, decimal_places=8)
    greenred = models.IntegerField()
    timer = models.DateTimeField(db_index=True)
    open = models.DecimalField(max_digits=15, decimal_places=8)
    close = models.DecimalField(max_digits=15, decimal_places=8)
    pair = models.CharField(max_length=10)
    ma14 = models.DecimalField(max_digits=15, decimal_places=8)
    money = models.IntegerField(db_index=True)


class ValuesPsyLine(models.Model):
    min = models.DecimalField(max_digits=15, decimal_places=8)
    max = models.DecimalField(max_digits=15, decimal_places=8)
    greenred = models.IntegerField()
    timer = models.DateTimeField(db_index=True)
    open = models.DecimalField(max_digits=15, decimal_places=8)
    close = models.DecimalField(max_digits=15, decimal_places=8)
    pair = models.CharField(max_length=10)
    ma14 = models.DecimalField(max_digits=15, decimal_places=8)
    money = models.IntegerField(db_index=True)


class ValuesLen(models.Model):
    min = models.DecimalField(max_digits=15, decimal_places=8)
    max = models.DecimalField(max_digits=15, decimal_places=8)
    greenred = models.IntegerField()
    timer = models.DateTimeField(db_index=True)
    open = models.DecimalField(max_digits=15, decimal_places=8)
    close = models.DecimalField(max_digits=15, decimal_places=8)
    pair = models.CharField(max_length=10)
    ma14 = models.DecimalField(max_digits=15, decimal_places=8)
    money = models.IntegerField(db_index=True)
    ignore = models.BooleanField()


class ValuesMAComplete(models.Model):
    min = models.DecimalField(max_digits=15, decimal_places=8)
    max = models.DecimalField(max_digits=15, decimal_places=8)
    greenred = models.IntegerField()
    timer = models.DateTimeField(db_index=True)
    open = models.DecimalField(max_digits=15, decimal_places=8)
    close = models.DecimalField(max_digits=15, decimal_places=8)
    pair = models.CharField(max_length=10)
    ma14 = models.DecimalField(max_digits=15, decimal_places=8)
    money = models.IntegerField(db_index=True)


class ValuesLenComplete(models.Model):
    min = models.DecimalField(max_digits=15, decimal_places=8)
    max = models.DecimalField(max_digits=15, decimal_places=8)
    greenred = models.IntegerField()
    timer = models.DateTimeField(db_index=True)
    open = models.DecimalField(max_digits=15, decimal_places=8)
    close = models.DecimalField(max_digits=15, decimal_places=8)
    pair = models.CharField(max_length=10, db_index=True)
    ma14 = models.DecimalField(max_digits=15, decimal_places=8)
    money = models.IntegerField(db_index=True)
    ignore = models.BooleanField(db_index=True)


class ValuesComplete(models.Model):
    min = models.DecimalField(max_digits=15, decimal_places=8)
    max = models.DecimalField(max_digits=15, decimal_places=8)
    greenred = models.IntegerField()
    timer = models.DateTimeField()
    open = models.DecimalField(max_digits=15, decimal_places=8)
    close = models.DecimalField(max_digits=15, decimal_places=8)
    pair = models.CharField(max_length=10)


class HourlyProfit(models.Model):
    dtime = models.DateTimeField()
    profits = models.IntegerField()
    asset = models.CharField(max_length=10)


class ValuesMA7(models.Model):
    min = models.DecimalField(max_digits=15, decimal_places=8)
    max = models.DecimalField(max_digits=15, decimal_places=8)
    greenred = models.IntegerField()
    timer = models.DateTimeField(db_index=True)
    open = models.DecimalField(max_digits=15, decimal_places=8)
    close = models.DecimalField(max_digits=15, decimal_places=8)
    pair = models.CharField(max_length=10)
    ma14 = models.DecimalField(max_digits=15, decimal_places=8)
    money = models.IntegerField(db_index=True)


class ValuesMA25(models.Model):
    min = models.DecimalField(max_digits=15, decimal_places=8)
    max = models.DecimalField(max_digits=15, decimal_places=8)
    greenred = models.IntegerField()
    timer = models.DateTimeField(db_index=True)
    open = models.DecimalField(max_digits=15, decimal_places=8)
    close = models.DecimalField(max_digits=15, decimal_places=8)
    pair = models.CharField(max_length=10)
    ma14 = models.DecimalField(max_digits=15, decimal_places=8)
    money = models.IntegerField(db_index=True)


class ValuesLen7(models.Model):
    min = models.DecimalField(max_digits=15, decimal_places=8)
    max = models.DecimalField(max_digits=15, decimal_places=8)
    greenred = models.IntegerField()
    timer = models.DateTimeField(db_index=True)
    open = models.DecimalField(max_digits=15, decimal_places=8)
    close = models.DecimalField(max_digits=15, decimal_places=8)
    pair = models.CharField(max_length=10)
    ma14 = models.DecimalField(max_digits=15, decimal_places=8)
    money = models.IntegerField(db_index=True)
    ignore = models.BooleanField()


class ValuesLen25(models.Model):
    min = models.DecimalField(max_digits=15, decimal_places=8)
    max = models.DecimalField(max_digits=15, decimal_places=8)
    greenred = models.IntegerField()
    timer = models.DateTimeField(db_index=True)
    open = models.DecimalField(max_digits=15, decimal_places=8)
    close = models.DecimalField(max_digits=15, decimal_places=8)
    pair = models.CharField(max_length=10)
    ma14 = models.DecimalField(max_digits=15, decimal_places=8)
    money = models.IntegerField(db_index=True)
    ignore = models.BooleanField()


class ValuesMAAll(models.Model):
    min = models.DecimalField(max_digits=15, decimal_places=8)
    max = models.DecimalField(max_digits=15, decimal_places=8)
    greenred = models.IntegerField()
    timer = models.DateTimeField(db_index=True)
    open = models.DecimalField(max_digits=15, decimal_places=8)
    close = models.DecimalField(max_digits=15, decimal_places=8)
    pair = models.CharField(max_length=10)
    ma14 = models.DecimalField(max_digits=15, decimal_places=8)
    ma25 = models.DecimalField(max_digits=15, decimal_places=8)
    ma7 = models.DecimalField(max_digits=15, decimal_places=8)
    money14 = models.IntegerField(db_index=True)
    money25 = models.IntegerField(db_index=True)
    money7 = models.IntegerField(db_index=True)
