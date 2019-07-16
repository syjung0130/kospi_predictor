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
import threading
import re
import collections

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
        
        self.start_time = datetime.datetime(2019, 7, 11, 9, 10, 00)
        self.end_time = datetime.datetime(2019, 7, 11, 15, 30, 00)
        self.set_base_time(self.start_time)
        self.set_url(self.start_time)
        self.time_table = collections.OrderedDict()
        self.volume_table = collections.OrderedDict()

    def set_base_time(self, time):
        self.base_time = time

    def get_base_time_str(self):
        base_time_str = self.get_time_str(self.base_time)
        # nowDatetime = self.base_time.strftime('%Y%m%d%H%M%S')
        return base_time_str
    
    def get_time_str(self, time):
        return time.strftime('%Y%m%d%H%M%S')

    def set_url(self, time):
        '''
        https://finance.naver.com/item/sise_time.nhn?code=035420&amp&thistime=20190621130000&amp&page=1
        '''
        self.str_search_base = "https://finance.naver.com"
        self.set_base_time(time)

        self.str_item_page = "/item/sise_time.nhn?code={}&amp&thistime={}&amp&page=1".format(self.str_code, self.get_base_time_str())
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
    
    def update_price(self):
        print('[DailyCollecotr][update_price] ')
        # BeautifulSoup으로 html소스를 python객체로 변환한다, 첫 인자는 html소스코드, 두 번째 인자는 어떤 parser를 이용할지 명시.
        self.soup = BeautifulSoup(self.html, 'html.parser')

        # BeautifulSoup를 이용해서 가져온 html을 parsing, 필요한 정보를 구성
        table_list = self.soup.body.find_all("table")
        # print('[soup] table_list len: {0}, type: {1}'.format(len(table_list), type(table_list[0])))
        tr_tag_list = table_list[0].find_all("tr")
        
        # print('[soup] price tr tag list length: {}'.format(len(tr_tag_list)))
        full_price_attr_list = [ item.find_all('span', {'class':'tah p11'}) for item in tr_tag_list ]
        price_attr_list = [ attr for attr in full_price_attr_list if attr]
        price_list = []
        deal_volume_list = []
        for item in price_attr_list:
            # print('type: {0}, item: {1}'.format(type(item), item))
            # print('item[0], tag: {0}, {1}'.format(type(item[0]),item[0]))
            # item[0], tag: <class 'bs4.element.Tag'>, <span class="tah p11">113,500</span>

            p = re.compile('\>[0-9,]+')
            value_list = p.findall(str(item[0]))
            price = value_list[0][1:]
            price = price.replace(',', '')
            price_list.append(price)
            
            value_list = p.findall(str(item[-2]))
            deal_volume = value_list[0][1:]
            deal_volume = deal_volume.replace(',', '')
            deal_volume_list.append(deal_volume)

        print('price list: {0}'.format(price_list))
        print('deal volume list: {0}'.format(deal_volume_list))
        
        # print('[soup] full_price_attr_list len: {0}, price attr list: {1}'.format(len(full_price_attr_list), len(price_attr_list)))
        temp_time = self.base_time
        self.update_prices_in_ten_minutes(price_list, deal_volume_list, temp_time)

    def update_prices_in_ten_minutes(self, price_list, volume_list, time):
        cur_time = time
        for item in list(reversed(price_list)):
            self.time_table[cur_time] = int(item)
            one_minute = datetime.timedelta(minutes=1)
            cur_time = cur_time + one_minute
        # print("time table dict: {}".format(self.time_table))
        
        cur_time = time
        for item in list(reversed(volume_list)):
            self.volume_table[cur_time] = int(item)
            one_minute = datetime.timedelta(minutes=1)
            cur_time = cur_time + one_minute
        # print("volume table dict: {}".format(self.volume_table))
    
    def read_stock_data(self):
        count = 6*6+2
        print("count : {}".format(count))
        temp_time = self.start_time

        for i in range(count):
            print('current time: {}'.format(self.get_time_str(temp_time)))
            self.set_url(temp_time)
            self.get_html_page()
            self.update_price()
            ten_minute = datetime.timedelta(minutes=10)
            temp_time = temp_time + ten_minute
            

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
        start = datetime.datetime(2009, 5, 1)
        end = datetime.datetime(2019, 6, 20)
        self.web_data_frame = pd_reader.DataReader(self.code+".KS", "yahoo", start, end)

        # print('==== stock data info from web =====')
        # print(self.web_data_frame.head)

        self.kospi_data = KospiDBManager(self.code)
        self.kospi_data.read_web_api_data(self.web_data_frame)

class KospiDBManager:
    def __init__(self, code):
        self.con = sqlite3.connect("./kospi.db")
        self.code = code

    def read_web_api_data(self, web_data_frame):
        web_data_frame.to_sql(self.code, self.con, if_exists='replace')
        self.read_data_frame = pd.read_sql("SELECT * FROM '{}'".format(self.code), self.con, index_col = 'Date')
        print('==== readed stock data info =====')
        print(self.read_data_frame.head)

daily_collector = DailyCollector("035420")
daily_collector.read_stock_data()

hourly_collector = HourlyCollector("035420")
hourly_collector.read_stock_data()