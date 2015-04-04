from bs4 import BeautifulSoup
import requests
import re
import time
import datetime
HS_URL = "http://hladnystudent.zones.sk/jedalne-listky-{}-{}-{}"
FF_URL = "http://www.freefood.sk/menu/"


def horna(day=None, month=None, year=None):
    if year is None or not year.isdigit():
        year = int(time.strftime("%Y"))
    if day is None or not day.isdigit():
        day = int(time.strftime("%d"))
    if month is None or not month.isdigit():
        month = int(time.strftime("%m"))

    lin = HS_URL.format(day, month, year)

    req = requests.get(lin)

    soup = BeautifulSoup(req.text)
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
    if year is None or not year.isdigit():
        year = int(time.strftime("%Y"))
    if day is None or not day.isdigit():
        day = int(time.strftime("%d"))
    if month is None or not month.isdigit():
        month = int(time.strftime("%m"))

    lin = HS_URL.format(day, month, year)

    weekday = int((datetime.date(year, month, day)).weekday())
    if weekday in [5, 6]:
        list.append("Closed")
        return list

    req = requests.get(lin)

    soup = BeautifulSoup(req.text)
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


def ffood( which ,weekday=None):
    if weekday == None:
        year = int(time.strftime("%Y"))
        day = int(time.strftime("%d"))
        month = int(time.strftime("%m"))
        weekday = int((datetime.date(year, month, day)).weekday())
    req = requests.get(FF_URL)
    soup = BeautifulSoup(req.text)
    menu_week = soup.find_all('ul')
    if which == 0:
        index = 3
    elif which == 1:
        index = 10
    menu_week = menu_week[index]
    menu_bs = BeautifulSoup(str(menu_week))
    daymenu = menu_bs.find_all('ul')[weekday]
    #weekday should be <1,5>
    lis = BeautifulSoup(str(daymenu))
    lis.find_all('li')
    meals = re.findall(r'</span>(.*?)<span class="brand">', str(lis), re.DOTALL)
    ret = []
    for i in range (0,len(meals)):
        if ((i % 2)==0):
            ret.append(meals[i])
    return ret   