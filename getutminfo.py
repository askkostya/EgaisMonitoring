#!/usr/bin/python3
# Get UTM info
# Used for Zabbix Scripts
import datetime
import requests
import sys


def deltadate(strData):
    now = datetime.datetime.now()
    DateofEND = datetime.datetime.strptime(strData, "%Y-%m-%d %H:%M:%S")
    deltaindays = (DateofEND - now).days
    return deltaindays

def getUTMUrl(getURL):
    try:
        user_agent = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(getURL, headers=user_agent)
        return (r.text)
    except requests.exceptions.RequestException:
    # Timeout or ConnectionError
        sys.exit()

try:
    getURL = sys.argv[2]
except BaseException:
    getURL = "http://localhost:8080"

if sys.argv[1] == "version":
    httptext = getUTMUrl(getURL+'/info/version')
    print(httptext)

if sys.argv[1] == "rsavalid":
    httptext = getUTMUrl(getURL)
    ipnumstr = httptext.rfind("Проблемы с RSA:")
    if ipnumstr == -1:
        print("Valid")
    else:
        print("Invalid")

if sys.argv[1] == "rsadate":
    httptext = getUTMUrl(getURL+'/home')
    ipnumstr = httptext.rfind("Сертификат RSA")
    strRSA = (httptext[ipnumstr+77:ipnumstr + 140])
    ipnumstr = strRSA.rfind("по")
    RSAdatestr = (strRSA[ipnumstr + 3:ipnumstr + 22])
    print(deltadate(RSAdatestr))

if sys.argv[1] == "gostdate":
    httptext = getUTMUrl(getURL+'/home')
    ipnumstr = httptext.rfind("Сертификат ГОСТ")
    strGOST = (httptext[ipnumstr:ipnumstr + 140])
    ipnumstr = strGOST.rfind("по")
    GOSTdatestr = (strGOST[ipnumstr + 3:ipnumstr + 22])
    print(deltadate(GOSTdatestr))

if sys.argv[1] == "docsbuffer":
    httptext = getUTMUrl(getURL)
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
