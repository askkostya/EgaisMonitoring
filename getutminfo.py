#!/usr/bin/python3
# Get UTM info
# Used for Zabbix Scripts
import datetime
import requests
import sys


def deltadate(strData):
    now = datetime.datetime.now()
    DateofEND = datetime.datetime.strptime(strData, "%Y-%m-%d %H:%M:%S")
    print((DateofEND - now).days)
    return

try:
    UTMURL = sys.argv[2]
except BaseException:
    UTMURL = "http://localhost:8080"

try:
    user_agent = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(UTMURL, headers=user_agent)
except requests.exceptions.RequestException:
    # Timeout or ConnectionError
    sys.exit()

if sys.argv[1] == "version":
    ipnumstr = r.text.rfind("<pre>version:")
    print(r.text[ipnumstr + 13:ipnumstr + 20])
if sys.argv[1] == "rsavalid":
    ipnumstr = r.text.rfind("Проблемы с RSA:")
    if ipnumstr == -1:
        print("Valid")
    else: 
        print("Invalid")
if sys.argv[1] == "rsadate":
    ipnumstr = r.text.rfind("PKI: FSRAR-RSA")
    strRSA = (r.text[ipnumstr:ipnumstr + 101])
    ipnumstr = strRSA.rfind("по")
    RSAdatestr = (strRSA[ipnumstr + 3:ipnumstr + 22])
    deltadate(RSAdatestr)
if sys.argv[1] == "gostdate":
    ipnumstr = r.text.rfind("ГОСТ:")
    strGOST = (r.text[ipnumstr:ipnumstr + 101])
    ipnumstr = strGOST.rfind("по")
    GOSTdatestr = (strGOST[ipnumstr + 3:ipnumstr + 22])
    deltadate(GOSTdatestr)
if sys.argv[1] == "docsbuffer":
    ipnumstr = r.text.rfind("Отсутствуют неотправленные розничные документы.")
    if ipnumstr == -1:
        ipnumstr = r.text.rfind("Дата самого старого неотправленного розничного документа:")
        DateFirstDOCDstr = (r.text[ipnumstr + 69:ipnumstr + 88])
        now = datetime.datetime.now()
        DateFirstDocEND = datetime.datetime.strptime(DateFirstDOCDstr, "%Y-%m-%d %H:%M:%S")
        print((now - DateFirstDocEND).seconds // 3600)
    else:
        print(0)
