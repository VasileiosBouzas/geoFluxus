from repair.apps.utils.serializers import (BulkSerializerMixin,
                                           Reference,)
from repair.apps.asmfa.serializers import (ActivityGroupSerializer,
                                           ActivitySerializer,
                                           ActorSerializer,
                                           LocationSerializer,
                                           WasteSerializer,
                                           MaterialSerializer,
                                           )
from repair.apps.asmfa.models import (ActivityGroup,
                                      Activity,
                                      Actor,
                                      Location,
                                      Material,
                                      Waste,
                                      )


class ActivityGroupCreateSerializer(BulkSerializerMixin,
                                    ActivityGroupSerializer):
    field_map = {
        'code': 'code',
        'name': 'name'
    }
    index_columns = ['code']

    def get_queryset(self):
        return ActivityGroup.objects.filter(keyflow=self.keyflow)


class ActivityCreateSerializer(BulkSerializerMixin,
                               ActivitySerializer):
    field_map = {
        'nace': 'nace',
        'name': 'name',
        'ag': Reference(name='activitygroup',
                        referenced_field='code',
                        referenced_model=ActivityGroup,
                        filter_args={'keyflow': '@keyflow'}),
    }
    index_columns = ['nace']

    def get_queryset(self):
        return Activity.objects.filter(activitygroup__keyflow=self.keyflow)


class ActorCreateSerializer(BulkSerializerMixin,
                            ActorSerializer):

    field_map = {
        'identifier': 'identifier',
        'name': 'name',
        'description english': 'description_eng',
        'description original': 'description',
        'nace': Reference(
            name='activity',
            referenced_field='nace',
            referenced_model=Activity,
            regex='[0-9]+',
            filter_args={'activitygroup__keyflow': '@keyflow'}
        )
    }
    index_columns = ['identifier']

    def get_queryset(self):
        return Actor.objects.filter(
            activity__activitygroup__keyflow=self.keyflow)


class LocationCreateSerializer(
    BulkSerializerMixin, LocationSerializer):

    field_map = {
        'identifier': Reference(name='actor',
                                referenced_field='identifier',
                                referenced_model=Actor,
                                filter_args={'activity__activitygroup__keyflow':
                                             '@keyflow'}),
        'Postcode': 'postcode',
        'Address': 'address',
        'City': 'city',
        'WKT': 'geom'
    }
    index_columns = ['identifier']

    def get_queryset(self):
        return Location.objects.filter(
            actor__activity__activitygroup__keyflow=self.keyflow)


class MaterialCreateSerializer(BulkSerializerMixin, MaterialSerializer):
    field_map = {'name': 'name',}
    index_columns = ['name']

    parent_lookup_kwargs = {
        'casestudy_pk': 'keyflow__casestudy__id',
        'keyflow_pk': 'keyflow__id',
    }

    def get_queryset(self):
        return Material.objects.filter(keyflow=self.keyflow)


class WasteCreateSerializer(BulkSerializerMixin,
                            WasteSerializer):

    parent_lookup_kwargs = {
        'casestudy_pk': 'keyflow__casestudy__id',
        'keyflow_pk': 'keyflow__id',
    }

    field_map = {
        'ewc_code': 'ewc_code',
        'ewc_name': 'ewc_name',
        #'ewc':
        #'hazardous',
        #'Item_descr': ''
    }
    index_columns = ['name']

    def get_queryset(self):
        return Waste.objects.filter(keyflow=self.keyflow)
