from repair.apps.asmfa.models import (Flow,
                                      FlowChain,
                                      Stock,
                                      Process
                                      )
from rest_framework import serializers
from repair.apps.login.serializers import (NestedHyperlinkedModelSerializer,
                                           IDRelatedField)
from repair.apps.asmfa.serializers.keyflows import (KeyflowInCasestudyField)


class FlowChainSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'keyflow__casestudy__id',
        'keyflow_pk': 'keyflow__id',
    }
    keyflow = KeyflowInCasestudyField(view_name='keyflowincasestudy-detail',
                                      read_only=True)
    publication = IDRelatedField(allow_null=True, required=False)
    process = IDRelatedField(allow_null=True)
    material = IDRelatedField()

    class Meta:
        model = FlowChain
        fields = ('id', 'process', 'route',
                  'collector', 'route', 'trips',
                  'keyflow', 'description', 'amount',
                  'material', 'year', 'waste', 'publication')


class FlowSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'keyflow__casestudy__id',
        'keyflow_pk': 'keyflow__id',
    }
    flowchain = IDRelatedField()
    origin = IDRelatedField()
    destination = IDRelatedField()

    class Meta:
        model = Flow
        fields = ('id', 'flowchain',
                  'origin', 'destination')


class StockSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'keyflow__casestudy__id',
        'keyflow_pk': 'keyflow__id',
    }
    keyflow = KeyflowInCasestudyField(view_name='keyflowincasestudy-detail',
                                      read_only=True)
    publication = IDRelatedField(allow_null=True, required=False)
    material = IDRelatedField()

    class Meta:
        model = Stock
        fields = ('url', 'id', 'amount',
                  'keyflow', 'description', 'year',
                  'material', 'publication')


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ('id', 'name')
