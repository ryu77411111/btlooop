#!/usr/bin/python3
import re
import sys
import json
import time
import requests
import traceback
import datetime
from contextlib import closing
from zoneinfo import ZoneInfo

AREA='03'
TIME_LIST={
    '00:00': True,
    '00:30': True,
    '01:00': True,
    '01:30': True,
    '02:00': True,
    '02:30': True,
    '03:00': True,
    '03:30': True,
    '04:00': True,
    '04:30': True,
    '05:00': True,
    '05:30': True,
    '06:00': True,
    '06:30': True,
    '07:00': True,
    '07:30': True,
    '08:00': True, #Falseは売電優先
    '08:30': True, #Falseは売電優先
    '09:00': True, #Falseは売電優先
    '09:30': True, #Falseは売電優先
    '10:00': True, #Falseは売電優先
    '10:30': True, #Falseは売電優先
    '11:00': True, #Falseは売電優先
    '11:30': True, #Falseは売電優先
    '12:00': True, #Falseは売電優先
    '12:30': True, #Falseは売電優先
    '13:00': True, #Falseは売電優先
    '13:30': True, #Falseは売電優先
    '14:00': True, #Falseは売電優先
    '14:30': True, #Falseは売電優先
    '15:00': True, #Falseは売電優先
    '15:30': True, #Falseは売電優先
    '16:00': True, #Falseは売電優先
    '16:30': True,
    '17:00': True,
    '17:30': True,
    '18:00': True,
    '18:30': True,
    '19:00': True,
    '19:30': True,
    '20:00': True,
    '20:30': True,
    '21:00': True,
    '21:30': True,
    '22:00': True,
    '22:30': True,
    '23:00': True,
    '23:30': True} 

##--GetPrice--###########
def getnow():
    now = datetime.datetime.now(ZoneInfo('Asia/Tokyo'))
    # + datetime.timedelta(days = 1)
    #return f'{now:%Y/%m/%d}'
    return f'{now:%H:%M}'

def isprice(jobj, idx):
    return True if idx in jobj.keys() and 'price_data' in jobj[idx].keys() else False

def getidx(now):
    idxmap = []
    for idx in range(0, 48):
        hhmm = list(TIME_LIST.keys())[idx]
        day = '2' if hhmm < now else '1'
        idxmap.append((day, idx))
    return sorted(idxmap)

def getpricemap(result):
    jobj = json.loads(result)
    # 2:明日 or 1:今日
    day = '2' if isprice(jobj, '2') else '1' if isprice(jobj, '1') else None
    map = {}
    for idxday, idx in getidx(getnow()):
        #print(f'{idx} {idxday}', file=sys.stderr)
        if day < idxday:
            continue
        prices = jobj[idxday]['price_data']
        hhmm = list(TIME_LIST.keys())[idx]
        strday = 'tomorrow' if idxday == '2' else 'today' if idxday == '1' else ''
        key = f'{hhmm}{strday}'
        map[key] = prices[idx]
    return day, map

def getwebprice():
    url = 'https://looop-denki.com/api/prices?select_area=' + AREA
    try:
        with closing(requests.session()) as session:
            contents = session.get(url)
            #print('contents_status:' + str(contents.status_code), file=sys.stderr)
            return getpricemap(contents.text)
    except Exception as e:
        print(list(traceback.TracebackException.from_exception(e).format()), file=sys.stderr)
    return None

def getlolist(price, limit):
    lolist = []
    for key, val in list(price.items()):
        if TIME_LIST[key[:5]] and val < limit:
            lolist.append((key, val))
    lolist = sorted(lolist, key=lambda v:v[1])
    return lolist

def gethilist(price, limit):
    hilist = []
    for key, val in price.items():
        if limit < val:
            hilist.append((key, val))
    return hilist

def contain(hhmm, list):
    for key, val in list:
        if hhmm == key:
            return True
    return False

def makeplan(day, price, hilimit, lolimit, mode):
    hilist = gethilist(price, hilimit)
    lolist = getlolist(price, lolimit) if 0 < len(hilist) else []
    #print(lolist, file=sys.stderr)
    #print(hilist, file=sys.stderr)
    prev = None
    for key, val in price.items():
        if contain(key, lolist):
            cmd = '42' #充電
        elif contain(key, hilist):
            cmd = '43' #放電
        else:
            cmd = '44' #待機
        # 変更のみ or すべて
        if mode == 'chg' and prev == cmd:
            continue
        prev = cmd
        print(f'{key} {cmd} {val:.2f}')

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 3:
        print("usage: LooopBTSch.py hi_limit lo_limit [all|chg]", file=sys.stderr)
        exit()
    day, price = getwebprice()
    if price is None:
        exit('1')
    hilimit = float(args[1])
    lolimit = float(args[2])
    mode = 'chg' if len(args) < 4 else args[3]
    makeplan(day, price, hilimit, lolimit, mode)

