from django.utils.translation import ugettext as _
import numpy as np

from repair.apps.utils.serializers import (BulkSerializerMixin,
                                           BulkResult,
                                           Reference,
                                           ValidationError,
                                           ErrorMask)
from repair.apps.asmfa.serializers import (ActivityGroupSerializer,
                                           ActivitySerializer,
                                           ActorSerializer,
                                           Actor2ActorSerializer,
                                           ActorStockSerializer,
                                           LocationSerializer,
                                           WasteSerializer,
                                           MaterialSerializer,
                                           )
from repair.apps.asmfa.models import (KeyflowInCasestudy,
                                      ActivityGroup,
                                      Activity,
                                      Actor,
                                      Actor2Actor,
                                      ActorStock,
                                      Location,
                                      Material,
                                      Waste,
                                      Process
                                      )
from repair.apps.publications.models import PublicationInCasestudy


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
        'BvDid': 'BvDid',
        'name': 'name',
        'code': 'consCode',
        'year': 'year',
        'description english': 'description_eng',
        'description original': 'description',
        'BvDii': 'BvDii',
        'website': 'website',
        'employees': 'employees',
        'turnover': 'turnover',
        'nace': Reference(
            name='activity',
            referenced_field='nace',
            referenced_model=Activity,
            regex='[0-9]+',
            filter_args={'activitygroup__keyflow': '@keyflow'}
        )
    }
    index_columns = ['BvDid']

    def get_queryset(self):
        return Actor.objects.filter(
            activity__activitygroup__keyflow=self.keyflow)


class Actor2ActorCreateSerializer(BulkSerializerMixin,
                                  Actor2ActorSerializer):

    field_map = {
        'origin': Reference(name='origin',
                            referenced_field='BvDid',
                            referenced_model=Actor,
                            filter_args={
                                'activity__activitygroup__keyflow':
                                '@keyflow'}),
        'destination': Reference(name='destination',
                                 referenced_field='BvDid',
                                 referenced_model=Actor,
                                 filter_args={
                                     'activity__activitygroup__keyflow':
                                     '@keyflow'}),
        'source': Reference(name='publication',
                            referenced_field='publication__citekey',
                            referenced_model=PublicationInCasestudy),
        'process': Reference(name='process', referenced_field='name',
                             referenced_model=Process,
                             allow_null=True),
        'waste': 'waste',
        'amount': 'amount',
        'year': 'year'
    }
    index_columns = ['origin', 'destination', 'composition']

    def get_queryset(self):
        return Actor2Actor.objects.filter(keyflow=self.keyflow)

    def validate(self, attrs):
        if 'dataframe' in attrs:
            df = attrs['dataframe']
            self_ref = df['origin'] == df['destination']

            if self_ref.sum() > 0:
                message = _("Flows from an actor to itself are not allowed.")
                error_mask = ErrorMask(df)
                error_mask.set_error(df.index[self_ref], 'destination', message)
                fn, url = error_mask.to_file(
                    file_type=self.input_file_ext.replace('.', ''),
                    encoding=self.encoding
                )
                raise ValidationError(
                    error_mask.messages, url
                )
        return super().validate(attrs)

    def _create_models(self, df):
        created = super()._create_models(df)
        # trigger conversion to fraction flow
        for model in created:
            model.save()
        return created


class ActorStockCreateSerializer(BulkSerializerMixin,
                                 ActorStockSerializer):

    field_map = {
        'origin': Reference(name='origin',
                            referenced_field='BvDid',
                            referenced_model=Actor,
                            filter_args={
                                'activity__activitygroup__keyflow':
                                '@keyflow'}),
        'source': Reference(name='publication',
                            referenced_field='publication__citekey',
                            referenced_model=PublicationInCasestudy),
        'amount': 'amount',
        'year': 'year',
        'waste': 'waste'
    }
    index_columns = ['origin', 'composition']

    def get_queryset(self):
        return ActorStock.objects.filter(keyflow=self.keyflow)

    def _create_models(self, df):
        created = super()._create_models(df)
        # trigger conversion to fraction flow
        for model in created:
            model.save()
        return created


class AdminLocationCreateSerializer(
    BulkSerializerMixin, LocationSerializer):

    field_map = {
        'BvDid': Reference(name='actor',
                           referenced_field='BvDid',
                           referenced_model=Actor,
                           filter_args={
                               'activity__activitygroup__keyflow':
                               '@keyflow'}),
        'Postcode': 'postcode',
        'Address': 'address',
        'City': 'city',
        'WKT': 'geom'
    }
    index_columns = ['BvDid']

    def get_queryset(self):
        return Location.objects.filter(
            actor__activity__activitygroup__keyflow=self.keyflow)


class MaterialCreateSerializer(BulkSerializerMixin, MaterialSerializer):
    field_map = {
        'parent': Reference(name='parent',
                            referenced_field='name',
                            referenced_model=Material,
                            allow_null=True),
        'name': 'name',
    }
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
        'name': 'name',
        'nace': 'nace',
        #'ewc':
        #'hazardous',
        #'Item_descr': ''
    }
    index_columns = ['name']

    def get_queryset(self):
        return Waste.objects.filter(keyflow=self.keyflow)
