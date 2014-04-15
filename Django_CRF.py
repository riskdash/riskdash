import MySQLdb
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from Aggregator.statistics.SummaryStatistic import getIndData
from Aggregator.statistics.PCA import *
from apps.dashboard.models import CumRF

if __name__ == '__main__':
	index_names = ['', 'brokers', 'banks', 'insurers']
	eigVal, eigVec = PCA(index_names)
	data = rollingCumulRiskFrac(index_names)
	for i in range(0, len(data[0])):
		point = CumRF(date=str(data[0][i]),frac=data[1][i])
		point.save()
	print CumRF.objects.all()
