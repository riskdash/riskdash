import numpy as np
import math
import pickle
import collections
from apps.dashboard.models import Qstatswithpvals

if __name__ == '__main__':
    Nameoutput = open('Aggregator/statistics/Qstatistic.pkl', 'rb')
    qValDict = pickle.load(Nameoutput)
    qValDict = collections.OrderedDict(sorted(qValDict.items()))
    for k in qValDict:
    	print "Key = " + str(k)
    	#print "Value = " + str(qValDict[k])
        pvals = qValDict[k][0]
        counter = 0
        for p in pvals:
            if p < 0.05:
                counter = counter + 1
        print "Count = " + str(counter)
        point = Qstatswithpvals(date=k.strftime("%Y-%m-%d"),val=counter)
        point.save()
    print Qstatswithpvals.objects.all()