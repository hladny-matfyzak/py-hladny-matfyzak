from bs4 import BeautifulSoup
import urllib2
import re
import time
import datetime

def horna(day = None, month = None):
    year = time.strftime("%Y")
    if day != None and month != None:
        lin = "http://hladnystudent.zones.sk/jedalne-listky-"+str(day)+"-"+str(month)+"-"+str(year)
        url = urllib2.urlopen(lin)        
    else :
        url = urllib2.urlopen("http://hladnystudent.zones.sk/")
    
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
    
def dolna(day = None, month = None):
    list= []
    year = time.strftime("%Y")
    weekday = time.strftime("%w")
    weekday = int(weekday)
    if day != None and month != None:
        lin = "http://hladnystudent.zones.sk/jedalne-listky-"+str(day)+"-"+str(month)+"-"+str(year)
        day = int(day)
        year = int(year)
        month = int(month)
        weekday = (datetime.date(year,month,day)).weekday()
        weekday = int(weekday)
        if weekday == 6 or weekday == 5:
            list.append("Closed")
            return list
        url = urllib2.urlopen(lin)
    else :
        url = urllib2.urlopen("http://hladnystudent.zones.sk/")
        if weekday == 6 or weekday == 0:
            list.append("Closed")
            return list
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

print(horna())
#print(dolna())

