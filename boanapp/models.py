from django.db import models


class Values(models.Model):
    min = models.DecimalField(max_digits=15, decimal_places=8)
    max = models.DecimalField(max_digits=15, decimal_places=8)
    greenred = models.IntegerField()
    timer = models.DateTimeField()
    open = models.DecimalField(max_digits=15, decimal_places=8)
    close = models.DecimalField(max_digits=15, decimal_places=8)
    pair = models.CharField(max_length=10)
