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
    Stock
)

from repair.apps.asmfa.serializers import (
    FlowChainSerializer,
    FlowSerializer,
    ProcessSerializer,
    StockSerializer,
    FlowCreateSerializer,
    FlowChainCreateSerializer
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
    pagination_class = UnlimitedResultsSetPagination

    def get_queryset(self):
        model = self.serializer_class.Meta.model
        return model.objects. \
            select_related('keyflow__casestudy'). \
            select_related('publication'). \
            select_related("origin"). \
            prefetch_related("composition__fractions"). \
            all().defer(
            "keyflow__note",
            "keyflow__casestudy__geom",
            "keyflow__casestudy__focusarea"). \
            order_by('id')


class StockViewSet(StockViewSetAbstract):
    add_perm = 'asfma.add_stock'
    change_perm = 'asmfa.change_stock'
    delete_perm = 'asmfa.delete_stock'
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class ProcessViewSet(ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
