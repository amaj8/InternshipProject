from django.conf.urls import url
from .views import *
from django.conf.urls import url
from . import views


# app_name = 'app'


urlpatterns = [
    url(r'^$', run_script, name='run_script'),
    # url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^final_response/$', views.final_response, name='final_response'),
]
