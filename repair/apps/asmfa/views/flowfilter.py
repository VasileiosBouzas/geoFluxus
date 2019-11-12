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
    Flow, AdministrativeLocation,
    Material, Flow, Actor, ActivityGroup, Activity,
    Process, FlowChain, Classification, Product, Composite, Waste
)
from repair.apps.changes.models import Strategy
from repair.apps.studyarea.models import Area

from repair.apps.asmfa.serializers import (
    FlowSerializer, FlowChainSerializer
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


# Flowchain filters
class FilterFlowChainViewSet(PostGetViewMixin, RevisionMixin,
                             CasestudyViewSetMixin,
                             ModelPermissionViewSet):
    serializer = FlowChainSerializer
    model = FlowChain

    queryset = FlowChain.objects.all()


def build_area_filter(function_name, values, keyflow_id):
    actors = Actor.objects.filter(
        activity__activitygroup__keyflow__id = keyflow_id)
    areas = Area.objects.filter(id__in = values).aggregate(area=Union('geom'))
    actors = actors.filter(
        administrative_location__geom__intersects=areas['area'])
    rest_func = 'origin__id__in' if function_name == 'origin__areas' \
        else 'destination__id__in'
    return rest_func, actors.values_list('id')


# Flow Filters
class FilterFlowViewSet(PostGetViewMixin, RevisionMixin,
                        CasestudyViewSetMixin,
                        ModelPermissionViewSet):
    serializer_class = FlowSerializer
    model = Flow
    queryset = Flow.objects.all()


    # POST is used to send filter parameters not to create
    def post_get(self, request, **kwargs):
        self.check_permission(request, 'view')

        # filter by query params
        queryset = self._filter(kwargs, query_params=request.query_params,
                                SerializerClass=self.get_serializer_class())

        # filter by flow params
        params = {}
        for key, value in request.data.items():
            try:
                params[key] = json.loads(value)
            except json.decoder.JSONDecodeError:
                params[key] = value

        # Divide filters
        filter_chains = params.get('filters', None)
        material_filter = params.get('materials', None)
        product_filter = params.get('products', None)
        composite_filter = params.get('composite', None)

        # Check the aggregation level for nodes
        l_a = params.get('aggregation_level', {})
        inv_map = {v: k for k, v in LEVEL_KEYWORD.items()}
        origin_level = inv_map[l_a['origin']] if 'origin' in l_a else Actor
        destination_level = inv_map[l_a['destination']] \
            if 'destination' in l_a else Actor

        # Filter by KEYFLOW & FILTERS
        keyflow = kwargs['keyflow_pk']
        if filter_chains:
            queryset = self.filter_chain(queryset, filter_chains, keyflow)

        # Filter by PROCESSES


        # Filter by MATERIALS
        material_ids = ([] if material_filter is None
                        else material_filter.get('unaltered', []))
        if len(material_ids) > 0:
            queryset = queryset.filter(flowchain__materials__in=
                                       Material.objects.filter(id__in=list(material_ids)))

        # Filter by PRODUCTS
        product_ids = ([] if product_filter is None
                        else product_filter.get('unaltered', []))
        if len(product_ids) > 0:
            queryset = queryset.filter(flowchain__products__in=
                                       Product.objects.filter(id__in=list(product_ids)))

        # Filter by COMPOSITES
        composite_ids = (None if composite_filter is None
                         else composite_filter.get('unaltered', []))
        if composite_ids is not None:
            queryset = queryset.filter(flowchain__composites__in=
                                       Composite.objects.filter(id__in=list(composite_ids)))

        # Serialize data
        data = self.serialize(queryset, origin_model=origin_level, destination_model=destination_level)
        return Response(data)


    def list(self, request, **kwargs):
        self.check_permission(request, 'view')
        self.check_casestudy(kwargs, request)

        queryset = self._filter(kwargs, query_params=request.query_params)
        if queryset is None:
            return Response(status=400)
        data = self.serialize(queryset)
        return Response(data)


    @staticmethod
    def serialize_nodes(nodes, add_locations=False, add_fields=[]):
        '''
        serialize actors, activities or groups in the same way
        add_locations works, only for actors
        '''
        args = ['id', 'name'] + add_fields
        if add_locations:
            args.append('administrative_location__geom')
        values = nodes.values(*args)
        node_dict = {v['id']: v for v in values}
        if add_locations:
            for k, v in node_dict.items():
                geom = v.pop('administrative_location__geom')
                v['geom'] = json.loads(geom.geojson) if geom else None
        node_dict[None] = None
        return node_dict


    def serialize(self, queryset, origin_model=Actor, destination_model=Actor,):
        '''
        serialize given queryset of flows to JSON,
        aggregates flows between nodes on actor level to the levels determined
        by origin_model and destination_model
        '''
        origin_filter = 'origin' + FILTER_SUFFIX[origin_model]
        destination_filter = 'destination' + FILTER_SUFFIX[destination_model]
        origin_level = LEVEL_KEYWORD[origin_model]
        destination_level = LEVEL_KEYWORD[destination_model]
        data = []
        origins = origin_model.objects.filter(
            id__in=list(queryset.values_list(origin_filter, flat=True)))
        destinations = destination_model.objects.filter(
            id__in=list(queryset.values_list(destination_filter, flat=True)))
        # workaround Django ORM bug
        queryset = queryset.order_by()

        groups = queryset.values(origin_filter,
                                 destination_filter,
                                 ).distinct()

        def get_code_field(model):
            if model == Actor:
                return 'activity__nace'
            if model == Activity:
                return 'nace'
            return 'code'

        origin_dict = self.serialize_nodes(
            origins, add_locations=True if origin_model == Actor else False,
            add_fields=[get_code_field(origin_model)]
        )
        destination_dict = self.serialize_nodes(
            destinations,
            add_locations=True if destination_model == Actor else False,
            add_fields=[get_code_field(destination_model)]
        )

        for group in groups:
            grouped = queryset.filter(**group)
            origin_item = origin_dict[group[origin_filter]]
            origin_item['level'] = origin_level
            dest_item = destination_dict[group[destination_filter]]
            if dest_item:
                dest_item['level'] = destination_level

            total_amount = list(
                grouped.aggregate(Sum('amount')).values())[0]

            flow_item = OrderedDict((
                ('origin', origin_item),
                ('destination', dest_item),
                ('amount', total_amount)
            ))
            data.append(flow_item)
        return data


    @staticmethod
    def filter_chain(queryset, filters, keyflow):
        for sub_filter in filters:
            filter_link = sub_filter.pop('link', 'and')
            filter_functions = []

            # Filter flowchains by keyflow
            # Retrieve only flowchain ids
            chains = FlowChain.objects.filter(keyflow__id=keyflow).only('id')

            # Production nodes (origin)
            subq = queryset.filter(Q(flowchain_id=OuterRef('pk')) &\
                                   Q(origin_role='Ontdoener'))
            chains = chains.annotate(pro_geom=
                                     Subquery(subq.values('origin__administrative_location__geom')))\
                           .annotate(pro_activity=
                                     Subquery(subq.values('origin__activity')))\
                           .annotate(pro_activitygroup=
                                     Subquery(subq.values('origin__activity__activitygroup')))

            # Collection nodes (origin or destination)
            # Check only origin to avoid duplicates
            subq = queryset.filter(Q(flowchain_id=OuterRef('pk')) &\
                                   Q(origin_role='Ontvanger'))
            chains = chains.annotate(col_geom=
                                     Subquery(subq.values('origin__administrative_location__geom')))\
                           .annotate(col_activity=
                                     Subquery(subq.values('origin__activity')))\
                           .annotate(col_activitygroup=
                                     Subquery(subq.values('origin__activity__activitygroup')))

            # Treatment nodes (destination)
            subq = queryset.filter(Q(flowchain_id=OuterRef('pk')) &\
                                   Q(destination_role='Verwerker'))
            chains = chains.annotate(treat_geom=
                                     Subquery(subq.values('destination__administrative_location__geom')))\
                           .annotate(treat_activity=
                                     Subquery(subq.values('destination__activity'))) \
                           .annotate(treat_activitygroup=
                                     Subquery(subq.values('destination__activity__activitygroup')))

            values = chains.values('id',
                                   'pro_geom',
                                   'pro_activity',
                                   'pro_activitygroup',
                                   'col_geom',
                                   'col_activity',
                                   'col_activitygroup',
                                   'treat_geom',
                                   'treat_activity',
                                   'treat_activitygroup')

            # Filter by PROCESSES
            process_ids = sub_filter.pop('process_id__in', [])
            if len(process_ids) > 0:
                queryset = queryset.filter(flowchain__process__in=
                                           Process.objects.filter(id__in=list(process_ids)))

            # Filter by WASTES
            waste_ids = sub_filter.pop('waste_id__in', [])
            if len(waste_ids) > 0:
                queryset = queryset.filter(flowchain__waste__in=
                                           Waste.objects.filter(id__in=list(waste_ids)))

            # Fields to check in parent flowchain
            flowchain_lookups = ['year',
                                 'route',
                                 'collector']

            # Annotate amount
            queryset = queryset.annotate(amount=F('flowchain__amount'))

            # Annotate classification
            classifs = Classification.objects.filter(flowchain__keyflow_id=keyflow)
            subq = classifs.filter(flowchain_id=OuterRef('flowchain'))
            # Mixed
            queryset = queryset.annotate(
                mixed=Subquery(subq.values('mixed'))
            )
            # Clean
            queryset = queryset.annotate(
                clean=Subquery(subq.values('clean'))
            )
            # Direct use
            queryset = queryset.annotate(
                direct=Subquery(subq.values('direct_use'))
            )

            for func, v in sub_filter.items():
                # Area filter
                if func.endswith('__areas'):
                    func, v = build_area_filter(func, v, keyflow)
                # Search in parent flowchain
                elif func in flowchain_lookups:
                    # Year filter
                    if func == 'year':
                        # Ignore flow year
                        if v == 'all': continue
                        v = int(v[1:])
                    filter_function = Q(**{('flowchain__' + func): v})
                elif func == 'hazardous':
                    filter_function = Q(**{('flowchain__waste__' + func): v})
                else:
                    # Search elsewhere
                    filter_function = Q(**{(func): v})

                # Append to filter functions after processing
                filter_functions.append(filter_function)

            if filter_link == 'and':
                link_func = np.bitwise_and
            else:
                link_func = np.bitwise_or
            if len(filter_functions) == 1:
                queryset = queryset.filter(filter_functions[0])
            if len(filter_functions) > 1:
                queryset = queryset.filter(link_func.reduce(filter_functions))
        return queryset







