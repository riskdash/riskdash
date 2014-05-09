import numpy as np
import math
import pickle
import collections
from apps.dashboard.models import B1Months

if __name__ == '__main__':
    Nameoutput = open('B1defaultsPerMonth.pkl', 'rb')
    arrays = pickle.load(Nameoutput)
    dates = arrays[0]
    vals = arrays[1]
    for i in range(0, len(dates)):
    	print "Key = " + str(dates[i])
    	print "Value = " + str(vals[i])
        new_date = str(dates[i]) + "-01-01"
        print "REAL date = " + new_date
        point = B1Months(date=new_date,val=vals[i])
        point.save()
    print B1Months.objects.all()
    	#check = True
    	#for val in qValDict[k][1]:
    		#if math.isnan(val):
    			#check = False
    	#if math.isnan(qValDict[k]):
    		#pass
    	#else:
    		#print "Average = " + str(np.mean(qValDict[k][1]))
    		#print "Values = " + str(qValDict[k][1])
	    	#point = AggIlliq(date=k.strftime("%Y-%m-%d"),val=qValDict[k])
	    	#point.save()
	#print AggIlliq.objects.all()