from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from repair.apps.asmfa.models import (Actor,
                                      Location)

from repair.apps.login.serializers import NestedHyperlinkedModelSerializer
from repair.apps.studyarea.models import Area

from .nodes import ActorIDField


class PatchFields:

    @property
    def fields(self):
        fields = super().fields
        for fn in ['type', 'geometry', 'properties']:
            if fn not in fields:
                fields[fn] = serializers.CharField(write_only=True,
                                                   required=False)
        return fields


class LocationSerializer(PatchFields,
                         GeoFeatureModelSerializer,
                         NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk':'actor__activity__activitygroup__keyflow__casestudy__id',
        'keyflow_pk':'actor__activity__activitygroup__keyflow__id'
    }
    actor = ActorIDField()
    area = serializers.PrimaryKeyRelatedField(required=False, allow_null=True,
                                              queryset=Area.objects.all())
    level = serializers.PrimaryKeyRelatedField(
        required=False, allow_null=True,
        read_only=True,
    )

    class Meta:
        model = Location
        geo_field = 'geom'
        fields = ['id', 'url', 'address', 'postcode', 'country',
                  'city', 'geom', 'name', 'actor', 'role',
                  'area', 'level']


class LocationsOfActorSerializer(LocationSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk':'actor__activity__activitygroup__keyflow__casestudy__id',
        'keyflow_pk':'actor__activity__activitygroup__keyflow__id',
        'actor_pk': 'actor__id',
    }

    class Meta(LocationSerializer.Meta):
        fields = ['id', 'url', 'address', 'postcode', 'country',
                  'city', 'geom', 'name', 'actor', 'role'
                  'area']

    id = serializers.IntegerField(label='ID', required=False)
    actor = ActorIDField(required=False)

    def create(self, validated_data):
        """Handle Post on Locations"""
        url_pks = self.context['request'].session['url_pks']
        actor_pk = url_pks['actor_pk']
        actor = Actor.objects.get(pk=actor_pk)

        locations = validated_data.get('features', None)

        if locations is None:
            # No Feature Collection: Add Single Location
            validated_data['actor'] = actor
            return super().create(validated_data)
        else:
            # Feature Collection: Add all Locations
            locs = Location.objects.filter(actor=actor)
            # delete existing rows not needed any more
            to_delete = locs.exclude(id__in=(ol.get('id') for ol
                                              in locations
                                              if ol.get('id') is not None))
            to_delete.delete()
            # add or update new locations
            for location in locations:
                loc = Location.objects.update_or_create(
                    actor=actor, id=location.get('id'))[0]

                for attr, value in location.items():
                    setattr(loc, attr, value)
                loc.save()

        # return the last location that was created
        return loc

    def to_internal_value(self, data):
        """
        Override the parent method to parse all features and
        remove the GeoJSON formatting
        """
        if data.get('type') == 'FeatureCollection':
            internal_data_list = list()
            for feature in data.get('features', []):
                if 'properties' in data:
                    feature = self.unformat_geojson(feature)
                internal_data = super().to_internal_value(feature)
                internal_data_list.append(internal_data)

            return {'features': internal_data_list}
        return super().to_internal_value(data)
