from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/(?P<content>\w+)/$|search/$', views.search, name='search'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'loginConfirm/$', views.loginConfirm, name='loginConfirm'),
    url(r'libadmin/$', views.libadmin, name='libadmin')
]
