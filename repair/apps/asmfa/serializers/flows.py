from repair.apps.asmfa.models import (Flow,
                                      FlowChain,
                                      Stock,
                                      Process,
                                      MaterialInChain,
                                      ProductInChain,
                                      CompositeInChain,
                                      Classification,
                                      ExtraDescription,
                                      Material
                                      )
from rest_framework import serializers
from repair.apps.login.serializers import (NestedHyperlinkedModelSerializer,
                                           IDRelatedField,)
from repair.apps.asmfa.serializers.keyflows import (KeyflowInCasestudyField,
                                                    KeyflowInCasestudyDetailCreateMixin,
                                                    MaterialListSerializer,
                                                    ProductListSerializer,
                                                    CompositeListSerializer)


class FlowChainSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'keyflow__casestudy__id',
        'keyflow_pk': 'keyflow__id',
    }
    keyflow = KeyflowInCasestudyField(view_name='keyflowincasestudy-detail',
                                      read_only=True)
    process = IDRelatedField(allow_null=True)
    waste = IDRelatedField(allow_null=True)
    materials = MaterialListSerializer(read_only=True, many=True)
    products = ProductListSerializer(read_only=True, many=True)
    composites = CompositeListSerializer(read_only=True, many=True)

    class Meta:
        model = FlowChain
        fields = ('id', 'identifier', 'keyflow', 'description',
                  'amount', 'year', 'collector', 'route', 'trips',
                  'process', 'waste', 'materials', 'products', 'composites')


class FlowSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'flowchain__keyflow__casestudy__id',
        'keyflow_pk': 'flowchain__keyflow__id'
    }
    keyflow = KeyflowInCasestudyField(view_name='keyflowincasestudy-detail',
                                      read_only=True)
    origin = IDRelatedField(allow_null=True, required=False)
    destination = IDRelatedField(allow_null=True, required=False)

    # Inherited from flowchain
    collector = serializers.BooleanField(source='flowchain.collector',
                                         allow_null=True,
                                         required=False)
    route = serializers.BooleanField(source='flowchain.route',
                                     allow_null=True,
                                     required=False)
    trips = serializers.IntegerField(source='flowchain.trips',
                                     allow_null=True,
                                     required=False)
    amount = serializers.FloatField(source='flowchain.amount',
                                    allow_null=True,
                                    required=False)
    year = serializers.IntegerField(source='flowchain.year',
                                    allow_null=True,
                                    required=False)

    process = serializers.IntegerField(source='flowchain.process.id',
                                       allow_null=True,
                                       required=False)
    waste = serializers.IntegerField(source='flowchain.waste.id',
                                     allow_null=True,
                                     required=False)

    materials = MaterialListSerializer(source='flowchain.materials',
                                       many=True)
    products = ProductListSerializer(source='flowchain.products',
                                     many=True)
    composites = CompositeListSerializer(source='flowchain.composites',
                                         many=True)

    class Meta:
        model = Flow
        fields = ('id', 'keyflow',
                  'origin', 'origin_role',
                  'destination', 'destination_role',
                  'collector',
                  'route',
                  'trips',
                  'amount',
                  'year',
                  'process',
                  'waste',
                  'materials',
                  'products',
                  'composites')


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
                  'clean', 'mixed', 'direct_use', 'product', 'composition')


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


