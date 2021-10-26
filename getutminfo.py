#!/usr/bin/python3
# Get UTM info
# Used for Zabbix Scripts
import datetime
import requests
import sys
import time


def deltadate(strData):
    now = datetime.datetime.now()
    DateofEND = datetime.datetime.strptime(strData[:-6], "%Y-%m-%d %H:%M:%S")
    deltaindays = (DateofEND - now).days
    return deltaindays


def getUTMURL(getURL, contType):
       try:
         user_agent = {'User-Agent': 'Mozilla/5.0'}
         r = requests.get(getURL, headers=user_agent)
         if contType == 1:
             return r.json()
         elif contType == 2:
             return r.text
       except requests.exceptions.RequestException:
     # Timeout or ConnectionError
             return -1


def getConnection(getURL, contType):
    i = 1
    while i < 5:
        utm_data = getUTMURL(getURL, contType)
        if utm_data != -1:
            return utm_data
        time.sleep(5)
        i = i+1

try:
    getURL = sys.argv[2]
except BaseException:
    getURL = "http://localhost:8080"

if sys.argv[1] == "version":
    httptext = getConnection(getURL+'/info/version', 2)
    print(httptext)

if sys.argv[1] == "rsavalid":
    httptext = getConnection(getURL + '/api/info/list', 1)
    rsaValid = httptext['rsa']['isValid']
    print(rsaValid)

if sys.argv[1] == "rsadate":
    httptext = getConnection(getURL + '/api/info/list', 1)
    expireDateStr = httptext['rsa']['expireDate']
    expireDate = deltadate(expireDateStr)
    print(expireDate)

if sys.argv[1] == "gostdate":
    httptext = getConnection(getURL+'/api/info/list', 1)
    expireDateStr = httptext['gost']['expireDate']
    expireDate = deltadate(expireDateStr)
    print(expireDate)

if sys.argv[1] == "docsbuffer":
    httptext = getConnection(getURL+'/home', 2)
    ipnumstr = httptext.rfind("Отсутствуют неотправленные чеки")
    if ipnumstr == -1:
        ipnumstr = httptext.rfind("Чеки не отправлялись с")
        DateFirstDOCDstr = (httptext[ipnumstr+23:ipnumstr + 42])
        now = datetime.datetime.now()
        DateFirstDocEND = datetime.datetime.strptime(DateFirstDOCDstr, "%Y-%m-%d %H:%M:%S")
        deltadays = (now - DateFirstDocEND).days*24
        deltaseconds = (now - DateFirstDocEND).seconds//3600
        print(deltadays+deltaseconds)
    else:
        print(0)
