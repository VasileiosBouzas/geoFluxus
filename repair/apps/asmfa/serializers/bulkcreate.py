from repair.apps.utils.serializers import (BulkSerializerMixin,
                                           Reference,)
from repair.apps.asmfa.serializers import (ActivityGroupSerializer,
                                           ActivitySerializer,
                                           ActorSerializer,
                                           LocationSerializer,
                                           WasteSerializer,
                                           MaterialSerializer,
                                           FlowSerializer,
                                           FlowChainSerializer,
                                           StockSerializer,
                                           MaterialInChainSerializer,
                                           ClassificationSerializer,
                                           ExtraDescriptionSerializer
                                           )
from repair.apps.asmfa.models import (ActivityGroup,
                                      Activity,
                                      Actor,
                                      Location,
                                      Material,
                                      Waste,
                                      Flow,
                                      FlowChain,
                                      Process,
                                      PublicationInCasestudy,
                                      Stock,
                                      MaterialInChain,
                                      Classification,
                                      ExtraDescription
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
        return Actor.objects.filter(activity__activitygroup__keyflow=self.keyflow)


class LocationCreateSerializer(BulkSerializerMixin,
                               LocationSerializer):

    field_map = {
        'Identifier': 'identifier',
        'Actor': Reference(name='actor',
                           referenced_field='identifier',
                           referenced_model=Actor,
                           filter_args={'activity__activitygroup__keyflow':
                                        '@keyflow'}),
        'Postcode': 'postcode',
        'Address': 'address',
        'City': 'city',
        'Country': 'country',
        'Role': 'role',
        'WKT': 'geom'
    }
    index_columns = ['identifier']

    def get_queryset(self):
        return Location.objects.filter(actor__activity__activitygroup__keyflow=self.keyflow)


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
    }
    index_columns = ['ewc_code']

    def get_queryset(self):
        return Waste.objects.filter(keyflow=self.keyflow)


class FlowChainCreateSerializer(BulkSerializerMixin,
                                FlowChainSerializer):
    field_map = {
        'identifier': 'identifier',
        'process': Reference(name='process',
                             referenced_field='code',
                             referenced_model=Process),
        'route': 'route',
        'collector': 'collector',
        'description': 'description',
        'amount': 'amount',
        'material': Reference(name='material',
                              referenced_field='name',
                              referenced_model=Material),
        'trips': 'trips',
        'year': 'year',
        'waste': Reference(name='waste',
                          referenced_field='ewc_code',
                          referenced_model=Waste),
        'source': Reference(name='publication',
                            referenced_field='publication_citekey',
                            referenced_model=PublicationInCasestudy)
    }
    index_columns = ['identifier']

    def get_queryset(self):
        return FlowChain.objects.filter(keyflow=self.keyflow)


class FlowCreateSerializer(BulkSerializerMixin,
                           FlowSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'flowchain__keyflow__casestudy__id',
        'keyflow_pk': 'flowchain__keyflow__id',
    }
    field_map = {
        'flowchain': Reference(name='flowchain',
                               referenced_field='identifier',
                               referenced_model=FlowChain),
        'origin': Reference(name='origin',
                            referenced_field='outputs',
                            referenced_model=Location,
                            filter_args={'actor__activity__activitygroup__keyflow':
                                         '@keyflow'}),
        'destination': Reference(name='destination',
                                 referenced_field='inputs',
                                 referenced_model=Location,
                                 filter_args={'actor__activity__activitygroup__keyflow':
                                              '@keyflow'})
    }
    index_columns = ['flowchain', 'origin', 'destination']

    def get_queryset(self):
        return Flow.objects.all(keyflow=self.keyflow)


class StockCreateSerializer(BulkSerializerMixin,
                            StockSerializer):
    field_map = {
        'identifier': 'identifier',
        'origin': Reference(name='origin',
                            referenced_field='origin',
                            referenced_model=Location),
        'material': Reference(name='material',
                              referenced_field='name',
                              referenced_model=Material),
        'amount': 'amount',
        'description': 'description',
        'year': 'year',
        'source': Reference(name='publication',
                            referenced_field='publication_citekey',
                            referenced_model=PublicationInCasestudy)
    }
    index = ['identifier']

    def get_queryset(self):
        return Stock.objects.filter(keyflow=self.keyflow)


class MaterialInChainCreateSerializer(BulkSerializerMixin,
                                      MaterialInChainSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'flowchain__keyflow__casestudy__id',
        'keyflow_pk': 'flowchain__keyflow__id',
    }
    field_map = {
        'material': Reference(name='material',
                              referenced_field='name',
                              referenced_model=Material),
        'flowchain': Reference(name='flowchain',
                               referenced_field='identifier',
                               referenced_model=FlowChain),
    }
    index_columns = ['material', 'flowchain']

    def get_queryset(self):
        return MaterialInChain.objects.all(keyflow=self.keyflow)


class ClassificationCreateSerializer(BulkSerializerMixin,
                                     ClassificationSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'flowchain__keyflow__casestudy__id',
        'keyflow_pk': 'flowchain__keyflow__id',
    }
    field_map = {
        'flowchain': Reference(name='flowchain',
                               referenced_field='identifier',
                               referenced_model=FlowChain),
        'clean': 'clean',
        'mixed': 'mixed',
        'product': 'product',
        'composition': 'composition'
    }
    index_columns = ['flowchain']

    def get_queryset(self):
        return Classification.objects.all(keyflow=self.keyflow)


class ExtraDescriptionCreateSerializer(BulkSerializerMixin,
                                       ExtraDescriptionSerializer):
    parent_lookup_kwargs = {
        'casestudy_pk': 'flowchain__keyflow__casestudy__id',
        'keyflow_pk': 'flowchain__keyflow__id',
    }
    field_map = {
        'flowchain': Reference(name='flowchain',
                               referenced_field='identifier',
                               referenced_model=FlowChain),
        'type': 'type',
        'description': 'description'
    }
    index_columns = ['flowchain']

    def get_queryset(self):
        return ExtraDescription.objects.all(keyflow=self.keyflow)
