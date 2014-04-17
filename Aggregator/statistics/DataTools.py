'''
Created on Apr 16, 2014

@author: Hanwen Xu
'''
import MySQLdb
import pickle
from DatabaseFiller.DatabaseTools import addMonths


'''
Get the tickers of all the companies we want to analyze with Granger Causality for a given date

Returns the data of the returns and the names of the companies.  Will create a separate python file with DataTools

input:
aDate:  datetime object
window:  the window of data in months, if window =0, returns the entire 240 month data set

'''
def getNames(aDate, window = 36, bDate = ""):
    db = MySQLdb.connect(host = "18.189.124.217", port = 3306, user = "guest", passwd = "guest123", db = "rawdata")
    cursor = db.cursor()
    
    TABLENAMES = ['brokers', 'banks', 'insurers', 'hedgefunds']
    
    cYear = int(aDate.strftime('%Y'))
    cMonth = int(aDate.strftime('%m'))
    
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
            #print r
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
            #print len(nameResults)
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