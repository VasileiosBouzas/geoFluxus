from rest_framework import serializers
from repair.apps.statusquo.models import (FlowType, NodeLevel, Direction,
                                          FlowFilter, TriState, Year, Role)

from repair.apps.utils.serializers import EnumField
from repair.apps.login.serializers import (IDRelatedField,
                                           NestedHyperlinkedModelSerializer)


class FlowFilterSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'keyflow__casestudy__id',
        'keyflow_pk': 'keyflow__id',
    }
    flow_type = EnumField(enum=FlowType, required=False)
    filter_level = EnumField(enum=NodeLevel, required=False)
    direction = EnumField(enum=Direction, required=False)
    hazardous = EnumField(enum=TriState, required=False)
    material = IDRelatedField(allow_null=True, required=False)
    product = IDRelatedField(allow_null=True, required=False)
    composite = IDRelatedField(allow_null=True, required=False)

    role = EnumField(enum=Role, required=False)
    route = EnumField(enum=TriState, required=False)
    collector = EnumField(enum=TriState, required=False)
    clean = EnumField(enum=TriState, required=False)
    mixed = EnumField(enum=TriState, required=False)
    direct = EnumField(enum=TriState, required=False)
    year = EnumField(enum=Year, required= False)

    class Meta:
        model = FlowFilter
        fields = ('id',
                  'name',
                  'description',
                  'direction',
                  'material',
                  'product',
                  'composite',
                  'area_level',
                  'areas',
                  'flow_type',
                  'filter_level',
                  'node_ids',
                  'process_ids',
                  'hazardous',
                  'role',
                  'waste_ids',
                  'route',
                  'collector',
                  'clean',
                  'mixed',
                  'direct',
                  'year')
