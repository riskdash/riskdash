import MySQLdb
import numpy as np
from scipy import stats
from Aggregator.statistics.Autocorrelation import autocorr
import pickle
from Aggregator.statistics.SummaryStatistic import pullSummarizedStatistics
from apps.dashboard.models import SumStatistics

if __name__ == '__main__':
    statistics = pullSummarizedStatistics()
    #print "HERE"
    #print stats
    for k, v in statistics.iteritems():
    	print "Sector: " + k
    	print "Values: " + str(v)
    	stat = SumStatistics(sector=k, sample_size=v[0], ann_mean=v[1], ann_sd=v[2], minimum=v[3],maximum=v[4],median=v[5],skewness=v[6],kurtosis=v[7],p1=v[8],p1_value=v[9],p2=v[10],p2_value=v[11],p3=v[12],p3_value=v[13])
    	stat.save()
   	print SumStatistics.objects.all()
