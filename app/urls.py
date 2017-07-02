from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'app'

urlpatterns= [
    url(r'^$',views.HomeView.as_view(),name='home'),
    url(r'^extract$',views.extract,name='extract'),
]
