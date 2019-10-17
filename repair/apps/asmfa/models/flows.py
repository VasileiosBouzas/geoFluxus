# -*- coding: utf-8 -*-
# Hello from another dimension!
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



class FlowChain(GDSEModel):
    # Chain specifics
    process = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True)
    route = models.BooleanField(default=False)
    collector = models.BooleanField(default=False)
    trips = models.IntegerField(blank=True, default=0)

    # Flow properties
    keyflow = models.ForeignKey(KeyflowInCasestudy, on_delete=models.CASCADE)
    description = models.TextField(max_length=510, blank=True, null=True)
    amount = models.BigIntegerField(blank=True, default=0)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, default='')
    year = models.IntegerField(default=2019)
    waste = models.BooleanField(default=False)
    publication = models.ForeignKey(PublicationInCasestudy,null=True,on_delete=models.SET_NULL)


# Flow
class Flow(GDSEModel):
    """One chain => Many flows"""
    flowchain = models.ForeignKey(FlowChain, on_delete=models.CASCADE)
    destination = models.ForeignKey(Location,
                                    on_delete=PROTECT_CASCADE,
                                    related_name='destination')
    origin = models.ForeignKey(Location,
                               on_delete=PROTECT_CASCADE,
                               related_name='origin')


class Stock(GDSEModel):
    # stocks relate to only one node, also data will be entered by the users
    amount = models.IntegerField(blank=True, default=0)
    keyflow = models.ForeignKey(KeyflowInCasestudy, on_delete=models.CASCADE)
    description = models.TextField(max_length=510, blank=True, null=True)
    year = models.IntegerField(default=2019)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, default='')
    publication = models.ForeignKey(PublicationInCasestudy, null=True, on_delete=models.SET_NULL)