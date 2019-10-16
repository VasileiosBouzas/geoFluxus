
from django.utils.translation import ugettext_lazy as _
from django.core.validators import URLValidator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


from repair.apps.asmfa.models import (ActivityGroup,
                                      Activity,
                                      Actor,
                                      Location)

from repair.apps.login.serializers import (NestedHyperlinkedModelSerializer,
                                           InCasestudyField,
                                           IdentityFieldMixin,
                                           CreateWithUserInCasestudyMixin,
                                           IDRelatedField,
                                           DynamicFieldsModelSerializerMixin)


# ActivityGroup Serializers
class ActivityGroupSerializer(CreateWithUserInCasestudyMixin,
                              NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {'casestudy_pk': 'keyflow__casestudy__id',
                            'keyflow_pk': 'keyflow__id', }
    keyflow = IDRelatedField(read_only=True, required=False)
    nace = serializers.ListField(read_only=True, source='nace_codes')
    flow_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ActivityGroup
        fields = ('url', 'id', 'code', 'name',
                  'keyflow', 'nace', 'flow_count')


class ActivityGroupListSerializer(ActivityGroupSerializer):

    class Meta(ActivityGroupSerializer.Meta):
        fields = ('id', 'code', 'name', 'flow_count')


class ActivityGroupField(InCasestudyField):
    parent_lookup_kwargs = {'casestudy_pk': 'keyflow__casestudy__id',
                            'keyflow_pk': 'keyflow__id', }


# Activity serializers
class ActivitySerializer(CreateWithUserInCasestudyMixin,
                         NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'activitygroup__keyflow__casestudy__id',
        'keyflow_pk': 'activitygroup__keyflow__id'
    }
    activitygroup = IDRelatedField()
    activitygroup_url = ActivityGroupField(view_name='activitygroup-detail',
                                           source='activitygroup',
                                           read_only=True)
    activitygroup_name = serializers.CharField(source='activitygroup.name',
                                               read_only=True)
    flow_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Activity
        fields = ('url', 'id', 'nace', 'name', 'activitygroup',
                  'activitygroup_name', 'activitygroup_url', 'flow_count')


class ActivityListSerializer(ActivitySerializer):
    class Meta(ActivitySerializer.Meta):
        fields = ('id', 'name', 'activitygroup', 'activitygroup_name',
                  'nace', 'flow_count')


class ActivityField(InCasestudyField):
    parent_lookup_kwargs = {
        'casestudy_pk':'activitygroup__keyflow__casestudy__id',
        'keyflow_pk': 'activitygroup__keyflow__id',
    }


# Location serializers
class GeolocationInCasestudyField(InCasestudyField):
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id'}


class GeolocationInCasestudySetField(InCasestudyField):
    lookup_url_kwarg = 'casestudy_pk'
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id'}


class GeolocationInCasestudyListField(IdentityFieldMixin,
                                      GeolocationInCasestudySetField):
    """"""
    parent_lookup_kwargs = {'casestudy_pk':
                            'activity__activitygroup__keyflow__casestudy__id'}


class GeolocationInCasestudySet2Field(InCasestudyField):
    lookup_url_kwarg = 'casestudy_pk'
    parent_lookup_kwargs = {'casestudy_pk': 'casestudy__id', }


class GeolocationInCasestudy2ListField(IdentityFieldMixin,
                                       GeolocationInCasestudySet2Field):
    """"""
    parent_lookup_kwargs = {'casestudy_pk':
                            'activity__activitygroup__keyflow__casestudy__id',
                            'actor_pk': 'id', }


class LocationsGeojsonField(GeoFeatureModelSerializer):
    actor = serializers.PrimaryKeyRelatedField(queryset=Actor.objects.all())
    id = serializers.IntegerField(label='ID')

    class Meta:
        model = Location
        geo_field = 'geom'
        fields = ['id', 'address', 'postcode', 'country',
                  'city', 'name', 'actor', 'role']


class URLWithoutProtocolValidator(URLValidator):
    def __call__(self, value):
        if len(value.split('://')) < 2:
            value = 'http://{}'.format(value)
        return super().__call__(value)


class URLFieldWithoutProtocol(serializers.CharField):
    default_error_messages = {'invalid':
                              _('Enter a valid URL (or leave it blank).')}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # add new validator
        validator = URLWithoutProtocolValidator(
            message=self.error_messages['invalid'])
        self.validators.append(validator)


# Actor serializer
class ActorField(InCasestudyField):
    parent_lookup_kwargs = {
        'casestudy_pk': 'activity__activitygroup__keyflow__casestudy__id',
        'keyflow_pk': 'activity__activitygroup__keyflow__id'}


class ActorIDField(serializers.RelatedField):
    default_error_messages = {
        'required': _('This field is required.'),
        'does_not_exist': _('Invalid Actor ID - Object does not exist.'),
        'null': _('This field may not be null.'),
    }

    def to_representation(self, value):
        return value.id

    def to_internal_value(self, data):
        try:
            return Actor.objects.get(id=data)
        except (ObjectDoesNotExist, TypeError, ValueError):
            self.fail('does_not_exist')

    def get_queryset(self):
        qs = Actor.objects.all()
        return qs


class ActorSerializer(DynamicFieldsModelSerializerMixin,
                      CreateWithUserInCasestudyMixin,
                      NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'activity__activitygroup__keyflow__casestudy__id',
        'keyflow_pk': 'activity__activitygroup__keyflow__id',
    }
    activity = IDRelatedField()
    activity_name = serializers.CharField(source='activity.name', read_only=True)
    activitygroup_name = serializers.CharField(source='activity.activitygroup.name', read_only=True)
    activitygroup = serializers.IntegerField(source="activity.activitygroup.id",
                                             read_only=True)
    activity_url = ActivityField(view_name='activity-detail',
                                 source='activity',
                                 read_only=True)
    nace = serializers.CharField(source='activity.nace', read_only=True)
    flow_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Actor
        fields = ('url', 'id', 'identifier', 'name',
                  'activity', 'activity_url', 'activity_name',
                  'activitygroup', 'activitygroup_name',
                  'nace', 'flow_count')


class ActorListSerializer(ActorSerializer):
    class Meta(ActorSerializer.Meta):
        fields = ('id',
                  'activity',  'activity_name',
                  'activitygroup', 'activitygroup_name',
                  'name', 'flow_count')


