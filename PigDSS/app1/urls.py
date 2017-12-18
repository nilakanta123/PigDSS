from django.conf.urls import url
from .views import page_one, ajax_request

urlpatterns = [
	url(r'^$', page_one, name='page_one'),
	url(r'^ajax_request/', ajax_request),
]
