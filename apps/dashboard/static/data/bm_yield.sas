/*******************************************************************************/
* 	Program        :    bmyield.sas
*	Author         :    Steve Crispi
*	Version        :    1.0
*	Date Created   :    -
*	Last Modified  :    -
*
*	Program Description:
*	Usage          :    To read CRSP Bonds (SAS dataset) 
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

data joined;
merge yields prices;
by crspid qdate;

data security_data;
	set crsp.bmheader;
	where type in ('1','2','4');
	where tax = '1';
	where flower = '1';
	where year(matdt) > 1987;

data security;
	set security_data (keep = crspid cusip name matdt type couprt datdt);

ods xml body="security_data.csv" type=csv;
proc print data=security noobs;
run;
ods xml close;
/*
proc sql;
	create table filtered_data as
	select * from joined
	where joined.crspid in (select crspid from security_data);

data filtered_daily;
set filtered_data;


ods xml body="dailies.csv" type=csv;
proc print data=filtered_daily noobs; /* limit no. of observations 
*/
run;
ods xml close;

proc print data=joined noobs label;
*/
/* -------------------------------------------------------------------- */

/* To Query by the quote date 						*/

/*									*/

/* Dates must be referenced as SAS date values 				*/

/*  (1/1/97 = '01jan1997'd)    						*/     

/* The year() function returns the year of a SAS date.                  */     

/* -------------------------------------------------------------------- */



where year(qdate) between 1992 and 1992;



/* -------------------------------------------------------------------- */

/* To Query by the maturity date                                        */

/*                                                                      */

/* Maturity date is the first half of the crsp ID field    		*/

/* This date is in YYYYMMDD format (1/1/97 = 19970101)                  */

/* Underscores in the second half of the crsp ID represent wildcard	*/ 

/* characters								*/

/* -------------------------------------------------------------------- */



/* where crspid between "&byr&bmo&bda.______" and "&eyr&emo&eda.______";*/



/* -------------------------------------------------------------------- */

/* Specify the variable names in the order in which they are to appear  */

/*  - for a list of variables, go to http://wrds.wharton.upenn.edu      */

/* -------------------------------------------------------------------- */

var crspid qdate duratn;







