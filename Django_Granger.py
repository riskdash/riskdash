import MySQLdb
import numpy as np
import pickle
import datetime as dt
from Aggregator.statistics.HacRegression import HAC_Regression
from Aggregator.DatabaseFiller.DatabaseTools import addMonths
from Aggregator.statistics.Granger import *
from apps.dashboard.models import GrangerCausalityConn

if __name__ == '__main__':
    (names, p_values) = getGCPvalues()
    dict_list = []
    for i in range(0, len(names)):
    	firm_dict = {}
    	imports = []
    	for j in range(0, len(p_values[i])):
    		if p_values[i][j] > 0.8:
    			imports.append(str(names[j][0]))
    			#print "Imports: " + str(names[j][0])
    	firm_dict["name"] = str(names[i][0])
    	firm_dict["size"] = 90;
    	firm_dict["imports"] = imports;
    	#print str(firm_dict)
    	dict_list.append(firm_dict)
    line = GrangerCausalityConn(imports=dict_list)
    #print "Line: " + str(line)
    line.save()
    print GrangerCausalityConn.objects.all()
