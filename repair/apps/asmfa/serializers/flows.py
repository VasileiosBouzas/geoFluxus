
from django.core.exceptions import ObjectDoesNotExist
from repair.apps.asmfa.models import (
                                      Flow,
                                      Stock,
                                      Process
                                      )
from rest_framework import serializers

from repair.apps.asmfa.models import KeyflowInCasestudy

from repair.apps.login.serializers import (NestedHyperlinkedModelSerializer,
                                           IDRelatedField)

from repair.apps.asmfa.serializers.keyflows import (
    KeyflowInCasestudyField, KeyflowInCasestudyDetailCreateMixin,)

from .nodes import (ActivityGroupField,
                    ActivityField,
                    ActorField)


class CompositionMixin:

    def create(self, validated_data):
        comp_data = validated_data.pop('composition')
        instance = super().create(validated_data)
        validated_data['composition'] = comp_data
        return self.update(instance, validated_data)

    def update(self, instance, validated_data):
        comp_data = validated_data.pop('composition', None)
        if comp_data:
            comp_id = comp_data.get('id')

            # custom composition: no product or waste
            if comp_id is None or comp_id == instance.composition_id:
                # no former compostition
                if instance.composition is None:
                    composition = Composition.objects.create()
                    if 'keyflow_id' in validated_data:
                        composition.keyflow = KeyflowInCasestudy.objects.get(
                            id=validated_data['keyflow_id'])
                    #composition.keyflow = self.request
                # former compostition
                else:
                    composition = instance.composition

                if composition.is_custom:
                    # update the fractions using the CompositionSerializer
                    comp_data['id'] = composition.id
                    composition = CompositionSerializer().update(
                        composition, comp_data)

            # product or waste
            else:
                # take the product or waste-instance as composition
                composition = Composition.objects.get(id=comp_id)

                # if old composition is a custom composition, delete it
                if instance.composition is not None:
                    old_composition = instance.composition
                    if old_composition.is_custom:
                        old_composition.delete()

            # assign the composition to the flow
            instance.composition = composition
        return super().update(instance, validated_data)


class FlowSerializer(CompositionMixin,
                     NestedHyperlinkedModelSerializer):
    """Abstract Base Class for a Flow Serializer"""
    parent_lookup_kwargs = {
        'casestudy_pk': 'keyflow__casestudy__id',
        'keyflow_pk': 'keyflow__id',
    }
    keyflow = KeyflowInCasestudyField(view_name='keyflowincasestudy-detail',
                                      read_only=True)
    publication = IDRelatedField(allow_null=True, required=False)
    process = IDRelatedField(allow_null=True)

    class Meta:
        model = Flow
        fields = ('id', 'amount', 'keyflow', 'origin', 'origin_url',
                  'destination', 'destination_url',
                  'origin_level', 'destination_level',
                  'composition', 'description',
                  'year', 'publication', 'waste', 'process')


class FlowSerializer(CompositionMixin,
                             NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'keyflow__casestudy__id',
        'keyflow_pk': 'keyflow__id',
    }
    keyflow = IDRelatedField()
    publication = IDRelatedField(allow_null=True, required=False)
    process = IDRelatedField(allow_null=True, required=False)
    origin = IDRelatedField()
    destination = IDRelatedField()
    material = IDRelatedField()
    #amount = serializers.DecimalField(max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None, localize=False, rounding=None)

    class Meta(FlowSerializer.Meta):
        model = Flow
        fields = ('id', 'origin', 'destination', 'keyflow', 'material',
                  'amount', 'process', 'nace', 'waste', 'avoidable',
                  'hazardous', 'description', 'year', 'publication')


class StockSerializer(CompositionMixin,
                      NestedHyperlinkedModelSerializer):
    keyflow = KeyflowInCasestudyField(view_name='keyflowincasestudy-detail',
                                      read_only=True)
    publication = IDRelatedField(allow_null=True, required=False)

    parent_lookup_kwargs = {
        'casestudy_pk': 'keyflow__casestudy__id',
        'keyflow_pk': 'keyflow__id',
    }

    class Meta:
        model = Stock
        fields = ('url', 'id', 'origin', 'amount',
                  'keyflow', 'year', 'composition',
                  'publication', 'waste'
                  )


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ('id', 'name')
