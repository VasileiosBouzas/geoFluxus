from repair.apps.asmfa.models import (Flow,
                                      FlowChain,
                                      Stock,
                                      Process,
                                      MaterialInChain,
                                      ProductInChain,
                                      CompositeInChain,
                                      Classification,
                                      ExtraDescription,
                                      )
from rest_framework import serializers
from repair.apps.login.serializers import (NestedHyperlinkedModelSerializer,
                                           IDRelatedField)
from repair.apps.asmfa.serializers.keyflows import (KeyflowInCasestudyField,
                                                    KeyflowInCasestudyDetailCreateMixin)


class FlowChainSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'keyflow__casestudy__id',
        'keyflow_pk': 'keyflow__id',
    }
    keyflow = KeyflowInCasestudyField(view_name='keyflowincasestudy-detail',
                                      read_only=True)
    publication = IDRelatedField(allow_null=True, required=False)
    process = IDRelatedField(allow_null=True)

    class Meta:
        model = FlowChain
        fields = ('id', 'identifier', 'process', 'route',
                  'collector', 'route', 'trips',
                  'keyflow', 'description', 'amount',
                  'year', 'waste', 'publication')


class FlowSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'flowchain__keyflow__casestudy__id',
        'keyflow_pk': 'flowchain__keyflow__id'
    }
    keyflow = KeyflowInCasestudyField(view_name='keyflowincasestudy-detail',
                                      read_only=True)
    flowchain = IDRelatedField()
    origin = IDRelatedField()
    destination = IDRelatedField()

    class Meta:
        model = Flow
        fields = ('id', 'keyflow', 'flowchain',
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
    origin = IDRelatedField()

    class Meta:
        model = Stock
        fields = ('url', 'id', 'identifier', 'amount',
                  'keyflow', 'origin', 'description', 'year',
                  'material', 'publication')


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ('id', 'code', 'name')


class MaterialInChainSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'flowchain__keyflow__casestudy__id',
        'keyflow_pk': 'flowchain__keyflow__id'
    }
    keyflow = KeyflowInCasestudyField(view_name='keyflowincasestudy-detail',
                                      read_only=True)
    material = IDRelatedField()
    flowchain = IDRelatedField()

    class Meta:
        model = MaterialInChain
        fields = ('url', 'id', 'keyflow',
                  'material', 'flowchain',)

class ProductInChainSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'flowchain__keyflow__casestudy__id',
        'keyflow_pk': 'flowchain__keyflow__id'
    }
    keyflow = KeyflowInCasestudyField(view_name='keyflowincasestudy-detail',
                                      read_only=True)
    product = IDRelatedField()
    flowchain = IDRelatedField()

    class Meta:
        model = ProductInChain
        fields = ('url', 'id', 'keyflow',
                  'product', 'flowchain',)

class CompositeInChainSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'flowchain__keyflow__casestudy__id',
        'keyflow_pk': 'flowchain__keyflow__id'
    }
    keyflow = KeyflowInCasestudyField(view_name='keyflowincasestudy-detail',
                                      read_only=True)
    composite = IDRelatedField()
    flowchain = IDRelatedField()

    class Meta:
        model = CompositeInChain
        fields = ('url', 'id', 'keyflow',
                  'composite', 'flowchain',)


class ClassificationSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'flowchain__keyflow__casestudy__id',
        'keyflow_pk': 'flowchain__keyflow__id'
    }
    keyflow = KeyflowInCasestudyField(view_name='keyflowincasestudy-detail',
                                      read_only=True)
    flowchain = IDRelatedField()

    class Meta:
        model = Classification
        fields = ('url', 'id', 'keyflow', 'flowchain',
                  'clean', 'mixed', 'product', 'composition')


class ExtraDescriptionSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'flowchain__keyflow__casestudy__id',
        'keyflow_pk': 'flowchain__keyflow__id'
    }
    keyflow = KeyflowInCasestudyField(view_name='keyflowincasestudy-detail',
                                      read_only=True)
    flowchain = IDRelatedField()

    class Meta:
        model = ExtraDescription
        fields = ('url', 'id', 'keyflow', 'flowchain',
                  'type', 'description')


