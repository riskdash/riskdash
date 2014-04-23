import numpy as np
import math
import pickle
import collections
from apps.dashboard.models import LiqQStat

if __name__ == '__main__':
    Nameoutput = open('Aggregator/statistics/Qstatistic.pkl', 'rb')
    qValDict = pickle.load(Nameoutput)
    qValDict = collections.OrderedDict(sorted(qValDict.items()))
    for k in qValDict:
    	print "Key = " + str(k)
    	#print "Value = " + str(qValDict[k])
    	check = True
    	for val in qValDict[k][1]:
    		if math.isnan(val):
    			check = False
    	#if check and len(qValDict[k][1]) > 0:
    		#print "Average = " + str(np.mean(qValDict[k][1]))
    		#print "Values = " + str(qValDict[k][1])
	    	#point = LiqQStat(date=k.strftime("%Y-%m-%d"),val=np.mean(qValDict[k][1]))
	    	#point.save()
	#print LiqQStat.objects.all()