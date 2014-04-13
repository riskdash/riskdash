'''
Created on Mar 22, 2014

@author: Hanwen Xu

this script will get the summarized statistics for the various hedge fund indices, brokers
banks, insurers, and the SP500

We will also analyze individualized hedge fund indices including:
Global macro
Long Short Equity
Illiquid Funds
Liquid Funds
'''

import MySQLdb
import numpy as np
from scipy import stats
from Autocorrelation import autocorr
import pickle

standardIndices = ['SP500', 'brokers', 'banks', 'insurers', 'liquid', 'illiquid']
HFIndices_raw = ['', 'Global Macro ', 'Long/Short Equity ']
IPADDR = "127.0.0.1"

'''
Return a numpy array of sorted DB data for the given column name, sorted by date in chronological order

inputs
ind:  requires to be from the standard or HF indices_raw
colName:  requires to be a column name from the indices table.  Requires to be matching in case

outputs
ROR:  numpy array of the ROR for the index
indNew:  Cleaned index name
'''
def getIndData(ind, colName, aDate="19940101", bDate = "20140101"):
    db = MySQLdb.connect(host = IPADDR, port = 3306, user = "guest", passwd = "guest123", db = "rawdata")
    cursor = db.cursor()
    suffix = "Hedge Fund Index"
    if ind in standardIndices:
        tname = 'indices'
        indNew = ind
    else:
        tname = 'hfindices'
        indNew = ind + suffix
    
    sqlquery1 = "SELECT %s FROM rawdata.%s where IndexID='%s' and Date>'%s' and Date<'%s' order by Date"%(colName, tname, indNew, aDate, bDate)
    cursor.execute(sqlquery1)
    results = cursor.fetchall()
    datalist = []
    for row in results:
        if colName!='Date':
            datalist.append(float(row[0]))
        else:
            datalist.append(row[0])
    data = np.array(datalist)
    # disconnect from server
    db.close()
    return data, indNew

def pullSummarizedStatistics():
    db = MySQLdb.connect(host = IPADDR, port = 3306, user = "guest", passwd = "guest123", db = "rawdata")
    cursor = db.cursor()
    
    rorDataDict = {}
    suffix = "Hedge Fund Index"
    
    for ind in standardIndices+HFIndices_raw:
        ROR, indNew = getIndData(ind, 'ROR')
        rorDataDict[indNew] = ROR
    
    outputDict = {}
    
    for ind in rorDataDict.keys():
        print ind
        #print rorDataDict[ind]
        ror = rorDataDict[ind]
        stats1 =  stats.describe(ror)
        #stats1 is the output defined in scipy.stats.describe.html
        rho_arr = []
        pval_arr = []
        for i in range(1, 4):
            r, p = autocorr(ror, i)
            rho_arr.append(r)
            pval_arr.append(p)
        output = [stats1[0], stats1[2]*12,np.sqrt(12*stats1[3]), stats1[1][0], stats1[1][1], 
                  np.median(ror), stats1[4], stats1[5],
                  rho_arr[0], pval_arr[0],
                  rho_arr[1], pval_arr[1],
                  rho_arr[2], pval_arr[2]]
        outputDict[ind] = output
        print output
    
    Dateoutput = open('SummaryStatistic.pkl', 'wb')
    pickle.dump(outputDict, Dateoutput)
    return outputDict

if __name__ == '__main__':
    pullSummarizedStatistics()

    
    