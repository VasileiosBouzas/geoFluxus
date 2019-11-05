from repair.apps import admin
from reversion_compare.admin import CompareVersionAdmin as VersionAdmin
from django.contrib.gis.admin import GeoModelAdmin
from repair.apps.login.models import (CaseStudy, )
from repair.apps.studyarea.models import (StakeholderCategory,
                                          Stakeholder,
                                          )

from repair.apps.asmfa.models import (Actor,
                                      Activity,
                                      ActivityGroup,
                                      Material,
                                      AdministrativeLocation,
                                      KeyflowInCasestudy,
                                      Flow,
                                      FlowChain,
                                      Stock,
                                      Waste,
                                      Classification,
                                      ExtraDescription
                                      )


@admin.register(CaseStudy)
class CaseStudyAdmin(GeoModelAdmin, VersionAdmin):
    """Versioning of casestudy"""


@admin.register(KeyflowInCasestudy)
class KeyflowInCasestudyAdmin(VersionAdmin):
    """Versioning of KeyflowInCasestudy"""


@admin.register(StakeholderCategory)
class StakeholderCategoryAdmin(VersionAdmin):
    """Versioning of StakeholderCategory"""


@admin.register(Stakeholder)
class StakeholderAdmin(VersionAdmin):
    """Versioning of Stakeholder"""


@admin.register(ActivityGroup)
class ActivityGroupAdmin(VersionAdmin):
    """Versioning of ActivityGroup"""

@admin.register(Activity)
class ActivityAdmin(VersionAdmin):
    """Versioning of Activity"""


@admin.register(Actor)
class ActorAdmin(VersionAdmin):
    """Versioning of Actor"""


@admin.register(Material)
class MaterialAdmin(VersionAdmin):
    """Versioning of Material"""


@admin.register(AdministrativeLocation)
class AdministrativeLocation(VersionAdmin):
    """Versioning of AdministrativeLocation"""


@admin.register(FlowChain)
class FlowChain(VersionAdmin):
    """Versioning of FlowChain"""


@admin.register(Flow)
class Flow(VersionAdmin):
    """Versioning of Flow"""


@admin.register(Stock)
class Stock(VersionAdmin):
    """Versioning of Stock"""

@admin.register(Waste)
class Waste(VersionAdmin):
    """Versioning of Waste"""

@admin.register(Classification)
class Classification(VersionAdmin):
    """Versioning of Classification"""

@admin.register(ExtraDescription)
class ExtraDescription(VersionAdmin):
    """Versioning of ExtraDescription"""
