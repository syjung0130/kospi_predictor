#-*- coding:utf-8 -*-
from __future__ import unicode_literals
import sys
import urllib
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup
import chardet
import pandas as pd
import pandas_datareader.data as pd_reader
import datetime
import sqlite3

'''
naver finance crawling
 - to collect price every hour
'''
class HourlyCollector:
    def __init__(self, code):
        if(type(code) is str):
            self.str_code = code
        else:
            self.str_code = str(code)
        self.set_url()

    def set_url(self):
        '''
        https://finance.naver.com/item/sise_time.nhn?code=035420&amp;thistime=20190621161018&amp;page=1
        https://finance.naver.com/item/sise_time.nhn?code=035420&amp&thistime=20190621161018&amp&page=1
        https://finance.naver.com/item/sise_time.nhn?code=035420&amp&thistime=20190621161018&amp&page=10
        '''
        self.str_search_base = "https://finance.naver.com"
        self.base_time = "161000"
        self.str_item_page = "/item/sise_time.nhn?code={}&amp&thistime=20190621{}&amp&page=10".format(self.str_code, self.base_time)
        self.str_total_word = self.str_search_base + self.str_item_page
        print(self.str_total_word)

    # 검색결과를 요청해서 html로 가져옴
    def get_html_page(self):
        self.str_html = ""
        try:
            print('=== scrapper ===')
            self.html = urlopen(self.str_total_word).read()
            print("success..()")
            # print(self.html)

            print('*** encoding type: {0}'.format(chardet.detect(self.html)))
            encoding_type = chardet.detect(self.html)
            self.str_html = self.html.decode(encoding_type['encoding'], 'ignore')
            # print('type: {0}, html: \n{1}'.format(type(self.str_html), self.str_html))

        except HTTPError as e:
            print("exception 1")
            print(e.code)
        except URLError as e:
            print("exception 2")
            print(e.code)
    
    def get_value_list(self):
        print('=======================')
        print('[DailyCollecotr][value] ')
        # BeautifulSoup를 이용해서 가져온 html을 parsing, 필요한 정보를 구성
        # BeautifulSoup으로 html소스를 python객체로 변환하기
        # 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시.
        # 이 글에서는 Python 내장 html.parser를 이용했다.
        self.soup = BeautifulSoup(self.html, 'html.parser')
        soup = self.soup
        #recruit_info_list > ul > li:nth-child(1) > div > div > h2 > a
        # print('[soup] body {0}'.format(self.soup.body))
        # print('[soup] h2: {0}'.format(soup.h2))

        # table = soup.body.table
        table_list = soup.body.find_all("table")
        print('[soup] table_list: {}'.format(len(table_list)))
        print('type table[0]: {}'.format(type(table_list[0])))
        tr_tag_list = table_list[0].find_all("tr")
        
        print('[soup] price tr tag list length: {}'.format(len(tr_tag_list)))
        full_price_attr_list = [ item.find_all('td', {'class':'num'}) for item in tr_tag_list ]
        price_attr_list = [ attr for attr in full_price_attr_list if attr]
        # for item in price_attr_list:
        #     print('item: {}'.format(item))

        print('[soup] full_price_attr_list: {}'.format(len(full_price_attr_list)))
        print('[soup] price attr list: {}'.format(len(price_attr_list)))



'''
yahoo finance + pandas datareader
 - to collect price every day
'''
class DailyCollector:
    def __init__(self, code):
        if(type(code) is str):
            self.code = code
        else:
            self.code = str(code)
    
    def read_stock_data(self):
        start = datetime.datetime(2019, 5, 1)
        end = datetime.datetime(2019, 6, 20)
        self.web_data_frame = pd_reader.DataReader(self.code+".KS", "yahoo", start, end)

        print('==== stock data info from web =====')
        print(self.web_data_frame.head)

        con =  sqlite3.connect("./kospi.db")
        self.web_data_frame.to_sql(self.code, con, if_exists='replace')
        self.readed_data_frame = pd.read_sql("SELECT * FROM '{}'".format(self.code), con, index_col = 'Date')
        print('==== readed stock data info =====')
        print(self.readed_data_frame.head)

hourly_collector = HourlyCollector("035420")
hourly_collector.get_html_page()
hourly_collector.get_value_list()

daily_collector = DailyCollector("035420")
daily_collector.read_stock_data()


# # BeautifulSoup를 이용해서 가져온 html을 parsing, 필요한 정보를 구성
# # BeautifulSoup으로 html소스를 python객체로 변환하기
# # 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시.
# # 이 글에서는 Python 내장 html.parser를 이용했다.
# soup = BeautifulSoup(html, 'html.parser')
# #recruit_info_list > ul > li:nth-child(1) > div > div > h2 > a
# print('[soup] h1: {0}'.format(soup.h1))
# print('[soup] h2: {0}'.format(soup.h2))


# all_text = soup.find(id="recruit_info_list")
# print('[soup] ({0}) all_text: {1}'.format(len(all_text), type(all_text)))
# print('[soup] ul: {0}'.format(len(all_text.ul)))
# print('[soup] ul.li: {0}'.format(len(all_text.ul.li)))

    
# li_list = all_text.ul.li
# cnt = 0
# for li in li_list:
#     # print('[soup] li: ({0})'.format(li))
#     # print('[soup] li.a: {0}'.format(li.find("a")))
#     if(cnt == 1):
#         print('=============================')
#         # print('[soup] li type : {0}'.format(type(li)))
#         # print('[soup] li.a type : {0}'.format(type(li.find("a"))))
#         # print('[soup] li.a: {0}'.format(li.find("a")))
#         print('[soup] li.a.href: {0}'.format((li.find("a")).get('href')))
#         print('[soup] li.a.title: {0}'.format((li.find("a")).get('title')))
#         print('[soup] li.a.span: {0}'.format((li.find("a")).find('span')))
        
#         print('=============================')
#     cnt += 1
