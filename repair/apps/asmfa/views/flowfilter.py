from collections import defaultdict, OrderedDict
from rest_framework.viewsets import ModelViewSet
from reversion.views import RevisionMixin
from django.contrib.gis.geos import GEOSGeometry
from django.http import HttpResponseBadRequest, HttpResponse
from django.db.models.functions import Coalesce
from django.db.models import (Q, Subquery, Min, IntegerField, OuterRef, Sum, F,
                              Case, When, Value, QuerySet, Count,
                              FilteredRelation)
import numpy as np
import copy
import json
from collections import defaultdict, OrderedDict
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.db.models import Union
from rest_framework.response import Response
from rest_framework.decorators import action

from repair.apps.utils.views import (CasestudyViewSetMixin,
                                     ModelPermissionViewSet,
                                     PostGetViewMixin)
from repair.apps.utils.utils import descend_materials

from repair.apps.asmfa.models import (
    Flow, Location,
    Material, Flow, Actor, ActivityGroup, Activity,
    Location, Process, FlowChain
)
from repair.apps.changes.models import Strategy
from repair.apps.studyarea.models import Area

from repair.apps.asmfa.serializers import (
    FlowSerializer, FlowChainSerializer
)

# structure of serialized components of a flow as the serializer
# will return it
flowchain_struct = OrderedDict(id=None,
                               route=None,
                               collector=None,
                               trips=0,
                               description=None,
                               amount=0,
                               year=0,
                               waste=None,
                               keyflow_id=None,
                               material_id=None,
                               process_id=None,
                               publication_id=None
                              )


flow_struct = OrderedDict(id=None,
                          flowchain_id=None,
                          origin=None,
                          destination=None,
                          origin_level=None,
                          destination_level=None,
                          )


FILTER_SUFFIX = {
    Actor: '',
    Activity: '__activity',
    ActivityGroup: '__activity__activitygroup'
}

LEVEL_KEYWORD = {
    Actor: 'actor',
    Activity: 'activity',
    ActivityGroup: 'activitygroup'
}


# Filter flowchain for keyflow
class FilterFlowChainViewSet(PostGetViewMixin, RevisionMixin,
                             CasestudyViewSetMixin,
                             ModelPermissionViewSet):
    serializer = FlowChainSerializer
    model = FlowChain

    queryset = FlowChain.objects.all()


# Flow Fliters
class FilterFlowViewSet(PostGetViewMixin, RevisionMixin,
                        CasestudyViewSetMixin,
                        ModelPermissionViewSet):
    serializer_class = FlowSerializer
    model = Flow

    queryset = Flow.objects.all()



