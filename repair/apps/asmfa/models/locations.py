# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.gis.db import models as gis

from repair.apps.studyarea.models import Area
from repair.apps.login.models import GDSEModelMixin
from .nodes import Actor


class Geolocation(GDSEModelMixin, gis.Model):
    geom = gis.PointField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        ret = '{s}@({g})'.format(s=self.address, g=self.geom)
        return ret

    class Meta:
        abstract = True
        default_permissions = ('add', 'change', 'delete', 'view')

    @property
    def level(self):
        """Return the adminlevel of the area, if exists, else None"""
        return getattr(self.area, 'adminlevel_id', None)


class Establishment(Geolocation):
    @property
    def casestudy(self):
        """Return establishment casestudy"""
        return self.actor.activity.activitygroup.keyflow.casestudy

    @property
    def keyflow(self):
        """Return establishment keyflow"""
        return self.actor.activity.activitygroup.keyflow

    @property
    def activitygroup(self):
        """Return establishment activity group"""
        return self.actor.activity.activitygroup

    @property
    def activity(self):
        """Return establishment activity"""
        return self.actor.activity

    class Meta(Geolocation.Meta):
        abstract = True


class Location(Establishment):
    """One actor => Many locations
       One location => One role"""
    actor = models.ForeignKey(Actor,
                              related_name='locations',
                              on_delete=models.CASCADE)

    role =  models.TextField(blank=True, null=True)
