/*******************************************************************************/
* 	Program        :    bm_yield.sas
*	Author         :    Ray Weng
*	Version        :    1.0
*	Date Created   :    10/24/2014
*	Last Modified  :    1/15/2015
*
*	Program Description:
*	Usage          :    To read CRSP Bonds (SAS dataset) and get all 
daily yields and prices for noncallable bills and bonds.
*	Input	       :    crsp.bmyield 
*	Output	       :    bmyield.log -- Log file
*			    bmyield.lst -- Output(list) file.
*	Method         :    SAS: PROC PRINT     
*                             
*	Variable    Variable Label
*	------------------------------------------------------------------- 
*	ACCINT      Total Accrued Interest at End of Day
*	CRSPID	    CRSP Issue Identification Number                       
*	DURATN	    Duration (Macaulay Duration) 
*	QDATE	    Quote Date                   
*	RETNUA	    Unadjusted Return            
*	YIELD	    Promised Daily Yield         
/*******************************************************************************/

options nosource nodate nocenter nonumber ps=max ls=72;

title ' ';



/* -------------------------------------------------------------------- */

/* Print out the data extraction                                        */      

/*  - noobs - "do not print the observation numbers"                    */      

/*  - label - "display variable labels"                                 */      

/* -------------------------------------------------------------------- */
data yields;
set crsp.bmyield;
where year(qdate) > 1987;

data prices;
set crsp.bmquotes;
where year(qdate) > 1987;

data yield_quotes;
merge yields prices;
by crspid qdate;

data security_data;
	set crsp.bmheader;
	where type in ('1','2','4');
	where tax = '1';
	where flower = '1';
	where year(matdt) > 1987;
/* security_data is now restricted to non callable bonds and T-bills 
with maturity greater than 1987 */


data security;
	set security_data (keep = crspid cusip name matdt type couprt 
datdt);

/* write these relevant CRPSIP/CUSIPs for the debt that we want, to a 
csv file so we can see which debts we are tracking*/
ods xml body="security_data.csv" type=csv;
proc print data=security noobs;
run;
ods xml close;


/* filter (daily) data in aggregated quote/yield table to only those 
debts we selected above that meet our noncallable post 1987 
criteria so that we can build a svensson model for each day*/
proc sql;
	create table filtered_data as
	select yield_quotes.crspid, 
security_data.cusip, yield_quotes.qdate, 
yield_quotes.yield, yield_quotes.bid, yield_quotes.ask, 
security_data.matdt, security_data.couprt, security_data.datdt, 
security_data.name
	from yield_quotes
	inner join security_data
	on yield_quotes.crspid = security_data.crspid
	order by yield_quotes.qdate;

data filtered_daily;
set filtered_data;


ods xml body="dailies.csv" type=csv;
proc print data=filtered_daily noobs; /* limit no. of observations */

run;
ods xml close;

/* Maturity date is the first half of the crsp ID field    		*/

/* This date is in YYYYMMDD format (1/1/97 = 19970101)                  */

/* Underscores in the second half of the crsp ID represent wildcard	*/ 

/* characters								*/

/* -------------------------------------------------------------------- */
