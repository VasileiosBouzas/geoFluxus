from rest_framework_nested.routers import (NestedSimpleRouter, DefaultRouter,
                                           NestedDefaultRouter)
from rest_framework.documentation import include_docs_urls

from django.conf.urls import url, include

from repair.apps.login import views as login_views
from repair.apps.studyarea.views import (
    StakeholderCategoryViewSet,
    StakeholderViewSet,
    AdminLevelViewSet,
    AreaViewSet,
    AreaInLevelViewSet,
    LayerCategoryViewSet,
    LayerViewSet,
    ChartCategoryViewSet,
    ChartViewSet
)

from repair.apps.changes.views import (
    SolutionCategoryViewSet,
    SolutionViewSet,
    StrategyViewSet,
    SolutionInStrategyViewSet,
    ImplementationQuestionViewSet,
    PossibleImplementationAreaViewSet,
    SolutionPartViewSet
)

from repair.apps.asmfa.views import (
    FlowViewSet,
    FlowChainViewSet,
    FilterFlowChainViewSet,
    ActivityGroupViewSet,
    ActivityViewSet,
    ActorViewSet,
    FilterFlowViewSet,
    KeyflowViewSet,
    KeyflowInCasestudyViewSet,
    AdministrativeLocationViewSet,
    AdministrativeLocationOfActorViewSet,
    MaterialViewSet,
    AllWasteViewSet,
    AllMaterialViewSet,
    WasteViewSet,
    ProcessViewSet,
    StockViewSet,
    ClassificationViewSet,
    ExtraDescriptionViewSet
)

from repair.apps.statusquo.views import (
    AimViewSet,
    UserObjectiveViewSet,
    ChallengeViewSet,
    FlowTargetViewSet,
    SustainabilityFieldViewSet,
    ImpactcategoryViewSet,
    ImpactCategoryInSustainabilityViewSet,
    AreaOfProtectionViewSet,
    TargetValueViewSet,
    TargetSpatialReferenceViewSet,
    FlowIndicatorViewSet,
    FlowFilterViewSet
)

from repair.apps.conclusions.views import (ConclusionViewSet, SectionViewSet,
                                           ConsensusViewSet)

from repair.apps.utils.views import PublicationView
from repair.apps.publications.views import (PublicationInCasestudyViewSet,)
from repair.apps.wmsresources.views import (WMSResourceInCasestudyViewSet, )


## base routes ##

router = DefaultRouter()
router.register(r'casestudies', login_views.CaseStudyViewSet)
router.register(r'keyflows', KeyflowViewSet)
router.register(r'wastes', AllWasteViewSet)
router.register(r'materials', AllMaterialViewSet)
router.register(r'publications', PublicationView)
# router.register(r'sustainabilities', SustainabilityFieldViewSet)
# router.register(r'impactcategories', ImpactcategoryViewSet)
# router.register(r'targetvalues', TargetValueViewSet)
# router.register(r'targetspecialreference', TargetSpatialReferenceViewSet)
# router.register(r'areasofprotection', AreaOfProtectionViewSet)
router.register(r'processes', ProcessViewSet)

## nested routes (see https://github.com/alanjds/drf-nested-routers) ##
# / sustainabilities/../
# sus_router = NestedDefaultRouter(router, r'sustainabilities',
#                                  lookup='sustainability')
# sus_router.register(r'areasofprotection', AreaOfProtectionViewSet)
# sus_router.register(r'impactcategories', ImpactCategoryInSustainabilityViewSet)

# /casestudies/...
cs_router = NestedDefaultRouter(router, r'casestudies', lookup='casestudy')
cs_router.register(r'users', login_views.UserInCasestudyViewSet)
cs_router.register(r'stakeholdercategories', StakeholderCategoryViewSet)
cs_router.register(r'chartcategories', ChartCategoryViewSet)
cs_router.register(r'keyflows', KeyflowInCasestudyViewSet)
cs_router.register(r'layercategories', LayerCategoryViewSet)
cs_router.register(r'levels', AdminLevelViewSet)
cs_router.register(r'areas', AreaViewSet)
cs_router.register(r'publications', PublicationInCasestudyViewSet)
cs_router.register(r'aims', AimViewSet)
cs_router.register(r'userobjectives', UserObjectiveViewSet)
cs_router.register(r'challenges', ChallengeViewSet)
cs_router.register(r'wmsresources', WMSResourceInCasestudyViewSet)
cs_router.register(r'sections', SectionViewSet)
cs_router.register(r'consensuslevels', ConsensusViewSet)

