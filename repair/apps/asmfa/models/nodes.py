# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from repair.apps.login.models import GDSEModel
from repair.apps.asmfa.models.keyflows import KeyflowInCasestudy
from repair.apps.utils.protect_cascade import PROTECT_CASCADE


class Node(GDSEModel):
    done = models.BooleanField(default=False)  # if true - data entry is done, no edit allowed

    class Meta(GDSEModel.Meta):
        abstract = True


class ActivityGroup(Node):
    # activity groups are predefined and same for all flows and case studies
    activity_group_choices = (("P1", "Production"),
                              ("P2", "Production of packaging"),
                              ("P3", "Packaging"),
                              ("D", "Distribution"),
                              ("S", "Selling"),
                              ("C", "Consuming"),
                              ("SC", "Selling and Consuming"),
                              ("R", "Return Logistics"),
                              ("COL", "Collection"),
                              ("W", "Waste Management"),
                              # 'import' and 'export' are "special" types
                              # of activity groups/activities/actors
                              ("imp", "Import"),
                              ("exp", "Export"))
    code = models.CharField(max_length=255, choices=activity_group_choices)
    name = models.CharField(max_length=255)
    keyflow = models.ForeignKey(KeyflowInCasestudy,
                                on_delete=PROTECT_CASCADE)

    @property
    def nace_codes(self):
        """
        returns a set of the nace codes of the activities
        that belong to the activity group

        Returns
        -------
        nace_code : set
        """
        return set((act['nace'] for act in self.activity_set.values()))


class Activity(Node):
    # NACE code, unique for each activity
    nace = models.CharField(max_length=255)
    # not sure about the max length, leaving everywhere 255 for now
    name = models.CharField(max_length=255)
    activitygroup = models.ForeignKey(ActivityGroup,
                                      on_delete=PROTECT_CASCADE)


class Actor(Node):
    # unique actor identifier in ORBIS database
    name = models.CharField(max_length=255)
    id = models.CharField(max_length=255)
    activity = models.ForeignKey(Activity, on_delete=PROTECT_CASCADE)

