# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from .keyflows import (KeyflowInCasestudy, Product)
from .nodes import (
    DataEntry,
    ActivityGroup,
    Activity,
    Actor,
)

class Stock(models.Model):

    # stocks relate to only one node, also data will be entered by the users
    amount = models.IntegerField(blank=True, default=0)
    keyflow = models.ForeignKey(KeyflowInCasestudy, on_delete=models.CASCADE)
    description = models.TextField(max_length=510, blank=True, null=True)
    year = models.IntegerField(default=2016)

    class Meta:
        abstract = True


class GroupStock(Stock):

    origin = models.ForeignKey(ActivityGroup, on_delete=models.CASCADE,
                               related_name='stocks')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='GroupStocks')
    entry = models.ForeignKey(DataEntry, on_delete=models.CASCADE,
                              related_name='GroupStockData', default=1)


class ActivityStock(Stock):

    origin = models.ForeignKey(Activity, on_delete=models.CASCADE,
                               related_name='stocks')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='ActivityStocks')
    entry = models.ForeignKey(DataEntry, on_delete=models.CASCADE,
                              related_name='ActivityStockData', default=1)


class ActorStock(Stock):

    origin = models.ForeignKey(Actor, on_delete=models.CASCADE,
                               related_name='stocks')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='ActorStocks')
    entry = models.ForeignKey(DataEntry, on_delete=models.CASCADE,
                              related_name='ActorStockData', default=1)
