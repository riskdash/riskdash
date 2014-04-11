'''
Created on Apr 10, 2014

@author: Hanwen Xu
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

'''
Get the Hedge Fund Index CSV from Credit Suisse 
'''

def test():
    driver = webdriver.Firefox()
    driver.get("http://www.hedgeindex.com/hedgeindex/secure/en/datadownload.aspx?cy=USD")
    #assert "Python" in driver.title
    try:
        elem = driver.find_element_by_name("ctl00$ContentPlaceHolder1$Login1$txtUserID")
        elem.send_keys("hanwenxu")
        elem = driver.find_element_by_name("ctl00$ContentPlaceHolder1$Login1$txtPassword")
        elem.send_keys("TerribleAbs15")
        elem.send_keys(Keys.RETURN)
        elem = driver.find_element_by_name("ctl00$ContentPlaceHolder1$LoginConfirm1$AcceptButton")
        elem.click()
        elem = driver.find_element_by_name("ctl00$ContentPlaceHolder1$datadownload1$chkNavRor$0")
        elem.click()
        elem = driver.find_element_by_name("ctl00$ContentPlaceHolder1$datadownload1$btnDownload")
        elem.click()
        
        
    except:
        pass
    #time.sleep(2)
    #driver.close()

if __name__ == '__main__':
    test()