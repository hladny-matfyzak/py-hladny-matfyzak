from bs4 import BeautifulSoup
import requests
import re
import time
import datetime
from enum import Enum
HS_URL = "http://hladnystudent.zones.sk/jedalne-listky-{}-{}-{}"
FF_URL = "http://www.freefood.sk/menu/"
EAM_URL = "http://www.eatandmeet.sk/menu/{0}/{1:02d}/{2:02d}"
ML_URL = "http://www.mlynska-dolina.sk/stravovanie/vsetky-zariadenia/venza/denne-menu"
DRAG_URL = "http://www.restauracia-drag.sk/?page=menu"

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
                        " price={price}"                        
                        ")>")


def horna(day=None, month=None, year=None):
    if year is None or not isinstance(year,int):
        year = int(time.strftime("%Y"))
    if day is None or not isinstance(day,int):
        day = int(time.strftime("%d"))
    if month is None or not isinstance(month,int):
        month = int(time.strftime("%m"))
    
    lin = EAM_URL.format(year, month, day)
    req = requests.get(lin)
    soup = BeautifulSoup(req.text)
    divs = soup.find_all('div')
    list = []
    
    try:
        hornasoup = BeautifulSoup(str(divs[18]))
        pol = re.findall(r'<span class="dish-name">(.*?)</span>', str(hornasoup))
        prices = re.findall(r'<span class="dish-price">...(.*?)/', str(hornasoup))
        list =[]
        for i in range (len(pol)):
            list.append(Meal(pol[i],'horna',prices[i],MealType.SOUP))
        
        hornameal = BeautifulSoup(str(divs[23]))
        meals = re.findall(r'<span class="dish-name">(.*?)</span>', str(hornameal))
        prices =re.findall(r'<span class="dish-price">...(.*?)/', str(hornameal))
        for i in range (len(prices)):
            list.append(Meal(meals[i],'horna',prices[i],MealType.MAIN_DISH))
    except IndexError:
        return ["unexpected structure of site"]
        
    return list


def dolna(day=None, month=None, year=None):
    if year is None or not isinstance(year,int):
        year = int(time.strftime("%Y"))
    if day is None or not isinstance(day,int):
        day = int(time.strftime("%d"))
    if month is None or not isinstance(month,int):
        month = int(time.strftime("%m"))

    list = []
    lin = ML_URL
    try:
        weekday = int((datetime.date(year, month, day)).weekday())
    except ValueError:
        return ["not a valid date"]
    if weekday in [5, 6]:
        list.append("Closed")
        return list

    req = requests.get(lin)
    soup = BeautifulSoup(req.text)
    tables = soup.find_all('table')
    meals_table = tables[weekday*9]
    soup_table = tables[weekday*9 + 6]
    meals = re.findall(r'<td width="400">(.*?)</td>', str(meals_table) )
    meal_price = re.findall(r'<td>(.*?)............./', str(meals_table))
    soups = re.findall(r'<td width="400">(.*?)</td>',str(soup_table))
    soup_price = re.findall(r'<td>(.*?)............./', str(soup_table))
    
    for i in range(len(soups)):
        list.append(Meal(soups[i],'dolna', soup_price[i],MealType.SOUP))
    for i in range(len(meals)):
        list.append(Meal(meals[i],'dolna', meal_price[i],MealType.MAIN_DISH)) 
    
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
    for i in range(len(meals)):
        if ((i % 2) == 0):
            price =  float(prices[i+1][:-3])   
            #due to strange format of price on site it needs to cut last 3
            # characters to make it possible to change it to float type
            ret.append(Meal(meals[i], which, price))
    return ret


def faynfood(weekday=None):
    return ffood('faynfood', weekday)


def freefood(weekday=None):
    return ffood('freefood', weekday)
    