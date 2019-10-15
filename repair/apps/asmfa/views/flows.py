# API View
from abc import ABC
from repair.apps.asmfa.views import UnlimitedResultsSetPagination

from rest_framework.viewsets import ModelViewSet
from reversion.views import RevisionMixin

from repair.apps.utils.views import (CasestudyViewSetMixin,
                                     ModelPermissionViewSet,
                                     PostGetViewMixin)


from repair.apps.asmfa.models import (
    Flow,
    Location,
    Material,
    Actor,
    Activity,
    ActivityGroup,
    Process
)

from repair.apps.studyarea.models import (
    Area, AdminLevels
)

from repair.apps.asmfa.serializers import (
    FlowSerializer,
    ProcessSerializer
)


class FlowViewSet(RevisionMixin,
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


class StockViewSet():
    pass

class ProcessViewSet(ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
