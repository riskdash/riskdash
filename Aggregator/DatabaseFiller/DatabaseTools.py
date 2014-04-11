'''
Created on Apr 10, 2014

@author: Hanwen Xu
'''
import datetime as dt, calendar
import MySQLdb

TABLENAMES = ['brokers', 'banks', 'insurers']

'''
Return the parsed date from 08/16/1988

---input--- 
date_raw:  requires to be a string of form 08/16/1988. 
takes the locale's appropriate date in 08/16/1988 format
output:  returns a string with YYYY-MM-DD format
'''
def formatDate(date_raw):
    date = dt.datetime.strptime(date_raw, "%x")
    #print date
    date_clean = date.strftime("%Y-%m-%d")
    return date_clean

'''
returns a datetime object with the gap of m months

---input---
sourcedate:  requires to be a datetime object 
m:  requires to be a number.  Can be float, integer, or double

---output---
returns:  a datetime object with shifted date by m months
'''
def addMonths(sourcedate, m):
    month = sourcedate.month - 1 + m
    year = sourcedate.year + month/12
    month = month%12 +1
    day = calendar.monthrange(year,month)[1]
    return dt.date(year,month,day)

'''
Checks the database connection
'''
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
    

'''
Print out text files of the unique PERMNOs
'''
def printPermnos():
    db = MySQLdb.connect(host = "127.0.0.1", port = 3306, user = "guest", passwd = "guest123", db = "rawdata")
    cursor = db.cursor()
    for t in TABLENAMES:
        selectString = "select distinct(permno) "
        fromString = "from rawdata.%s "%t
        intoString = "into outfile '%s.txt' LINES TERMINATED BY '\n';"%t
        sqlQuery = selectString+fromString+intoString
        cursor.execute(sqlQuery)
    db.close()
    
'''
Load CSV files into the database tables
'''
def loadInstitutionCSVs():
    db = MySQLdb.connect(host = "127.0.0.1", port = 3306, user = "guest", passwd = "guest123", db = "rawdata")
    cursor = db.cursor()
    for t in TABLENAMES:
        trnQuery = "truncate table rawdata.%s"%t
        cursor.execute(trnQuery)
        db.commit()
        loadString = "load data local infile "
        fileString = "'C:\\\\Users\\\\Hanwen Xu\\\\Dropbox\\\\6.UAR\\\\Data Raw\\\\CRSP\\\\tmp\\\\%s.csv' "%t
        intoString = "into table rawdata.%s fields terminated by ',' lines terminated by '\n' IGNORE 1 LINES;"%t
        sqlQuery = loadString+fileString+intoString
        cursor.execute(sqlQuery)
        db.commit()
        sqlQuery2 = "delete from %s where PERMNO=0;"%t
        cursor.execute(sqlQuery2)
        db.commit()
    db.close()



