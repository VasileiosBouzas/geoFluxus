# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.functional import cached_property

from django.db import models
from collections import defaultdict

from repair.apps.login.models import (CaseStudy, GDSEModel)
from repair.apps.publications.models import PublicationInCasestudy
from repair.apps.utils.protect_cascade import PROTECT_CASCADE


# General keyflow properties
class Keyflow(GDSEModel):
    # the former "Material" class - not to confuse with the other one
    keyflow_choices = (("Org", "Organic"),
                       ("CDW", "Construction & Demolition"),
                       ("Food", "Food"),
                       ("MSW", "Municipal Solid Waste"),
                       ("PCPW", "Post-Consumer Plastic"),
                       ("HHW", "Household Hazardous Waste"))
    code = models.TextField(choices=keyflow_choices)
    name = models.TextField()
    casestudies = models.ManyToManyField(CaseStudy,
                                         through='KeyflowInCasestudy')

# Keyflow in case study
class KeyflowInCasestudy(GDSEModel):
    keyflow = models.ForeignKey(Keyflow, on_delete=models.CASCADE,
                                related_name='products')
    casestudy = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)

    def __str__(self):
        return 'KeyflowInCasestudy {pk}: {k} in {c}'.format(
            pk=self.pk, k=self.keyflow, c=self.casestudy)


# Material
class Material(GDSEModel):
    name = models.CharField(max_length=255)
    keyflow = models.ForeignKey(KeyflowInCasestudy, on_delete=PROTECT_CASCADE,
                                null=True)


# Process
class Process(GDSEModel):
    name = models.TextField(max_length=255, default='')
    code = models.TextField(max_length=255, default='')


# Waste
class Waste(GDSEModel):
    ewc_code = models.CharField(max_length=255, default='')
    ewc_name = models.CharField(max_length=255, default='')
    hazardous = models.BooleanField(default=False)