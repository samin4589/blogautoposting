import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os
import feedparser
from newspaper import Article
from gensim.summarization.summarizer import summarize

date = str(datetime.now())
date = date[:date.rfind(':')].replace(' ', '_')
date = date.replace(':', '시') + '분'

query = input()

news_url = 'https://www.mdtoday.co.kr/news/search.php?q={}&sfld=subj&period=MONTH%7C12'.format(query)

req = requests.get(news_url)
soup = BeautifulSoup(req.text, 'html.parser')

dt = soup.find_all("dt")

print(dt)

for href in soup.find_all("dt"):

    try:
        mdt = requests.get("https://www.mdtoday.co.kr/" + href.find("a")["href"])
        mdtsoup = BeautifulSoup(mdt.text, 'html.parser')

        table = mdtsoup.find_all('div', {'id': 'articleBody'})

        sttable = str(table)

        cleantext = BeautifulSoup(sttable, "lxml").text

        cleantext1 = cleantext.replace(
            ", [저작권자ⓒ 메디컬투데이. 무단전재-재배포 금지], 댓글 0, - 띄어 쓰기를 포함하여 250자 이내로 써주세요.- 건전한 토론문화를 위해, 타인에게 불쾌감을 주는 욕설/비방/허위/명예훼손/도배 등의 댓글은 표시가 제한됩니다., 대량 모발이식, 복합 채취 필요한 상황과 주의사항]",
            "")

        print(summarize(cleantext1))


    except Exception as e:

        print(e)