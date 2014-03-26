'''
Created on Dec 8, 2013

@author: Hanwen Xu
'''

import MySQLdb, csv, pickle as pkl
import _mysql_exceptions
import datetime as dt, time, calendar
import locale
import sys
locale.setlocale(locale.LC_TIME  , "usa")

'''
Create the illiquid and liquid strategy entries
'''
#Dictionary of hedge fund index, and their associated estimated weights
LiqHFIndWts = {'Dedicated Short Bias': 0.5, 'Equity Market Neutral':5.0, 'Managed Futures':7.0}
IllHFIndWts = {'Convertible Arbitrage':3.0, 'Emerging Markets': 5.0, 'Event Driven Risk Arbitrage': 20.0, 'Fixed Income Arbitrage':8.0,
               'Managed Futures': 11.0}

def checkDBConnection():
    
    try:
        db = MySQLdb.connect(host = "127.0.0.1", port = 3306, user = "guest", passwd = "guest123", db = "rawdata")
        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
    
        # Fetch a single row using fetchone() method.
        data = cursor.fetchone()
        
        print "Database version : %s " % data
        
        # disconnect from server
        db.close()
        return True
    except:
        return False

def pullHFIndxCSV():
    with open('CS_ALL.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        row = reader.next()
        cleaned_list = [x for x in row if x.strip() is not '']
        #print cleaned_list
        l = len(cleaned_list)
        #print l
        DateList = []
        HFDataDict ={}
        for x in cleaned_list:
            HFDataDict[x] = []
        
        reader.next() #skip a header row
        for row in reader:
            if row[0]=='':
                break
            DateList.append(row[0])
            #print row
            for i in xrange(l):
                (NAV, ROR) = (row[2+3*i], row[3+3*i])
                if ROR=="USD":
                    print reader.line_num, cleaned_list[i]
                    print row[1+3*i]
                HFDataDict[cleaned_list[i]].append((NAV, ROR))
        
        #print HFDataDict[cleaned_list[0]]
        #print DateList
        
        HFoutput = open('HFData.pkl', 'wb')
        Dateoutput = open('DateList.pkl', 'wb')
        pkl.dump(HFDataDict, HFoutput)
        pkl.dump(DateList, Dateoutput)
        

def fillHFIndxDatabase():
    db = MySQLdb.connect(host = "127.0.0.1", port = 3306, user = "guest", passwd = "guest123", db = "rawdata")
    cursor = db.cursor()
    
    HFoutput = open('HFData.pkl', 'rb')
    Dateoutput = open('DateList.pkl', 'rb')
    
    HFDataDict =pkl.load(HFoutput)
    DateList = pkl.load(Dateoutput)
    
    hedgeFunds = HFDataDict.keys()
    cursor.execute("truncate rawdata.hedgefundindices")
    db.commit()
    for HF in hedgeFunds:
        data = HFDataDict[HF]
        for i, x in enumerate(data):
            #print i, x
            #print HF
            Name_raw = HF
            Name = Name_raw.replace("Credit Suisse ", "")
            
            NAV_raw = x[0]
            
            Date_raw = DateList[i]
            date_clean = formatDate(Date_raw)
            
            ROR_raw = x[1]
            ROR = ROR_raw.replace("%", "")
            if ROR=='':
                ROR='0'
            if NAV_raw=='':
                NAV_raw = '0'
            
            try:
                cursor.execute("insert into rawdata.hedgefundindices " + 
                           "Values('%s', '%s', '%s', '%s')"%(Name, date_clean, NAV_raw, ROR))
                db.commit()
            except _mysql_exceptions.OperationalError:
                print (Name, date_clean, NAV_raw, ROR)
                db.rollback()
    db.close()

'''
Return the parsed date
'''
def formatDate(date_raw):
    date = dt.datetime.strptime(date_raw, "%x")
    #print date
    date_clean = date.strftime("%Y-%m-%d")
    return date_clean


'''
Given a CSVfile, database hook, and cursor, update the hedge fund returns
'''
def HFCSVparse(csvfile, db, cursor):
    reader = csv.reader(csvfile)
    reader.next()
    prevAsset = '0'
    rowCount = 0
    for row in reader:
        if rowCount%1000==0:
            print "finished processing %d hedgefund datapoints"%(rowCount)
        rowCount += 1
        if row[0]=='':
            break
        HFID = row[0]
        Date_raw = row[1].split()[0]
        #date_clean = formatDate(Date_raw)
        ROR_raw = row[2]
        NAV_raw = row[3]
        Assets_raw = row[4]
        if Assets_raw =='':
            Assets_raw = prevAsset
        else:
            prevAsset = Assets_raw
        try:
            cursor.execute("insert into rawdata.hedgefunds " + 
                       "Values('%s', '%s', '%s', '%s', '%s')"%(Date_raw, HFID, ROR_raw, NAV_raw, Assets_raw))
            db.commit()
        except _mysql_exceptions.OperationalError:
            print (Date_raw, HFID, ROR_raw, NAV_raw, Assets_raw)
            db.rollback()

def SP500parse(csvfile, db, cursor):
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        if row[0]=='':
            break
        Date_raw = row[0]
        IndexID = row[1]
        #date_clean = formatDate(Date_raw)
        ROR_raw = row[2]
        NAV_raw = row[3]
        ROR = float(ROR_raw)*100
        try:
            cursor.execute("insert into rawdata.indices " + 
                       "Values('%s', '%s', '%s', '%s')"%(Date_raw, IndexID, str(ROR), NAV_raw))
            db.commit()
        except _mysql_exceptions.OperationalError as e:
            print (Date_raw, IndexID, ROR_raw, NAV_raw)
            print e
            db.rollback()


'''
Pull CSV, and insert into database
'''
def pullHFCSV():
    db = MySQLdb.connect(host = "127.0.0.1", port = 3306, user = "guest", passwd = "guest123", db = "rawdata")
    cursor = db.cursor()
    
    cursor.execute("truncate rawdata.hedgefunds")
    db.commit()
    
    with open('GYFund.csv', 'rb') as csvfile:
        HFCSVparse(csvfile, db, cursor)
      
    with open('LiveFund.csv', 'rb') as csvfile:
        HFCSVparse(csvfile, db, cursor)

    db.close()
    

def addMonths(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month/12
    month = month%12 +1
    day = calendar.monthrange(year,month)[1]
    return dt.date(year,month,day)

'''
Get the index WAV of the given table name, date, and cursor to database

if liquid, then use the weighted average of liquid hedge funds
if illiquid, then use the weighted average of illiquid hedge funds
'''
def getWAV(tName, iDate, cursor):
    if 'liquid' not in tName:
        sqlQuery1 = "SELECT sum(abs(Price)*SharesOut) FROM rawdata."+tName+" where Year(Date)='%s' and Month(Date)='%s'"%(iDate.strftime('%Y'), iDate.strftime('%m'))
        try:
            cursor.execute(sqlQuery1)
            results = cursor.fetchall()
            row = results[0]
            WAV = float(row[0])
        except:
            print "Error, unable to fetch data FROM rawdata."+tName+" where Year(Date)='%s' and Month(Date)='%s'"%(iDate.strftime('%Y'), iDate.strftime('%m'))
            WAV = 0
    else:
        WAV = 0.0
        suffix = " Hedge Fund Index"
        if 'liquid'==tName:
            totalWeight = 12.5
            IndWts = LiqHFIndWts
        elif 'illiquid'==tName:
            totalWeight = 47.0
            IndWts = IllHFIndWts
        else:
            return 0
        for hfind in IndWts.keys():
            sqlQuery1 = "SELECT NAV FROM rawdata.hfindices where IndexID='%s' and Year(Date)='%s' and Month(Date)='%s'"%(hfind+suffix, iDate.strftime('%Y'), iDate.strftime('%m'))
            try:
                cursor.execute(sqlQuery1)
                results = cursor.fetchall()
                row = results[0]
                NAV = float(row[0])
                WAV += IndWts[hfind]*NAV/totalWeight
            except:
                print "Error, unable to fetch data where IndexID='%s' and Year(Date)='%s' and Month(Date)='%s'"%(hfind+suffix, iDate.strftime('%Y'), iDate.strftime('%m'))
    return WAV

'''
Update the indices database with the following cleaned data.
Minimal parsing will be done on this data, such as accepting the float data type

Requires date to be datetime format
'''
def updateIndicesDB(cursor, db, name, date, ROR, NAV):
    strDate = date.strftime("%Y-%m-%d")
    try:
        cursor.execute("insert into rawdata.indices " + 
                   "Values('%s', '%s', '%s', '%s')"%(strDate, name, str(ROR), str(NAV)))
        db.commit()
    except _mysql_exceptions.OperationalError as e:
        print (strDate, name, str(ROR), str(NAV))
        print e
        db.rollback()
    except _mysql_exceptions.DataError:
        print (strDate, name, str(ROR), str(NAV))
        sys.exit("failed to input data")
    
'''
Create the value weighted indices for brokers, banks, insurers
This will be referenced against the S&P 500
'''
def createIndexTables():
    db = MySQLdb.connect(host = "127.0.0.1", port = 3306, user = "guest", passwd = "guest123", db = "rawdata")
    cursor = db.cursor()
    
    tableNames = ['brokers', 'banks', 'insurers', 'liquid', 'illiquid']
    
    currentYear = int(time.strftime('%Y'))
    currentMonth = int(time.strftime('%m'))
    
    cursor.execute("truncate rawdata.indices")
    db.commit()
    
    with open('SP500.csv', 'rb') as csvfile:
        SP500parse(csvfile, db, cursor)
    
    initYear = 1994
    initMonth = 1
    initDate = dt.date(1994, 1, 31)
    
    for tName in tableNames:
        NAV = 100.0
        ROR = 0.0
        updateIndicesDB(cursor, db, tName, initDate, ROR, NAV)
        
        oldWAV = getWAV(tName, initDate, cursor)
        iDate = addMonths(initDate, 1)
        iYear = initYear
        iMonth = initMonth
        while iYear!=currentYear and iMonth !=currentMonth:
            newWAV = getWAV(tName, iDate, cursor)
            if newWAV == 0:
                break
            ROR = newWAV/oldWAV - 1
            NAV = (1.0 + ROR)*NAV
            #print newWAV, ROR, NAV, iDate
            oldWAV = newWAV
            updateIndicesDB(cursor, db, tName, iDate, ROR*100, NAV)
            iDate = addMonths(iDate, 1)
        

def main():
    assert checkDBConnection()
    #pullHFIndxCSV()
    #fillHFIndxDatabase()
    print "Finished updating HF Indices"
    #pullHFCSV()
    print "Finished updating Hedge Funds"
    createIndexTables()
    print "Finished updating index tables"
    
if __name__ == '__main__':
    main()