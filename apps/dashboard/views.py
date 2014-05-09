import json
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from apps.dashboard.models import SumStatistics, CumRF, GrangerCausalityConn, GrangerRan, Qstatswithpvals, AggIlliq, B1Months

def returns_stats(request):	
	stats = SumStatistics.objects.all()
	cleaned_stats = [None] * 9
	for s in stats:
		s.ann_mean = round(s.ann_mean,2)
		s.ann_sd = round(s.ann_sd,2)
		s.minimum = round(s.minimum,2)
		s.maximum = round(s.maximum,2)
		s.median = round(s.median,2)
		s.skewness = round(s.skewness,2)
		s.kurtosis = round(s.kurtosis,2)
		s.p1 = round(s.p1, 2)
		s.p1_value = round(s.p1_value,2)
		s.p2 = round(s.p2, 2)
		s.p2_value = round(s.p2_value,2)
		s.p3 = round(s.p3, 2)
		s.p3_value = round(s.p3_value,2)
		if s.sector == "banks":
			s.sector = "Banks"
			cleaned_stats[0] = s
		elif s.sector == "brokers":
			s.sector = "Brokers"
			cleaned_stats[1] = s
		elif s.sector == "insurers":
			s.sector = "Insurers"
			cleaned_stats[2] = s
		elif s.sector == "Hedge Fund Index":
			cleaned_stats[3] = s
		elif s.sector == "Global Macro Hedge Fund Index":
			cleaned_stats[4] = s
		elif s.sector == "Long/Short Equity Hedge Fund Index":
			cleaned_stats[5] = s
		elif s.sector == "liquid":
			s.sector = "Liquid Hedge Funds"
			cleaned_stats[6] = s
		elif s.sector == "illiquid":
			s.sector = "Illiquid Hedge Funds"
			cleaned_stats[7] = s
		elif s.sector == "SP500":
			cleaned_stats[8] = s
	return render_to_response('dashboard/returns.html', {'stats': cleaned_stats}, context_instance=RequestContext(request))

def crf_data(request):
	points = CumRF.objects.all()
	data = [ {'date': p.date, 'price': p.frac} for p in points]

	return HttpResponse(json.dumps(data), mimetype='application/json')

def granger_data(request):
	date = request.GET['date']
	lines = GrangerRan.objects.get(date=date)
	return HttpResponse(json.dumps(lines.imports), mimetype='application/json')

def qstats_data(request):
	points = Qstatswithpvals.objects.all()
	data = [ {'date': p.date, 'price': p.val} for p in points]

	return HttpResponse(json.dumps(data), mimetype='application/json')

def aggIlliq_data(request):
	points = AggIlliq.objects.all()
	data = [ {'date': p.date, 'price': p.val} for p in points]

	return HttpResponse(json.dumps(data), mimetype='application/json')

def B1Months_data(request):
	points = B1Months.objects.all()
	data = [ {'date': p.date, 'price': p.val} for p in points]

	return HttpResponse(json.dumps(data), mimetype='application/json')