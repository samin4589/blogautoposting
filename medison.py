
import requests, xmltodict, json
import pandas as pd

import time
import random
import requests

import pandas as pd

import signaturehelper

import os
import sys
import urllib.request
import json


def call(n):
    global ddf2, ddf1

    ddf2 = pd.DataFrame()

    key = "2euKJ4e1ZVTvxSSZB7%2BkFnM63%2Bg9k0tkYx3pnpRJseur0K%2B4i1iD2Yi6WeBQPeaCc2rZb%2Bc176Vc9WH2z875Cg%3D%3D"

    url = "http://apis.data.go.kr/1471000/HtfsInfoService2/getHtfsItem?ServiceKey=2euKJ4e1ZVTvxSSZB7%2BkFnM63%2Bg9k0tkYx3pnpRJseur0K%2B4i1iD2Yi6WeBQPeaCc2rZb%2Bc176Vc9WH2z875Cg%3D%3D&numOfRows=100&pageNo={}&type=xml".format(
        n)

    content = requests.get(url).content
    dict = xmltodict.parse(content)
    jsonString = json.dumps(dict['response']['body']['items'], ensure_ascii=False)
    jsonObj = json.loads(jsonString)
    # print(jsonObj)
    for p in jsonObj['item']:
        # print(p['prdlstNm'])
        # ddf = p['PRDUCT'],p['REGIST_DT']
        #ddf = p['PRDUCT'],p['REGIST_DT'],p['SRV_USE'],p['MAIN_FNCTN']
        ddf = p['PRDUCT']
        if int(p['REGIST_DT']) >20200101: # 최근 제품
            ddf2 = ddf2.append([ddf])


global ddf, ddf1, n
ddf = pd.DataFrame()
ddf1 = pd.DataFrame()

for n in range(251, 350):
    call(n)
    ddf1 = ddf1.append(ddf2)

print(ddf1)
ddf1.to_excel('350.xlsx')

# file = open("./nonPayment.json", "w+")
# file.write(json.dumps(jsonObj['items']['item']))