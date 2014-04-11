'''
Created on Mar 27, 2014

@author: Hanwen Xu
'''

import MySQLdb
import numpy as np
from scipy import stats
from Autocorrelation import autocorr
import datetime as dt
from DatabaseFiller.DatabaseTools import addMonths
'''
Get the tickers of all the companies we want to analyze with Granger Causality for a given date

input:
aDate:  datetime object
'''
def getNames(aDate):
    db = MySQLdb.connect(host = "127.0.0.1", port = 3306, user = "guest", passwd = "guest123", db = "rawdata")
    cursor = db.cursor()
    
    TABLENAMES = ['brokers', 'banks', 'insurers', 'hedgefunds']
    
    cYear = int(aDate.strftime('%Y'))
    cMonth = int(aDate.strftime('%m'))
    
    bDate = addMonths(aDate, -37)
    
    
    #store the ticker and common name for stocks, 
    #store the hedge fund ID and asset value for hedge funds
    nameArray = []
    #store the past 48 months of return data
    dataArray = []
    
    for t in TABLENAMES:
        print t
        if t!='hedgefunds':
            selectString1 = "select Ticker, CommonName, @curRank := @curRank + 1 as rank "
            orderByString = "order by abs(Price)*SharesOut desc limit 0, 25;"
            selectString2 = "select abs(Price)*SharesOut, Date "
        else:
            selectString1 = "select HFID, AssetValue, @curRank := @curRank + 1 as rank "
            orderByString = "order by AssetValue desc limit 0, 25;"
            selectString2 = "select ROR, Date "
        fromString = "from rawdata.%s b, (select @curRank := 0) r "%(t)
        whereString = "where Year(Date)='%d' and Month(Date)='%d' "%(cYear, cMonth)
        sqlQuery = selectString1+fromString+whereString+orderByString
        cursor.execute(sqlQuery)
        results = cursor.fetchall()
        for r in results:
            print r
            nameArray.append((r[0], r[1]))
            if t=='hedgefunds':
                identifier = "HFID = '%d'"%r[0]
            else:
                identifier = "Ticker = '%s'"%r[0]
            orderByString2 = "order by Date desc;"
            adStr = aDate.strftime('%Y%m%d')
            bdStr = bDate.strftime('%Y%m%d')
            wString1 = "where %s and Date<'%s' and Date>'%s' "%(identifier, adStr, bdStr)
            sqlQuery2 = selectString2+fromString+wString1+orderByString2
            cursor.execute(sqlQuery2)
            nameResults = cursor.fetchall()
            RORdata = []
            
            for i in xrange(36):
                if i>=len(nameResults)-1:
                    RORdata.append(0)
                elif t=='hedgefunds':
                    RORdata.append(nameResults[i][0])
                else:
                    NAV = nameResults[i][0]
                    NAV2 = nameResults[i+1][0]
                    ROR = 100.0*(NAV2-NAV)/NAV
                    RORdata.append(ROR)
            dataArray.append(RORdata)
    npDArray = np.array(dataArray)
    npNArray = np.array(nameArray)
    return npNArray, npDArray

'''
return a matrix with p-values of granger causality metrics
'''
def grangerCausality(npNArray, npDArray):
    
    
    for rowi in npDArray:
        for rowj in npDArray:
            pass
    pass

  
if __name__ == '__main__':
    #pullSummarizedStatistics()
    #genRollAutocorr()
    aDate = dt.datetime(2013, 12, 1)
    getNames(aDate)