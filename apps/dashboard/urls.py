from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from apps.dashboard import views

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='dashboard/index.html')),
	url(r'granger/$', TemplateView.as_view(template_name='dashboard/granger.html')),
	url(r'granger/data/$', views.granger_data),
	url(r'about/$', TemplateView.as_view(template_name='dashboard/about.html')),
	url(r'contact/$', TemplateView.as_view(template_name='dashboard/contact.html')),
	url(r'pca/$', TemplateView.as_view(template_name='dashboard/pca.html')),
	url(r'pca/data/$', views.crf_data),
	url(r'returns/$', views.returns_stats),
	url(r'sercorr/$', TemplateView.as_view(template_name='dashboard/sercorr.html')),
	url(r'sercorr/q-data/$', views.qstats_data),
	url(r'illiq_viz/$', TemplateView.as_view(template_name='dashboard/illiq_viz.html')),
	url(r'illiq_viz/data/$', views.aggIlliq_data),
	url(r'other/$', TemplateView.as_view(template_name='dashboard/other.html')),
	url(r'mems/$', TemplateView.as_view(template_name='dashboard/mems.html')),
	url(r'B1months/$', TemplateView.as_view(template_name='dashboard/B1months.html')),
	url(r'B1months/data/$', views.B1Months_data),
)
