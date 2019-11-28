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


def merge(queryset):
    # producer flows
    pros = queryset.filter(origin_role='Ontdoener')\
                   .values('flowchain',
                           'origin')

    # treatment flows
    treats = queryset.filter(destination_role='Verwerker')\
                     .values('destination')

    subq = treats.filter(flowchain=OuterRef('flowchain'))
    queryset = pros.annotate(destination__id=
                             Subquery(subq.values('destination__id')),
                             destination__activity__id=
                             Subquery(subq.values('destination__activity__id')),
                             destination__activity__activitygroup__id=
                             Subquery(subq.values('destination__activity__activitygroup__id')))

    return queryset


def build_chain_filter(filter, queryset, keyflow):
    # Role is meaningless without nodes or areas
    if len(filter) == 1:
        return queryset

    # Filter flowchains by keyflow
    # Retrieve only flowchain ids
    chains = FlowChain.objects.filter(keyflow__id=keyflow).values('id')

    # Retrieve role
    role = filter.pop('role') # retrieve role

    # Retrieve areas
    values = filter.pop('areas', []) # retrieve areas
    if len(values) > 0: # avoid intersecting all multipolygons!!!
        areas = Area.objects.filter(id__in = values).aggregate(area=Union('geom'))

    # Retrieve activities or activitygroups
    acts, ids = [], []
    if len(filter) > 0:
        acts, ids = filter.popitem()

    intersects, is_ins = [], []
    # Production nodes (origin)
    if (role != 'collection' and role != 'treatment'):
        subq = queryset.filter(flowchain_id=OuterRef('pk'),
                               origin_role='Ontdoener')
        if len(values) > 0:
            chains = chains.annotate(pro_geom=
                                     Subquery(subq.values('origin__administrative_location__geom'))
                                     )
            intersects.append('pro_geom__intersects')
        if len(acts) > 0:
            chains = chains.annotate(pro_act=
                                     Subquery(subq.values('origin' + acts))
                                     )
            is_ins.append('pro_act__in')

    # Collection nodes (origin or destination)
    # Check only origin to avoid duplicates
    if (role != 'production' and role != 'treatment'):
        subq = queryset.filter(flowchain_id=OuterRef('pk'),
                               origin_role='Ontvanger')
        if len(values) > 0:
            chains = chains.annotate(col_geom=
                                     Subquery(subq.values('origin__administrative_location__geom'))
                                     )
            intersects.append('col_geom__intersects')
        if len(acts) > 0:
            chains = chains.annotate(col_act=
                                     Subquery(subq.values('origin' + acts))
                                     )
            is_ins.append('col_act__in')

    # Treatment nodes (destination)
    if (role != 'production' and role != 'collection'):
        subq = queryset.filter(flowchain_id=OuterRef('pk'),
                               destination_role='Verwerker')
        if len(values) > 0:
            chains = chains.annotate(treat_geom=
                                     Subquery(subq.values('destination__administrative_location__geom'))
                                     )
            intersects.append('treat_geom__intersects')
        if len(acts) > 0:
            chains = chains.annotate(treat_act=
                                     Subquery(subq.values('destination' + acts))
                                     )
            is_ins.append('treat_act__in')

    filter_functions = []
    # Both area and activity/group check
    if len(intersects) > 0 and len(is_ins) > 0:
        for intersect, is_in in zip(intersects, is_ins):
            filter_functions.append(Q(**{intersect : areas['area'],
                                         is_in : ids}))
    # Only area
    elif len(intersects) > 0:
        for intersect in intersects:
            filter_functions.append(Q(**{intersect : areas['area']}))
    # Only activity/group
    else:
        for is_in in is_ins:
            filter_functions.append(Q(**{is_in : ids}))

    # Apply filters to CHAINS
    # SOLVE BUG!!!
    if role == 'all':
        # ALL nodes should satisfy the criteri
        chains = chains.filter(np.bitwise_and.reduce(filter_functions))
    elif role == 'any':
        # ANY node should satisfy the criteria
        chains = chains.filter(np.bitwise_or.reduce(filter_functions))
    else:
        # REQUESTED node should satisfy the criteria
        chains = chains.filter(filter_functions[0])

    chains = list(chains.values_list('id', flat=True))
    return queryset.filter(flowchain_id__in=chains)


