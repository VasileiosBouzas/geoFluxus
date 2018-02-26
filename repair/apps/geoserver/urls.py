from django.conf.urls import url, include
from rest_framework_nested.routers import DefaultRouter
from repair.apps.geoserver import views

rest_router = DefaultRouter()
rest_router.register(r'layers', views.GeoserverLayerViewSet,
                     base_name='layers')
urlpatterns = [
    url(r'^$', views.GeoserverIndexView.as_view(), name='index'),
    url(r'^', include(rest_router.urls)), 

    url(r'^ows',
        views.GeoserverOwsView.as_view(),
        name='ows')
]