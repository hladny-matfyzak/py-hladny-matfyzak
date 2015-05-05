from bs4 import BeautifulSoup
import requests
import re
import time
import datetime
from enum import Enum
HS_URL = "http://hladnystudent.zones.sk/jedalne-listky-{}-{}-{}"
FF_URL = "http://www.freefood.sk/menu/"


class MealType(Enum):
    SOUP = 0
    MAIN_DISH = 1
    OTHER = 2


class Meal(object):
    def __init__(self, name, place, price='', type=None):
        self.name = name
        self.place = place
        self.price = price
        self.type = type

    def fmt(self, form):
        return form.format(**self.__dict__)

    def __str__(self):
        return self.fmt("{name} - {place}")

    def __repr__(self):
        return self.fmt("<Meal('{name}',"
                        " place='{place}'"
                        " price='{price}'"                        
                        ")>")


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
        list.append(Meal(bettermatch[0], 'horna'))
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
        list.append(Meal(dbettermatch[0], 'dolna'))
    return list


def ffood(which, weekday=None):
    """Free/Fayn food wrapper. The first argument `which` describes which of
    these two is to be used: 0 for freefood, 1 for faynfood."""

    idx = {
        'freefood': 3,
        'faynfood': 10
    }

    if which not in idx.keys():
        return []
    index = idx[which]

    if weekday is None:
        year = int(time.strftime("%Y"))
        day = int(time.strftime("%d"))
        month = int(time.strftime("%m"))
        weekday = int((datetime.date(year, month, day)).weekday())

    req = requests.get(FF_URL)
    soup = BeautifulSoup(req.text)
    menu_week = soup.find_all('ul')

    menu_week = menu_week[index]
    menu_bs = BeautifulSoup(str(menu_week))
    daymenu = menu_bs.find_all('ul')[weekday]

    # weekday should be <1,5>
    lis = BeautifulSoup(str(daymenu))
    lis.find_all('li')
    meals = re.findall(r'</span>(.*?)<span class="brand">',
                       str(lis),
                       re.DOTALL)
    prices = re.findall(r'class="brand">(.*?)</span>',
                        str(lis))
                        
    ret = []
    for i in range(0, len(meals)):
        if ((i % 2) == 0):
            price =  float(prices[i+1][:-3])
            ret.append(Meal(meals[i], which, price))
    return ret


def faynfood(weekday=None):
    return ffood('faynfood', weekday)


def freefood(weekday=None):
    return ffood('freefood', weekday)
