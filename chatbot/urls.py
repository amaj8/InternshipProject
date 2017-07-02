from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', run_script, name='run_script'),
    # url(r'^display/$', display, name='display'),
]
