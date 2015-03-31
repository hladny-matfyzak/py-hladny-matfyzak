from bs4 import BeautifulSoup
import urllib2
import re
import time
import datetime
HS_URL = "http://hladnystudent.zones.sk"

def horna(day = None, month = None, year = None):
    if year == None:
        year = time.strftime("%Y")
    if month == None:
        month = time.strftime("%m")
    if day == None:
        day = time.strftime("%d")
    lin =HS_URL.format("/jedalne-listky-",day,month,year)
    url = urllib2.urlopen(lin)        

    
    text = url.read()
    soup = BeautifulSoup(text)
    tables = soup.find_all('table')
    hornasoup = BeautifulSoup(str(tables[1])) 
    list = []
    trs = hornasoup.find_all('tr')

    for i in range (1,len(trs)):        
         td = str(trs[i])
         tdsoup = BeautifulSoup(td)
         bordel = tdsoup.find_all('td')
         match = re.findall(r'<td>(.*?)<span',str(bordel[1]),re.DOTALL)
         bettermatch = re.findall(r'\n\s\s\s\s\s\s\s\s(.*?)\n',match[0])
         list.append(bettermatch[0])
    return list
    
def dolna(day = None, month = None, year = None):
    list= []
    if year == None:
        year = (int)(time.strftime("%Y"))
    if day == None:
        day = (int)(time.strftime("%d"))
    if month == None:
        month = (int)(time.strftime("%m"))
    lin =HS_URL.format("/jedalne-listky-",day,month,year)
    weekday = (datetime.date(year,month,day)).weekday()
    weekday = int(weekday)
    if weekday == 6 or weekday == 5:
        list.append("Closed")
        return list
    url = urllib2.urlopen(lin)
        
    text = url.read()
    soup = BeautifulSoup(text)
    tables = soup.find_all('table')
    dolnasoup = BeautifulSoup(str(tables[2])) 
    trs_dolna = dolnasoup.find_all('tr')

    for i in range (1,trs_dolna.__len__()):        
        dtd = str(trs_dolna[i])
        dtdsoup = BeautifulSoup(dtd)
        dbordel = dtdsoup.find_all('td')

        dmatch = re.findall(r'<td>(.*?)<span',str(dbordel[1]),re.DOTALL)
        dbettermatch = re.findall(r'\n\s\s\s\s\s\s\s\s(.*?)\n',dmatch[0])
        list.append(dbettermatch[0])
    return list
