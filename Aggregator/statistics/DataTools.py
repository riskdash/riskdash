'''
Created on Apr 16, 2014

@author: Hanwen Xu
'''
import MySQLdb
import pickle
from DatabaseFiller.DatabaseTools import addMonths
IPADDR = "18.189.104.232"


'''
Get the tickers of all the companies we want to analyze with Granger Causality for a given date

Also returns a matrix of returns

Returns the data of the returns and the names of the companies.  Will create a separate python file with DataTools

Default, will return the 36 months of data from the end date.  Optional, provide your own start date

Stocks will have ticker and common name in the name array
Hedge funds will have HFID and asset value. 

input:
endDate:  datetime object
inst:  the names of the institutions
window:  the window of data in months, if window =0, returns the entire 240 month data set
startDate: optional
numcomps:  number of top companies to draw out
'''
def getNames(endDate, inst=['brokers', 'banks', 'insurers', 'hedgefunds'], window = 36, startDate = "", numComps = 25):
    db = MySQLdb.connect(host = IPADDR, port = 3306, user = "guest", passwd = "guest123", db = "rawdata")
    cursor = db.cursor()
    
    TABLENAMES = inst
    
    cYear = int(endDate.strftime('%Y'))
    cMonth = int(endDate.strftime('%m'))
    
    if startDate=="":
        startDate = addMonths(endDate, -1*window-1)
    
    
    #store the ticker and common name for stocks, 
    #store the hedge fund ID and asset value for hedge funds
    nameArray = []
    #store the past 48 months of return data
    dataArray = []
    
    for t in TABLENAMES:
        print t
        if t!='hedgefunds':
            selectString1 = "select Ticker, CommonName, @curRank := @curRank + 1 as rank "
            orderByString = "order by abs(Price)*SharesOut desc limit 0, %d;"%numComps
            selectString2 = "select abs(Price)*SharesOut, Date "
        else:
            selectString1 = "select HFID, AssetValue, @curRank := @curRank + 1 as rank "
            orderByString = "order by AssetValue desc limit 0, %d;"%numComps
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
            adStr = endDate.strftime('%Y%m%d')
            bdStr = startDate.strftime('%Y%m%d')
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
                    if NAV!=0:
                        ROR = 100.0*(NAV2-NAV)/NAV
                    else:
                        ROR= 0.0
                    RORdata.append(round(ROR, 5))
            RORdata.reverse()
            dataArray.append(RORdata[1:])

    '''
    Dataoutput = open('GrangerData.pkl', 'wb')
    Nameoutput = open('GrangerNames.pkl', 'wb')
    pickle.dump(dataArray, Dataoutput)
    pickle.dump(dataArray, Nameoutput)
    '''
    
    db.close()
    return nameArray, dataArray

