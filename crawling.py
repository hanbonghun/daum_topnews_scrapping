# Crawling articles that be read out a lot by each date on news.daum.net
import requests
from bs4 import BeautifulSoup
import re
import csv

#Create csv file to save article title and content
csvfile= open('articles.csv', 'w', newline='',encoding='utf-8')
writer = csv.writer(csvfile)

URL = 'https://news.daum.net/ranking/popular?regDate=' # URL about articles that be read out a lot on news.daum.net
response = requests.get(URL)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

# Function of getting article title
def getTitle(soup):
    title = soup.find(class_ = 'tit_view').text
    return title

# Function of getting article contents
def getContents(soup):
    contents = '' # 'empty contets variable' for make full contents
    for i in soup.select('p[dmcf-ptype=general]'):
        contents = contents + str(i.find_all(text = True)) + '\n'
    return contents

# Function of cleaning article contents
def clean_text(text):
    cleaned_text = re.sub('[━><\[\]\'\\\\]', '', text)
    return cleaned_text

# Function of getting article URL
def getUrl(soup):
    url_list = []
    for rank in soup.select('ul.list_news2 strong.tit_thumb > a.link_txt'):
        url = rank.attrs['href']
        url_list.append(url)
    return url_list

# Function of crawling articles by date
def news_by_date_Crawling(URL, index):
    response = requests.get(URL)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    url_list = getUrl(soup)
    for rank in range(0, 50):
        response = requests.get(url_list[rank])
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        title = getTitle(soup)
        contents = getContents(soup)
        contents = clean_text(contents)
        contents = contents[:-1] # For delete last '\n'
        writer.writerow([title,contents])
       

# Function of crawling articles at 2020.08.01~2020.08.(1000 articles)
def newsCrawling(URL):
    print('Start crawling..')

    index = 0
    for day in range(20201101, 20201121):
        url_day = URL + str(day)
        news_by_date_Crawling(url_day, index)
        print(f'{day} 기사 스크롤링 완료.')
        index += 1
    print(f'스크롤링 종료. {50*index}개의 기사를 불러왔습니다.')

newsCrawling(URL)
