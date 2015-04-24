from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/(?P<content>\w+)/$', views.search, name='search'),
    url(r'^login/$', views.login, name='login'),
    url(r'user/$', views.user, name='user'),
    url(r'libadmin/$', views.libadmin, name='libadmin')
]
