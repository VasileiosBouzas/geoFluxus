# API View
from reversion.views import RevisionMixin
from repair.apps.asmfa.views import UnlimitedResultsSetPagination

from repair.apps.asmfa.models import (
    Location
)

from repair.apps.asmfa.serializers import (
    LocationSerializer,
    LocationsOfActorSerializer
)

from repair.apps.utils.views import (CasestudyViewSetMixin,
                                     ModelPermissionViewSet,
                                     PostGetViewMixin)


class LocationViewSet(PostGetViewMixin, RevisionMixin,
                                 CasestudyViewSetMixin,
                                 ModelPermissionViewSet):
    pagination_class = UnlimitedResultsSetPagination
    add_perm = 'asmfa.add_location'
    change_perm = 'asmfa.change_location'
    delete_perm = 'asmfa.delete_location'
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        locations = Location.objects.select_related(
            "actor__activity__activitygroup__keyflow__casestudy").all().defer(
                "actor__activity__activitygroup__keyflow__casestudy__geom",
                "actor__activity__activitygroup__keyflow__casestudy__focusarea")
        if (self.isGET):
            if 'actor__in' in self.request.data:
                ids = self.request.data['actor__in'].split(",")
                locations = locations.filter(actor__in=ids)
        return locations.order_by('id')


class LocationsOfActorViewSet(PostGetViewMixin, RevisionMixin,
                                         CasestudyViewSetMixin,
                                         ModelPermissionViewSet):
    pagination_class = UnlimitedResultsSetPagination
    queryset = Location.objects.all()
    serializer_class = LocationsOfActorSerializer

    def get_queryset(self):
        locations = Location.objects.select_related(
            "actor__activity__activitygroup__keyflow__casestudy").all().defer(
                "actor__activity__activitygroup__keyflow__casestudy__geom",
                "actor__activity__activitygroup__keyflow__casestudy__focusarea")
        if (self.isGET):
            if 'actor__in' in self.request.data:
                ids = self.request.data['actor__in'].split(",")
                locations = locations.filter(actor__in=ids)
        return locations.order_by('id')

