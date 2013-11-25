from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='dashboard/index.html')),
	url(r'granger/$', TemplateView.as_view(template_name='dashboard/granger.html')),
	url(r'about/$', TemplateView.as_view(template_name='dashboard/about.html')),
)
