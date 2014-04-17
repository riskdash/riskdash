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
    		if p_values[i][j] < 0.05:
    			full_string = ""
    			if j < 25:
    				full_string = "root.bank."
    			elif j >= 25 and j < 50:
    				full_string = "root.broker."
    			elif j >= 50 and j < 75:
    				full_string = "root.insurer."
    			else:
    				full_string = "root.hfund."
    			imports.append(full_string + str(names[j][0]))
    			#print "Imports: " + str(names[j][0])

		full_string = ""
		if i < 25:
			full_string = "root.bank."
		elif i >= 25 and i < 50:
			full_string = "root.broker."
		elif i >= 50 and i < 75:
			full_string = "root.insurer."
		else:
			full_string = "root.hfund."
    	firm_dict["name"] = full_string + str(names[i][0])
    	firm_dict["size"] = 90;
    	firm_dict["imports"] = imports;
    	#print str(firm_dict)
    	dict_list.append(firm_dict)
    line = GrangerCausalityConn(imports=dict_list)
    #print "Line: " + str(line)
    line.save()
    print GrangerCausalityConn.objects.all()
