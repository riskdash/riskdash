from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='dashboard/index.html')),
	url(r'granger/$', TemplateView.as_view(template_name='dashboard/granger.html')),
	url(r'about/$', TemplateView.as_view(template_name='dashboard/about.html')),
	url(r'contact/$', TemplateView.as_view(template_name='dashboard/contact.html')),
	url(r'pca/$', TemplateView.as_view(template_name='dashboard/pca.html')),
	url(r'returns/$', TemplateView.as_view(template_name='dashboard/returns.html')),
)
