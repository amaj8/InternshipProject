from django.conf.urls import url
from .views import *
from django.conf.urls import url
from . import views


# app_name = 'app'


urlpatterns = [
    url(r'^$', run_script, name='run_script'),
    url(r'^final_response/$', views.final_response, name='final_response'),
     url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                views.activate, name='activate'),
]
