from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$',views.dashboard),
    url(r'^admin/', admin.site.urls),
    url(r'^plants/', include('wms.urls')),

]
