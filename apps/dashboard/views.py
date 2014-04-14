from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.dashboard.models import SumStatistics

def returns_stats(request):	
	stats = SumStatistics.objects.all()
	return render_to_response('dashboard/returns.html', {'stats': stats}, context_instance=RequestContext(request))