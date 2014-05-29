import calendar
import pytz
from Aggregator.statistics.PCA import rollingCumulRiskFrac, PCA
from apps.dashboard.models import CumRF

def to_utc(dt):
    utc = pytz.timezone('UTC')
    d_utc = utc.localize(dt).astimezone(utc)
    return calendar.timegm(d_utc.utctimetuple()) * 1000

if __name__ == '__main__':
	index_names = ['', 'brokers', 'banks', 'insurers']
	eigVal, eigVec = PCA(index_names)
	data = rollingCumulRiskFrac(index_names)
	for i in range(0, len(data[0])):
		point = CumRF(date=to_utc(data[0][i]),frac=data[1][i])
		point.save()
	print CumRF.objects.all()
