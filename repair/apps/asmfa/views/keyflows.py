# API View
from reversion.views import RevisionMixin
from django.db.models import Q, Subquery, Count, Case, When, IntegerField
from rest_framework import serializers, exceptions
from rest_framework_datatables import pagination
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import (
    DjangoFilterBackend, Filter, FilterSet, MultipleChoiceFilter)
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.response import Response
import json

from repair.apps.asmfa.graphs.graph import BaseGraph

from repair.apps.asmfa.models import (
    Keyflow,
    KeyflowInCasestudy,
    Material,
    Waste,
    Flow,
    Product,
    Composite
)

from repair.apps.asmfa.serializers import (
    KeyflowSerializer,
    KeyflowInCasestudySerializer,
    KeyflowInCasestudyPostSerializer,
    MaterialSerializer,
    MaterialListSerializer,
    AllMaterialSerializer,
    AllMaterialListSerializer,
    WasteSerializer,
    WasteCreateSerializer,
    MaterialInChainCreateSerializer,
    ProductSerializer,
    ProductListSerializer,
    AllProductSerializer,
    AllProductListSerializer,
    ProductInChainCreateSerializer,
    CompositeSerializer,
    CompositeListSerializer,
    AllCompositeSerializer,
    AllCompositeListSerializer,
    CompositeInChainCreateSerializer
)

from repair.apps.utils.views import (CasestudyViewSetMixin,
                                     ModelPermissionViewSet)


class UnlimitedResultsSetPagination(pagination.DatatablesPageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'


class KeyflowViewSet(ModelPermissionViewSet):
    add_perm = 'asmfa.add_keyflow'
    change_perm = 'asmfa.change_keyflow'
    delete_perm = 'asmfa.delete_keyflow'
    queryset = Keyflow.objects.order_by('id')
    serializer_class = KeyflowSerializer


class KeyflowInCasestudyViewSet(CasestudyViewSetMixin, ModelPermissionViewSet):
    """
    API endpoint that allows Keyflowincasestudy to be viewed or edited.
    """
    add_perm = 'asmfa.add_keyflowincasestudy'
    change_perm = 'asmfa.change_keyflowincasestudy'
    delete_perm = 'asmfa.delete_keyflowincasestudy'
    queryset = KeyflowInCasestudy.objects.order_by('id')
    serializer_class = KeyflowInCasestudySerializer
    serializers = {'create': KeyflowInCasestudyPostSerializer,
                   'update': KeyflowInCasestudyPostSerializer}

    @action(methods=['get', 'post'], detail=True)
    def build_graph(self, request, **kwargs ):
        keyflow = self.queryset.get(id=kwargs['pk'])
        kfgraph = BaseGraph(keyflow)
        graph = kfgraph.build()
        #return Response(kfgraph.serialize(graph))
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['get', 'post'], detail=True)
    def validate_graph(self, request, **kwargs):
        keyflow = self.queryset.get(id=kwargs['pk'])
        kfgraph = BaseGraph(keyflow)
        res = kfgraph.validate()
        return Response(res)


class CommaSeparatedValueFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        self.lookup_expr = 'in'
        values = value.split(',')
        return super(CommaSeparatedValueFilter, self).filter(qs, values)


class WasteFilter(FilterSet):
    nace = CommaSeparatedValueFilter(field_name='nace')

    class Meta:
        model = Waste
        fields = ('ewc_code', 'ewc_name', 'hazardous')


class MaterialFilter(FilterSet):

    class Meta:
        model = Material
        fields = ('name', 'keyflow')

class ProductFilter(FilterSet):

    class Meta:
        model = Product
        fields = ('name', 'keyflow')

class CompositeFilter(FilterSet):

    class Meta:
        model = Composite
        fields = ('name', 'keyflow')


class AllWasteViewSet(RevisionMixin, ModelPermissionViewSet):
    pagination_class = UnlimitedResultsSetPagination
    add_perm = 'asmfa.add_waste'
    change_perm = 'asmfa.change_waste'
    delete_perm = 'asmfa.delete_waste'
    queryset = Waste.objects.order_by('id')
    serializer_class = WasteSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = WasteFilter


class WasteViewSet(CasestudyViewSetMixin, AllWasteViewSet):
    pagination_class = UnlimitedResultsSetPagination
    serializer_class = WasteSerializer
    serializers = {
        'list': WasteSerializer,
        'create': WasteCreateSerializer
    }
    # include products with keyflow-pk == null as well
    def get_queryset(self):
        keyflow_id = self.kwargs['keyflow_pk']

        wastes = Waste.objects.\
            select_related("keyflow__casestudy").defer(
                "keyflow__note", "keyflow__casestudy__geom",
                "keyflow__casestudy__focusarea")
        if 'nace[]' in self.request.query_params.keys():
            nace = self.request.GET.getlist('nace[]')
            wastes = wastes.filter(nace__in=nace)
        return wastes\
               .filter(Q(keyflow__isnull=True) | Q(keyflow=keyflow_id))\
               .order_by('id')


class AllMaterialViewSet(RevisionMixin, ModelPermissionViewSet):
    add_perm = 'asmfa.add_material'
    change_perm = 'asmfa.change_material'
    delete_perm = 'asmfa.delete_material'
    queryset = Material.objects.order_by('id')
    serializer_class = AllMaterialSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = MaterialFilter
    serializers = {'list': AllMaterialListSerializer}


