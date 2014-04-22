import numpy as np
import pickle
from apps.dashboard.models import GrangerRan

if __name__ == '__main__':
    Nameoutput = open('Aggregator/statistics/GrangerPrecomputed.pkl', 'rb')
    preCalcDict = pickle.load(Nameoutput)
    for k in preCalcDict:
        #print "Date: " + str(k)
        #print k.strftime("%m/%Y")
        (names, p_values) = preCalcDict[k]
        #print p_values
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
        #print "JSON Dictionary: "  + str(dict_list)

        entry = GrangerRan(date=k.strftime("%m/%Y"),imports=dict_list)
        entry.save()
    print GrangerRan.objects.all()


