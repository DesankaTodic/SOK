from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^ucitavanje/plugin/(?P<id>([a-z]+|[_])+)$', views.ucitavanje_plugin, name="ucitavanje_plugin"),
    url(r'^viz/plugin/(?P<id>([a-z]+|[_])+)$', views.viz_plugin, name="viz_plugin"),
    url(r'^search', views.search, name="search"),
    url(r'^filter', views.filter, name="filter"),

]