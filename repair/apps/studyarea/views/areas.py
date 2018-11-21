from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions
from django.contrib.gis.db.models.functions import PointOnSurface

from repair.apps.utils.views import (CasestudyViewSetMixin,
                                     ModelPermissionViewSet)

from repair.apps.studyarea.models import (AdminLevels,
                                          Area,
                                          )

from repair.apps.studyarea.serializers import (AdminLevelSerializer,
                                               AreaSerializer,
                                               AreaGeoJsonSerializer,
                                               AreaGeoJsonPostSerializer,
                                               AdminLevelCreateSerializer,
                                               AreaCreateSerializer
                                               )


class AdminLevelViewSet(CasestudyViewSetMixin, ModelPermissionViewSet):
    queryset = AdminLevels.objects.all()
    serializer_class = AdminLevelSerializer
    serializers = {'list': AdminLevelSerializer,
                   'create': AdminLevelCreateSerializer}


class AreaViewSet(CasestudyViewSetMixin, ModelPermissionViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    serializers = {
        'list': AreaSerializer,
        'create': AreaCreateSerializer
    }

    def get_queryset(self):
        model = self.serializer_class.Meta.model
        casestudy_pk = self.kwargs.get('casestudy_pk')
        areas = model.objects.select_related("adminlevel").filter(
            adminlevel__casestudy=casestudy_pk)
        areas = areas.annotate(pnt=PointOnSurface('geom'))
        return areas


class AreaInLevelViewSet(AreaViewSet):
    serializers = {
        'retrieve': AreaGeoJsonSerializer,
        'update': AreaGeoJsonSerializer,
        'partial_update': AreaGeoJsonSerializer,
        'create': AreaGeoJsonPostSerializer
    }