# /casestudies/*/userobjectives/...
uo_router = NestedSimpleRouter(cs_router, r'userobjectives',
                               lookup='userobjective')
uo_router.register(r'flowtargets', FlowTargetViewSet)

# /casestudies/*/layercategories/...
layercat_router = NestedSimpleRouter(cs_router, r'layercategories',
                                     lookup='layercategory')
layercat_router.register(r'layers', LayerViewSet)

# /casestudies/*/levels/...
levels_router = NestedSimpleRouter(cs_router, r'levels',
                                 lookup='level')
levels_router.register(r'areas', AreaInLevelViewSet)

# /casestudies/*/chartcategories/...
chart_router = NestedSimpleRouter(cs_router, r'chartcategories',
                                  lookup='chartcategory')
chart_router.register(r'charts', ChartViewSet)

# /casestudies/*/stakeholdercategories/...
shcat_router = NestedSimpleRouter(cs_router, r'stakeholdercategories',
                                  lookup='stakeholdercategory')
shcat_router.register(r'stakeholders', StakeholderViewSet)

# /casestudies/*/keyflows/...
kf_router = NestedSimpleRouter(cs_router, r'keyflows', lookup='keyflow')

kf_router.register(r'wastes', WasteViewSet)
kf_router.register(r'stocks', StockViewSet)
kf_router.register(r'flowchains', FlowChainViewSet)
kf_router.register(r'flows', FlowViewSet)
kf_router.register(r'materials', MaterialViewSet)
kf_router.register(r'activitygroups', ActivityGroupViewSet)
kf_router.register(r'activities', ActivityViewSet)
kf_router.register(r'actors', ActorViewSet)
kf_router.register(r'locations', AdministrativeLocationViewSet)
kf_router.register(r'flowindicators', FlowIndicatorViewSet)
kf_router.register(r'flowfilters', FlowFilterViewSet)
kf_router.register(r'solutioncategories', SolutionCategoryViewSet)
kf_router.register(r'solutions', SolutionViewSet)
kf_router.register(r'strategies', StrategyViewSet)
kf_router.register(r'conclusions', ConclusionViewSet)
kf_router.register(r'classifications', ClassificationViewSet),
kf_router.register(r'extradescriptions', ExtraDescriptionViewSet)

# /casestudies/*/keyflows/*/solutions...
sol_router = NestedSimpleRouter(kf_router, r'solutions',
                                 lookup='solution')
sol_router.register(r'questions', ImplementationQuestionViewSet)
sol_router.register(r'areas', PossibleImplementationAreaViewSet)
sol_router.register(r'parts', SolutionPartViewSet)

# /casestudies/*/keyflows/*/strategies/...
strat_router = NestedSimpleRouter(kf_router, r'strategies',
                                lookup='strategy')
strat_router.register(r'solutions', SolutionInStrategyViewSet)

# /casestudies/*/keyflows/*/actors/...
actors_router = NestedSimpleRouter(kf_router, r'actors',
                                   lookup='actor')
actors_router.register(r'locations', AdministrativeLocationOfActorViewSet)

## webhook ##

url(r'^api/payload', include('repair.static.webhook.urls'))

urlpatterns = [
    url(r'^docs/', include_docs_urls(title='REPAiR API Documentation')),
    url(r'^', include(router.urls)),
    # url(r'^', include(sus_router.urls)),
    url(r'^', include(cs_router.urls)),
    url(r'^', include(shcat_router.urls)),
    url(r'^', include(chart_router.urls)),
    url(r'^', include(sol_router.urls)),
    url(r'^', include(strat_router.urls)),
    url(r'^', include(kf_router.urls)),
    url(r'^', include(actors_router.urls)),
    url(r'^', include(levels_router.urls)),
    url(r'^', include(layercat_router.urls)),
    url(r'^', include(uo_router.urls))
]
