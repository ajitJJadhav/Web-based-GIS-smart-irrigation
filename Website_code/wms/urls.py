from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.plant_list, name='plants_list'),
    url(r'^(?P<pID>\d+)/$', views.plant_detail, name='plant_detail'),
    url(r'^getdata/$',views.grab,name="grab_data"),
    url(r'^getdimensions/$',views.dimensions,name="enter_dimensions"),
    url(r'^getWaterLevel/$',views.waterLevel,name="waterLevel"),
    url(r'^showLocation/$',views.showMap,name="map"),
    url(r'^updateLocation/$',views.changeLocation,name='location-update'),
    url(r'^showTank/$',views.showTank,name="tankDetails"),
]
