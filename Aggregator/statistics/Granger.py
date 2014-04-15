'''
Created on Mar 27, 2014

@author: Hanwen Xu
'''

import MySQLdb
import numpy as np
import pickle
import datetime as dt
from HacRegression import HAC_Regression
from DatabaseFiller.DatabaseTools import addMonths
'''
Get the tickers of all the companies we want to analyze with Granger Causality for a given date

input:
aDate:  datetime object
'''
def getNames(aDate):
    db = MySQLdb.connect(host = "18.189.124.217", port = 3306, user = "guest", passwd = "guest123", db = "rawdata")
    cursor = db.cursor()
    
    TABLENAMES = ['brokers', 'banks', 'insurers', 'hedgefunds']
    
    cYear = int(aDate.strftime('%Y'))
    cMonth = int(aDate.strftime('%m'))
    window = 36
    
    bDate = addMonths(aDate, -1*window-1)
    
    
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
            print len(nameResults)
            for i in xrange(window):
                if i>=len(nameResults)-1:
                    RORdata.append(0)
                elif t=='hedgefunds':
                    RORdata.append(round(nameResults[i][0], 5))
                else:
                    NAV = float(nameResults[i][0])
                    NAV2 = float(nameResults[i+1][0])
                    ROR = 100.0*(NAV2-NAV)/NAV
                    RORdata.append(round(ROR, 5))
            RORdata.reverse()
            dataArray.append(RORdata[1:])
    npDArray = dataArray
    npNArray = nameArray
    #print npDArray
    Dataoutput = open('GrangerData.pkl', 'wb')
    Nameoutput = open('GrangerNames.pkl', 'wb')
    pickle.dump(npDArray, Dataoutput)
    pickle.dump(npNArray, Nameoutput)
    db.close()
    return npNArray, npDArray

'''
return a matrix with p-values of granger causality metrics
Each X value will be the input instituion returns, Y is the output

'''
def grangerCausality(npNArray, npDArray):
    
    p_values = []
    for i, Xraw in enumerate(npDArray):
        #print i, Xraw
        row_pvalues = []
        for j, Yraw in enumerate(npDArray):
            if i!=j:
                #form the response in the regression equation
                y = np.array(Yraw[1:])
                #form the regressors
                X1 = np.array([Xraw[:-1], Yraw[:-1]])
                X = X1.T
                #print X, y
                try:
                    olsModel, V_hat = HAC_Regression(y, X, 0.1)
                    if i==1 and j==2:
                        olsModel.summary()
                    row_pvalues.append(olsModel.p[1])
                except:
                    print "position %d and %d have a singular matrix"%(i, j)
                    row_pvalues.append(1)
            else:
                row_pvalues.append(1)
        p_values.append(row_pvalues)
            #perform heteroscedastic and autocorrelation consistent regression
    p_values = np.array(p_values)
    return p_values

  
if __name__ == '__main__':
    #pullSummarizedStatistics()
    #genRollAutocorr()
    #aDate = dt.datetime(2013, 12, 1)
    #getNames(aDate)
    Dataoutput = open('GrangerData.pkl', 'rb')
    Nameoutput = open('GrangerNames.pkl', 'rb')
    npNArray = pickle.load(Nameoutput)
    npDArray = pickle.load(Dataoutput)
    p_value_matrix = grangerCausality(npNArray, npDArray)
    print p_value_matrix[1][2]