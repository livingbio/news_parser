from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.welcome, name='welcome'),
	url(r'^query/(?P<query_type>\w{1,50})$', views.query_api, name='query_api'),
	url(r'^(?P<query_type>\w{1,50})/(?P<id>[0-9]+)/(?P<output_type>\w{1,50})/$', views.basic_view , name='basic_view'),
	
]