from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from enum import Enum
from enumfields import EnumIntegerField

from repair.apps.login.models import GDSEModel
from repair.apps.asmfa.models import Material, KeyflowInCasestudy
from repair.apps.statusquo.models.indicators import NodeLevel, FlowType, TriState
from repair.apps.studyarea.models import Area, AdminLevels


class Direction(Enum):
    BOTH = 1
    FROM = 2
    TO = 3

class Role(Enum):
    PRODUCTION = 1
    COLLECTION = 2
    TREATMENT = 3

class Year(Enum):
    ALL = 1
    Y13 = 2
    Y14 = 3
    Y15 = 4
    Y16 = 5
    Y17 = 6
    Y18 = 7


class FlowFilter(GDSEModel):
    '''
    predefined filters for rendering flows in workshop mode
    '''
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    keyflow = models.ForeignKey(KeyflowInCasestudy, on_delete=models.CASCADE)
    filter_level = EnumIntegerField(
        enum=NodeLevel, default=NodeLevel.ACTIVITYGROUP)
    node_ids = models.TextField(
        validators=[validate_comma_separated_integer_list],
        blank=True, null=True)
    material = models.ForeignKey(Material,
                                 on_delete=models.SET_NULL,
                                 null=True)
    direction = EnumIntegerField(
        enum=Direction, default=Direction.BOTH)
    flow_type = EnumIntegerField(
        enum=FlowType, default=FlowType.FLOW)
    process_ids = models.TextField(
        validators=[validate_comma_separated_integer_list],
        blank=True, null=True)
    hazardous = EnumIntegerField(
        enum=TriState, default=TriState.BOTH)
    area_level = models.ForeignKey(AdminLevels,
                                   on_delete=models.SET_NULL,
                                   null=True)
    areas = models.ManyToManyField(Area, blank=True)

    role = EnumIntegerField(enum=Role, default=Role.PRODUCTION)
    waste_ids = models.TextField(
        validators=[validate_comma_separated_integer_list],
        blank=True, null=True
    )
    route = EnumIntegerField(enum=TriState, default=TriState.BOTH)
    collector = EnumIntegerField(enum=TriState, default=TriState.BOTH)
    clean = EnumIntegerField(enum=TriState, default=TriState.BOTH)
    mixed = EnumIntegerField(enum=TriState, default=TriState.BOTH)
    year = EnumIntegerField(enum=Year, default=Year.ALL)

