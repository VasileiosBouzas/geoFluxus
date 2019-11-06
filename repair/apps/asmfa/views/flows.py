# API View
from abc import ABC
from repair.apps.asmfa.views import UnlimitedResultsSetPagination

from rest_framework.viewsets import ModelViewSet
from reversion.views import RevisionMixin

from repair.apps.utils.views import (CasestudyViewSetMixin,
                                     ModelPermissionViewSet,
                                     PostGetViewMixin)


from repair.apps.asmfa.models import (
    FlowChain,
    Flow,
    Process,
    Stock,
    Material,
    Classification,
    ExtraDescription
)

from repair.apps.asmfa.serializers import (
    FlowChainSerializer,
    FlowSerializer,
    ProcessSerializer,
    StockSerializer,
    FlowCreateSerializer,
    FlowChainCreateSerializer,
    StockCreateSerializer,
    MaterialSerializer,
    MaterialInChainCreateSerializer,
    ClassificationSerializer,
    ClassificationCreateSerializer,
    ExtraDescriptionSerializer,
    ExtraDescriptionCreateSerializer
)

# FlowChain View
class FlowChainViewSetAbstract(RevisionMixin,
                               CasestudyViewSetMixin,
                               ModelPermissionViewSet,
                               ABC):
    serializer_class = FlowChainSerializer
    model = FlowChain
    pagination_class = UnlimitedResultsSetPagination


class FlowChainViewSet(FlowChainViewSetAbstract):
    add_perm = 'asmfa.add_flowchain'
    change_perm = 'asmfa.change_flowchain'
    delete_perm = 'asmfa.delete_flowchain'
    queryset =  FlowChain.objects.all()
    serializer_class = FlowChainSerializer
    serializers = {
        'list': FlowChainSerializer,
        'create': FlowChainCreateSerializer
    }


# Flow View
class FlowViewSetAbstract(RevisionMixin,
                          CasestudyViewSetMixin,
                          ModelPermissionViewSet,
                          ABC):
    """
    Abstract BaseClass for a FlowViewSet
    The Subclass has to provide a model inheriting from Flow
    and a serializer-class inheriting form and a model
    """
    serializer_class = FlowSerializer
    model = Flow
    pagination_class = UnlimitedResultsSetPagination


class FlowViewSet(FlowViewSetAbstract):
    add_perm = 'asmfa.add_flow'
    change_perm = 'asmfa.change_flow'
    delete_perm = 'asmfa.delete_flow'
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer
    serializers = {
        'list': FlowSerializer,
        'create': FlowCreateSerializer
    }


# Stock View
class StockViewSetAbstract(RevisionMixin,
                           CasestudyViewSetMixin,
                           ModelPermissionViewSet,
                           ABC):
    serializer_class = StockSerializer
    model = Stock
    pagination_class = UnlimitedResultsSetPagination


class StockViewSet(StockViewSetAbstract):
    add_perm = 'asfma.add_stock'
    change_perm = 'asmfa.change_stock'
    delete_perm = 'asmfa.delete_stock'
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    serializers = {
        'list': StockSerializer,
        'create': StockCreateSerializer
    }


class ClassificationViewSetAbstract(RevisionMixin,
                                    CasestudyViewSetMixin,
                                    ModelPermissionViewSet,
                                    ABC):
    serializer_class = ClassificationSerializer
    model = Classification
    pagination_class = UnlimitedResultsSetPagination


class ClassificationViewSet(ClassificationViewSetAbstract):
    add_perm = 'asfma.add_classification'
    change_perm = 'asmfa.change_classification'
    delete_perm = 'asmfa.delete_classification'
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
    serializers = {
        'list': ClassificationSerializer,
        'create': ClassificationCreateSerializer
    }


class ExtraDescriptionViewSetAbstract(RevisionMixin,
                                     CasestudyViewSetMixin,
                                     ModelPermissionViewSet,
                                     ABC):
    serializer_class = ExtraDescriptionSerializer
    model = ExtraDescription
    pagination_class = UnlimitedResultsSetPagination


class ExtraDescriptionViewSet(ClassificationViewSetAbstract):
    add_perm = 'asfma.add_extradescription'
    change_perm = 'asmfa.change_extradescription'
    delete_perm = 'asmfa.delete_extradescription'
    queryset = ExtraDescription.objects.all()
    serializer_class = ExtraDescriptionSerializer
    serializers = {
        'list': ExtraDescriptionSerializer,
        'create': ExtraDescriptionCreateSerializer
    }


class ProcessViewSet(ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
