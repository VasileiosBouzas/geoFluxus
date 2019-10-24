from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from repair.apps.asmfa.graphs.graph import BaseGraph
from repair.apps.login.models import CaseStudy
from repair.apps.asmfa.models import (Keyflow,
                                      KeyflowInCasestudy,
                                      Material,
                                      Waste,
                                      )

from repair.apps.login.serializers import (NestedHyperlinkedModelSerializer,
                                           InCasestudySerializerMixin,
                                           InCasestudyField,
                                           InCasestudyListField,
                                           IdentityFieldMixin,
                                           NestedHyperlinkedRelatedField,
                                           IDRelatedField)


class InCasestudyKeyflowListField(InCasestudyListField):
    """
    Field that returns a list of all items in the keyflow in the casestudy
    """
    lookup_url_kwarg = 'keyflow_pk'
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id',
                            'keyflow_pk': 'id'}


class KeyflowSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {}
    casestudies = serializers.HyperlinkedRelatedField(
        queryset=CaseStudy.objects,
        many=True,
        view_name='casestudy-detail',
        help_text=_('Select the Casestudies the Keyflow is used in')
    )

    class Meta:
        model = Keyflow
        fields = ('url', 'id', 'code', 'name', 'casestudies')

    def update(self, instance, validated_data):
        """update the user-attributes, including profile information"""
        keyflow = instance

        # handle groups
        new_casestudies = validated_data.pop('casestudies', None)
        if new_casestudies is not None:
            ThroughModel = Keyflow.casestudies.through
            casestudy_qs = ThroughModel.objects.filter(
                keyflow=keyflow.id)
            # delete existing groups
            casestudy_qs.exclude(
                casestudy__id__in=(cs.id for cs in new_casestudies)).delete()
            # add or update new groups
            for cs in new_casestudies:
                ThroughModel.objects.update_or_create(keyflow=keyflow,
                                                      casestudy=cs)

        # update other attributes
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def create(self, validated_data):
        """Create a new Keyflow"""
        code = validated_data.pop('code')

        keyflow = Keyflow.objects.create(code=code)
        self.update(instance=keyflow, validated_data=validated_data)
        return keyflow


class InKeyflowField(InCasestudyField):
    parent_lookup_kwargs = {
        'casestudy_pk':
        'keyflow__casestudy__id',
        'keyflow_pk': 'keyflow__id', }
    extra_lookup_kwargs = {}
    filter_field = 'keyflow_pk'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_pks_lookup['keyflow_pk'] = \
            self.parent_lookup_kwargs['keyflow_pk']


class InKeyflowSetField(IdentityFieldMixin, InKeyflowField, ):
    """Field that returns a list of all items in the casestudy"""
    lookup_url_kwarg = 'keyflow_pk'
    parent_lookup_kwargs = {
        'casestudy_pk': 'casestudy__id',
        'keyflow_pk': 'id', }


class KeyflowField(NestedHyperlinkedRelatedField):
    parent_lookup_kwargs = {'pk': 'id'}
    queryset = Keyflow.objects
    """This is fixed in rest_framework_nested, but not yet available on pypi"""
    def use_pk_only_optimization(self):
        return False


class KeyflowInCasestudySerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id'}
    note = serializers.CharField(required=False, allow_blank=True)
    casestudy = IDRelatedField()
    keyflow = IDRelatedField()

    activitygroups = InCasestudyKeyflowListField(view_name='activitygroup-list')
    activities = InCasestudyKeyflowListField(view_name='activity-list')
    actors = InCasestudyKeyflowListField(view_name='actor-list')
    locations = InCasestudyKeyflowListField(view_name='location-list')

    code = serializers.CharField(source='keyflow.code',
                                 allow_blank=True, required=False)
    name = serializers.CharField(source='keyflow.name',
                                 allow_blank=True, required=False)
    graph_date = serializers.SerializerMethodField()

    class Meta:
        model = KeyflowInCasestudy
        fields = ('url',
                  'id',
                  'keyflow',
                  'casestudy',
                  'note',
                  'code',
                  'note',
                  'name',
                  'activitygroups',
                  'activities',
                  'actors',
                  'locations',
                  'graph_date'
                  )

    def get_graph_date(self, obj):
        kfgraph = BaseGraph(obj)
        return kfgraph.date


class KeyflowInCasestudyPostSerializer(InCasestudySerializerMixin,
                                       NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id'}
    note = serializers.CharField(required=False, allow_blank=True)
    keyflow = IDRelatedField()

    class Meta:
        model = KeyflowInCasestudy
        fields = ('keyflow',
                  'note',)


class KeyflowInCasestudyDetailCreateMixin:
    def create(self, validated_data):
        """Create a new solution quantity"""
        url_pks = self.context['request'].session['url_pks']
        keyflow_pk = url_pks['keyflow_pk']
        # ToDo: raise some kind of exception or prevent creating object with
        # wrong keyflow/casestudy combination somewhere else (view.update?)
        # atm the server will just hang up here
        mic = KeyflowInCasestudy.objects.get(id=keyflow_pk)
        validated_data['keyflow'] = mic

        obj = self.Meta.model.objects.create(
            **validated_data)
        return obj


class KeyflowInCasestudyField(InCasestudyField):
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id',}


class WasteSerializer(KeyflowInCasestudyDetailCreateMixin,
                      NestedHyperlinkedModelSerializer):

    class Meta:
        model = Waste
        fields = ('url', 'id',
                  'ewc_code', 'ewc_name', 'hazardous')


class AllMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = ('url', 'id',
                  'name', 'keyflow')


class AllMaterialListSerializer(AllMaterialSerializer):
    class Meta(AllMaterialSerializer.Meta):
        fields = ('id', 'name', 'keyflow')


class MaterialSerializer(KeyflowInCasestudyDetailCreateMixin,
                         AllMaterialSerializer):
    # keyflow filtering is done by "get_queryset"
    parent_lookup_kwargs = {}
    keyflow = IDRelatedField(read_only=True)
    class Meta:
        model = Material
        fields = ('url', 'id',
                  'name', 'keyflow')


class MaterialListSerializer(MaterialSerializer):
    class Meta(MaterialSerializer.Meta):
        fields = ('id', 'name',
                  'keyflow')

