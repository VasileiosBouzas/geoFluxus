# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from repair.apps.asmfa.models import (KeyflowInCasestudy,
                                      Actor,
                                      Material,
                                      Process,
                                      Waste,
                                      Product,
                                      Composite)
from repair.apps.publications.models import PublicationInCasestudy

from repair.apps.login.models.bases import GDSEModel
from repair.apps.utils.protect_cascade import PROTECT_CASCADE


# Flow Chain
class FlowChain(GDSEModel):
    # Chain specifics
    identifier = models.CharField(max_length=255)
    process = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True)
    route = models.BooleanField(default=False)
    collector = models.BooleanField(default=False)
    trips = models.IntegerField(blank=True, default=0)

    # Flow properties
    keyflow = models.ForeignKey(KeyflowInCasestudy, on_delete=models.CASCADE)
    description = models.TextField(max_length=510, blank=True, null=True)
    amount = models.DecimalField(decimal_places=3, max_digits=3, default=0)
    materials = models.ManyToManyField(Material,
                                       through='MaterialInChain')
    products = models.ManyToManyField(Product,
                                      through='ProductInChain')
    composites = models.ManyToManyField(Composite,
                                        through='CompositeInChain')
    year = models.IntegerField(default=2019)
    waste = models.ForeignKey(Waste, on_delete=models.CASCADE, default='')
    publication = models.ForeignKey(PublicationInCasestudy,null=True,on_delete=models.SET_NULL)


# Flow
class Flow(GDSEModel):
    """One chain => Many flows"""
    flowchain = models.ForeignKey(FlowChain, on_delete=models.CASCADE)
    destination = models.ForeignKey(Actor,
                                    on_delete=PROTECT_CASCADE,
                                    related_name='outputs')
    origin = models.ForeignKey(Actor,
                               on_delete=PROTECT_CASCADE,
                               related_name='inputs')
    origin_role = models.CharField(max_length=255, default='')
    destination_role = models.CharField(max_length=255, default='')


# Stock
class Stock(GDSEModel):
    # stocks relate to only one node, also data will be entered by the users
    identifier = models.CharField(max_length=255)
    origin = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='origin')
    amount = models.IntegerField(blank=True, default=0)
    keyflow = models.ForeignKey(KeyflowInCasestudy, on_delete=models.CASCADE)
    description = models.TextField(max_length=510, blank=True, null=True)
    year = models.IntegerField(default=2019)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, default='')
    publication = models.ForeignKey(PublicationInCasestudy, null=True, on_delete=models.SET_NULL)


# Material in Chain
class MaterialInChain(GDSEModel):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    flowchain = models.ForeignKey(FlowChain, on_delete=models.CASCADE)


# Product in Chain
class ProductInChain(GDSEModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    flowchain = models.ForeignKey(FlowChain, on_delete=models.CASCADE)


# Product in Chain
class CompositeInChain(GDSEModel):
    composite = models.ForeignKey(Composite, on_delete=models.CASCADE)
    flowchain = models.ForeignKey(FlowChain, on_delete=models.CASCADE)


# Classification
class Classification(GDSEModel):
    flowchain = models.ForeignKey(FlowChain, on_delete=models.CASCADE)
    clean = models.BooleanField(default=False)
    mixed = models.BooleanField(default=False)


# Extra description
class ExtraDescription(GDSEModel):
    flowchain = models.ForeignKey(FlowChain, on_delete=models.CASCADE)
    description_type_choices = (("RE", "Reason"),
                                ("OR", "Origin"),
                                ("COL", "Colour"),
                                ("ST", "State"),
                                ("DIM", "Dimensions"),
                                ("SH", "Shape"),
                                ("CON", "Consistency"),
                                ("COD", "Codes"),
                                ("MAT", "Material type"),
                                ("COMP", "Composition type"),
                                ("PRO", "Product type")
                                )
    type = models.CharField(max_length=255, choices=description_type_choices, default='')
    description = models.TextField(default='', null=True)