# Flowchain filters
class FilterFlowChainViewSet(PostGetViewMixin, RevisionMixin,
                             CasestudyViewSetMixin,
                             ModelPermissionViewSet):
    serializer = FlowChainSerializer
    model = FlowChain

    queryset = FlowChain.objects.all()


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
        middle = params.get('middle', False);
        chain = params.get('chain', None)
        filter_chains = params.get('filters', None)
        material_filter = params.get('materials', None)
        product_filter = params.get('products', None)
        composite_filter = params.get('composites', None)

        # Check the aggregation level for nodes
        l_a = params.get('aggregation_level', {})
        inv_map = {v: k for k, v in LEVEL_KEYWORD.items()}
        origin_level = inv_map[l_a['origin']] if 'origin' in l_a else Actor
        destination_level = inv_map[l_a['destination']] \
            if 'destination' in l_a else Actor

        # Filter by CHAIN
        keyflow = kwargs['keyflow_pk']
        if chain:
            queryset = build_chain_filter(chain, queryset, keyflow)

        # remove collection node
        if middle: queryset = merge(queryset)

        # Filter by FILTERS
        if filter_chains:
            queryset = self.filter_chain(self, queryset, filter_chains, keyflow)

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
        composite_ids = ([] if composite_filter is None
                         else composite_filter.get('unaltered', []))
        if len(composite_ids) > 0:
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
        origin_filter = 'origin' + FILTER_SUFFIX[origin_model] + '__id'
        destination_filter = 'destination' + FILTER_SUFFIX[destination_model] + '__id'
        origin_level = LEVEL_KEYWORD[origin_model]
        destination_level = LEVEL_KEYWORD[destination_model]
        data = []
        origins = origin_model.objects.filter(
            id__in=list(queryset.values_list(origin_filter, flat=True)))
        destinations = destination_model.objects.filter(
            id__in=list(queryset.values_list(destination_filter, flat=True)))
        # workaround Django ORM bug
        queryset = queryset.order_by()

        # Annotate amount
        queryset = queryset.annotate(amount=F('flowchain__amount'),
                                     description=F('flowchain__description'))

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
            description = list(grouped.values_list('description', flat=True).distinct())

            flow_item = OrderedDict((
                ('origin', origin_item),
                ('destination', dest_item),
                ('amount', total_amount),
                ('description', description)
            ))
            data.append(flow_item)
        return data


    @staticmethod
    def filter_classif(queryset, filter):
        funcs = []
        lookup, options = filter
        for option in options:
            funcs.append(Q(**{lookup : option}))
        if len(funcs) == 1:
            queryset = queryset.filter(funcs[0])
        else:
            queryset = queryset.filter(np.bitwise_or.reduce(funcs))
        return queryset


    @staticmethod
    def filter_chain(self, queryset, filters, keyflow):
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

        # Fields to check in parent flowchain
        flowchain_lookups = ['year',
                             'route',
                             'collector',
                             'process_id__in',
                             'waste_id__in']

        classif_lookups = ['clean',
                           'mixed',
                           'direct']
        
        for sub_filter in filters:
            filter_link = sub_filter.pop('link', 'and')
            filter_functions = []

            for lookup in classif_lookups:
                options = sub_filter.pop(lookup, None)
                if options is not None:
                    filter = (lookup, options)
                    queryset = self.filter_classif(queryset, filter)

            for func, v in sub_filter.items():
                # Search in parent flowchain
                if func in flowchain_lookups:
                    # Year filter
                    if func == 'year': v = int(v[1:])
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







