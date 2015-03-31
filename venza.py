from bs4 import BeautifulSoup
import urllib2
import re
import time
import datetime
HS_URL = "http://hladnystudent.zones.sk/jedalne-listky-{}-{}-{}"


def horna(day=None, month=None, year=None):
    if year is None and year.isdigit():
        year = int(time.strftime("%Y"))
    if day is None and day.isdigit():
        day = int(time.strftime("%d"))
    if month is None and day.isdigit():
        month = int(time.strftime("%m"))

    lin = HS_URL.format(day, month, year)
    url = urllib2.urlopen(lin)

    text = url.read()
    soup = BeautifulSoup(text)
    tables = soup.find_all('table')
    hornasoup = BeautifulSoup(str(tables[1]))
    list = []
    trs = hornasoup.find_all('tr')

    for i in range(1, len(trs)):
        td = str(trs[i])
        tdsoup = BeautifulSoup(td)
        bordel = tdsoup.find_all('td')
        match = re.findall(r'<td>(.*?)<span', str(bordel[1]), re.DOTALL)
        bettermatch = re.findall(r'\n\s\s\s\s\s\s\s\s(.*?)\n', match[0])
        list.append(bettermatch[0])
    return list


def dolna(day=None, month=None, year=None):
    list = []
    if year is None and year.isdigit():
        year = int(time.strftime("%Y"))
    if day is None and day.isdigit():
        day = int(time.strftime("%d"))
    if month is None and day.isdigit():
        month = int(time.strftime("%m"))

    lin = HS_URL.format(day, month, year)
    weekday = (datetime.date(year, month, day)).weekday()
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

    for i in range(1, len(trs_dolna)):
        dtd = str(trs_dolna[i])
        dtdsoup = BeautifulSoup(dtd)
        dbordel = dtdsoup.find_all('td')

        dmatch = re.findall(r'<td>(.*?)<span', str(dbordel[1]), re.DOTALL)
        dbettermatch = re.findall(r'\n\s\s\s\s\s\s\s\s(.*?)\n', dmatch[0])
        list.append(dbettermatch[0])
    return list
