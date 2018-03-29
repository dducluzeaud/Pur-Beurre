from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^search/$', views.search, name='search'),
	url(r'^(?P<id_product>[0-9]+)/$', views.detail, name='detail')
]
