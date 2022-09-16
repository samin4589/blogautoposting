import time
import random
import requests

import pandas as pd

import signaturehelper

import os
import sys
import urllib.request
import json


def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8',
            'X-Timestamp': timestamp, 'X-API-KEY': API_KEY,
            'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


BASE_URL = 'https://api.naver.com'
API_KEY = '010000000058f49de37938d0de79fd97e7654fd2f2600112c18e3895bc62af000e433679e9'
SECRET_KEY = 'AQAAAABY9J3jeTjQ3nn9l+dlT9LyVlVKoyp+s7tQ0BA+2BCmuQ=='
CUSTOMER_ID = '2268245'


def get_keyword(w):
    global ddf
    global ch
    global ch2
    global ch3
    global ct

    # keyw = '노트북'
    uri = '/keywordstool'
    method = 'GET'
    prm = {'hintKeywords': w, 'showDetail': 1}
    r = requests.get(BASE_URL + uri, params=prm,
                     headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

    # r.json()['keywordList'][0]
    # print(r)
    client_id = "ErWmPO1KoMye3et18nhY"
    client_secret = "XnthrDWiD6"
    encText = urllib.parse.quote(str(w))
    url1 = "https://openapi.naver.com/v1/search/blog?query=" + encText  # json 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
    request1 = urllib.request.Request(url1)
    request1.add_header("X-Naver-Client-Id", client_id)
    request1.add_header("X-Naver-Client-Secret", client_secret)
    response1 = urllib.request.urlopen(request1)
    rescode = response1.getcode()

    if (rescode == 200):
        json_rt1 = response1.read().decode('utf-8')
        py_rt1 = json.loads(json_rt1)
        b = pd.DataFrame((py_rt1)['items'])
        ct = py_rt1['total']

        if (ct == 0):
            c = 0
        else:
            c = b.iloc[0:4, 1]
            c = c.replace('\n', '', regex=True)


    else:
        print("Error Code:" + rescode)

    df = pd.DataFrame(r.json()['keywordList'])

    relKeyword = df['relKeyword'][0]
    ct = py_rt1['total']
    pQcCnt = df['monthlyPcQcCnt'][0]
    mQcCnt = df['monthlyMobileQcCnt'][0]
    get_keyword1(w)

    data = [w, pQcCnt, mQcCnt, ct, cdata]
    ddf = pd.DataFrame([data], columns=['Col1', 'Col2', 'Col3', 'Col4', 'Col6'])
    ddf.loc[(ddf['Col2'] == '< 10'), 'Col2'] = '10'
    ddf.loc[(ddf['Col3'] == '< 10'), 'Col3'] = '10'
    if int(ddf['Col4']) == 0:
        ddf['Col5'] = 0
    else:
        ddf['Col5'] = ct / (int(ddf['Col2']) + int(ddf['Col3']))

    ch = int(ddf['Col5'])
    ch2 = int(ddf['Col2'])
    ch3 = int(ddf['Col3'])
    ddf['Col7'] = ddf['Col6'].apply(str).str.count('blog')


def get_keyword1(w):
    global cdd
    global cdata
    # keyw = '노트북'
    uri = '/keywordstool'
    method = 'GET'
    prm = {'hintKeywords': w, 'showDetail': 1}
    r = requests.get(BASE_URL + uri, params=prm,
                     headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

    # r.json()['keywordList'][0]
    # print(r)
    client_id = "ErWmPO1KoMye3et18nhY"
    client_secret = "XnthrDWiD6"
    encText = urllib.parse.quote(str(w))
    url = "https://openapi.naver.com/v1/search/webkr?query=" + encText  # json 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if (rescode == 200):
        json_rt = response.read().decode('utf-8')
        py_rt = json.loads(json_rt)
        b = pd.DataFrame((py_rt)['items'])
        t = py_rt['total']
        # z = b.iloc[1]
        # z = b.iloc[0:4,]

        if (t == 0):
            cdd = 0
        else:
            cdd = b.iloc[0:4, 1]

        # web = pd.DataFrame(b)
        # d = web['title']cn
        #  b = py_rt['total']

    else:
        print("Error Code:" + rescode)

    cdata = [cdd]
    # ddf = pd.DataFrame([data])


# 2. Excel 파일 불러오기
cf = pd.read_excel('350.xlsx')

# 3. excel 의 값을 list 로 변환
df_list = cf.values.tolist()

# # 4. 불러온 excel 의 column 값 가져오기
# df_col = list([col for col in cf])

# # 5. df_list 수정

# # 6. 다시 df 로 변환
# cf = pd.DataFrame(df_list, columns=df_col)
# c = cf.loc[:,]
# print(c)

global ddf1
ddf1 = pd.DataFrame()

st = 0
ed = 3957

for i in range(st, ed):
    # time.sleep(1)
    w = df_list[i:i + 1]
    try:
        get_keyword(w)

        if (ch < 0.05):
            if(ch2 != 10) or (ch3 != 10):
                ddf1 = ddf1.append(ddf)
                ddf1 = ddf1.replace('\n', '', regex=True)
    except:
        print(w)
ddf1.to_excel('건강350.xlsx')