class MaterialViewSet(CasestudyViewSetMixin, AllMaterialViewSet):
    pagination_class = UnlimitedResultsSetPagination
    serializer_class = MaterialSerializer
    serializers = {
        'list': MaterialListSerializer,
        'create': MaterialInChainCreateSerializer,
    }

    # include materials with keyflows with pk null as well (those are the default ones)
    def get_queryset(self):
        keyflow_id = self.kwargs['keyflow_pk']

        materials = Material.objects.\
            select_related("keyflow__casestudy").defer(
                "keyflow__note", "keyflow__casestudy__geom",
                "keyflow__casestudy__focusarea")
        materials = materials.filter(
            Q(keyflow__isnull=True) | Q(keyflow=keyflow_id)).order_by('id')

        # calc flow_count
        # flows = Flow.objects.filter(
        #     Q(oactor__activity__activitygroup__keyflow__id=keyflow_id) |
        #     Q(destination__actor__activity__activitygroup__keyflow__id=keyflow_id)
        # )
        # materials = materials.annotate(
        #     flow_count=Count(Case(
        #         When(flowchain__in=flows, then=1),
        #         output_field=IntegerField(),
        #     ))
        # )
        return materials

    def checkMethod(self, request, **kwargs):
        model = self.serializer_class.Meta.model
        try:
            instance = model.objects.get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            return
        if instance.keyflow is None:
            raise exceptions.MethodNotAllowed(
                'PUT',
                _('This material is a default material '
                  'and can neither be edited nor deleted.')
            )

    def update(self, request, **kwargs):
        self.checkMethod(request, **kwargs)
        return super().update(request, **kwargs)

    def destroy(self, request, **kwargs):
        self.checkMethod(request, **kwargs)
        return super().destroy(request, **kwargs)


class AllProductViewSet(RevisionMixin, ModelPermissionViewSet):
    add_perm = 'asmfa.add_product'
    change_perm = 'asmfa.change_product'
    delete_perm = 'asmfa.delete_product'
    queryset = Product.objects.order_by('id')
    serializer_class = AllProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ProductFilter
    serializers = {'list': AllProductListSerializer}


class ProductViewSet(CasestudyViewSetMixin, AllProductViewSet):
    pagination_class = UnlimitedResultsSetPagination
    serializer_class = ProductSerializer
    serializers = {
        'list': ProductListSerializer,
        'create': ProductInChainCreateSerializer,
    }

    # include materials with keyflows with pk null as well (those are the default ones)
    def get_queryset(self):
        keyflow_id = self.kwargs['keyflow_pk']

        products = Product.objects.\
            select_related("keyflow__casestudy").defer(
                "keyflow__note", "keyflow__casestudy__geom",
                "keyflow__casestudy__focusarea")
        products = products.filter(
            Q(keyflow__isnull=True) | Q(keyflow=keyflow_id)).order_by('id')

        # calc flow_count
        # flows = Flow.objects.filter(
        #     Q(origin__actor__activity__activitygroup__keyflow__id=keyflow_id) |
        #     Q(destination__actor__activity__activitygroup__keyflow__id=keyflow_id)
        # )
        # materials = materials.annotate(
        #     flow_count=Count(Case(
        #         When(flowchain__in=flows, then=1),
        #         output_field=IntegerField(),
        #     ))
        # )
        return products

    def checkMethod(self, request, **kwargs):
        model = self.serializer_class.Meta.model
        try:
            instance = model.objects.get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            return
        if instance.keyflow is None:
            raise exceptions.MethodNotAllowed(
                'PUT',
                _('This product is a default product'
                  'and can neither be edited nor deleted.')
            )

    def update(self, request, **kwargs):
        self.checkMethod(request, **kwargs)
        return super().update(request, **kwargs)

    def destroy(self, request, **kwargs):
        self.checkMethod(request, **kwargs)
        return super().destroy(request, **kwargs)


class AllCompositeViewSet(RevisionMixin, ModelPermissionViewSet):
    add_perm = 'asmfa.add_composite'
    change_perm = 'asmfa.change_composite'
    delete_perm = 'asmfa.delete_composite'
    queryset = Composite.objects.order_by('id')
    serializer_class = AllCompositeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = CompositeFilter
    serializers = {'list': AllCompositeListSerializer}


class CompositeViewSet(CasestudyViewSetMixin, AllCompositeViewSet):
    pagination_class = UnlimitedResultsSetPagination
    serializer_class = CompositeSerializer
    serializers = {
        'list': CompositeListSerializer,
        'create': CompositeInChainCreateSerializer,
    }

    # include materials with keyflows with pk null as well (those are the default ones)
    def get_queryset(self):
        keyflow_id = self.kwargs['keyflow_pk']

        products = Composite.objects.\
            select_related("keyflow__casestudy").defer(
                "keyflow__note", "keyflow__casestudy__geom",
                "keyflow__casestudy__focusarea")
        products = products.filter(
            Q(keyflow__isnull=True) | Q(keyflow=keyflow_id)).order_by('id')

        # calc flow_count
        # flows = Flow.objects.filter(
        #     Q(origin__actor__activity__activitygroup__keyflow__id=keyflow_id) |
        #     Q(destination__actor__activity__activitygroup__keyflow__id=keyflow_id)
        # )
        # materials = materials.annotate(
        #     flow_count=Count(Case(
        #         When(flowchain__in=flows, then=1),
        #         output_field=IntegerField(),
        #     ))
        # )
        return products

    def checkMethod(self, request, **kwargs):
        model = self.serializer_class.Meta.model
        try:
            instance = model.objects.get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            return
        if instance.keyflow is None:
            raise exceptions.MethodNotAllowed(
                'PUT',
                _('This composite is a default composite'
                  'and can neither be edited nor deleted.')
            )

    def update(self, request, **kwargs):
        self.checkMethod(request, **kwargs)
        return super().update(request, **kwargs)

    def destroy(self, request, **kwargs):
        self.checkMethod(request, **kwargs)
        return super().destroy(request, **kwargs)
