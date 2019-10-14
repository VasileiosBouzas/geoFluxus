# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from repair.apps.asmfa.models import (KeyflowInCasestudy,
                                      Location,
                                      Material,
                                      Process)
from repair.apps.changes.models.strategies import Strategy
from repair.apps.publications.models import PublicationInCasestudy
from repair.apps.asmfa.models.nodes import (
    ActivityGroup,
    Activity,
    Actor
)

from repair.apps.login.models.bases import GDSEModel
from repair.apps.utils.protect_cascade import PROTECT_CASCADE


# General flow properties
class Flow(GDSEModel):
    amount = models.BigIntegerField(blank=True, default=0)
    keyflow = models.ForeignKey(KeyflowInCasestudy, on_delete=models.CASCADE)
    description = models.TextField(max_length=510, blank=True, null=True)
    year = models.IntegerField(default=2016)
    waste = models.BooleanField(default=False)
    process = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True)

    class Meta(GDSEModel.Meta):
        abstract = True


# Location - Location flow
class Location2Location(Flow):
    origin = models.ForeignKey(Location,
                               on_delete=PROTECT_CASCADE,
                               related_name='inputs')
    destination = models.ForeignKey(Location,
                                    on_delete=PROTECT_CASCADE,
                                    related_name='outputs')

    publication = models.ForeignKey(PublicationInCasestudy,
                                    null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='Location2LocationData')


# Group - Group flow
class Group2Group(Flow):
    destination = models.ForeignKey(ActivityGroup,
                                    on_delete=PROTECT_CASCADE,
                                    related_name='inputs')
    origin = models.ForeignKey(ActivityGroup,
                               on_delete=PROTECT_CASCADE,
                               related_name='outputs')
    publication = models.ForeignKey(PublicationInCasestudy,
                                    null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='Group2GroupData')


# Activity - activity flow
class Activity2Activity(Flow):
    destination = models.ForeignKey(Activity,
                                    on_delete=PROTECT_CASCADE,
                                    related_name='inputs')
    origin = models.ForeignKey(Activity,
                               on_delete=PROTECT_CASCADE,
                               related_name='outputs')
    publication = models.ForeignKey(PublicationInCasestudy,
                                    null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='Activity2ActivityData')

# Actor - actor flow
class Actor2Actor(Flow):
    destination = models.ForeignKey(Actor,
                                    on_delete=PROTECT_CASCADE,
                                    related_name='inputs')
    origin = models.ForeignKey(Actor,
                               on_delete=PROTECT_CASCADE,
                               related_name='outputs')
    publication = models.ForeignKey(PublicationInCasestudy,
                                    null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='Actor2ActorData')


class Stock(GDSEModel):
    # stocks relate to only one node, also data will be entered by the users
    amount = models.IntegerField(blank=True, default=0)
    keyflow = models.ForeignKey(KeyflowInCasestudy, on_delete=models.CASCADE)
    description = models.TextField(max_length=510, blank=True, null=True)
    year = models.IntegerField(default=2019)

    class Meta(GDSEModel.Meta):
        abstract = True


class GroupStock(Stock):
    origin = models.ForeignKey(ActivityGroup, on_delete=models.CASCADE,
                               related_name='stocks')
    publication = models.ForeignKey(PublicationInCasestudy, null=True, on_delete=models.SET_NULL,
                                    related_name='GroupStockData')


class ActivityStock(Stock):
    origin = models.ForeignKey(Activity, on_delete=models.CASCADE,
                               related_name='stocks')
    publication = models.ForeignKey(PublicationInCasestudy, null=True, on_delete=models.SET_NULL,
                                    related_name='ActivityStockData')


class ActorStock(Stock):
    origin = models.ForeignKey(Actor, on_delete=models.CASCADE,
                               related_name='stocks')
    publication = models.ForeignKey(PublicationInCasestudy, null=True, on_delete=models.SET_NULL,
                                    related_name='ActorStockData')