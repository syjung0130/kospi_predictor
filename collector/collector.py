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
from timeutill_helper import TimeUtillHelper
from kospi_db_manager import KospiDBManager

class Collector:
    def __init__(self, code, start_time, end_time):
        if(type(code) is str):
            self.str_code = code
        else:
            self.str_code = str(code)
        self.set_start_time(start_time)
        self.set_end_time(end_time)
    
    def set_start_time(self, time):
        self.start_time = time
    
    def set_end_time(self, time):
        self.end_time = time

    def get_start_time(self):
        return self.start_time
    
    def get_end_time(self):
        return self.end_time
    
    def get_code(self):
        return self.str_code

'''
naver finance crawling
 - to collect price every hour
'''
class HourlyCollector(Collector):
    def __init__(self, code, start_time, end_time):
        Collector.__init__(self, code, start_time, end_time)
        self.set_base_time(start_time)
        self.price_table = collections.OrderedDict()
        self.volume_table = collections.OrderedDict()

    def set_base_time(self, time):
        self.base_time = time

    def set_url(self, time):
        '''
        https://finance.naver.com/item/sise_time.nhn?code=035420&amp&thistime=20190621130000&amp&page=1
        '''
        self.str_search_base = "https://finance.naver.com"
        self.set_base_time(time)
        self.str_item_page = "/item/sise_time.nhn?code={}&amp&thistime={}&amp&page=1".format(self.str_code, self.base_time.get_time_str())
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
        print('[HourlyCollector][update_price] ')
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
        for price_item, volume_item in zip(reversed(price_list), reversed(volume_list)):
            self.price_table[cur_time.get_datetime()] = float(price_item)
            self.volume_table[cur_time.get_datetime()] = float(volume_item)
            # print('cur time: {0}'.format(cur_time.get_datetime().replace(microsecond=0).isoformat().replace('T',' ')))
            cur_time.add_minutes(1)

    def read_stock_data(self):
        temp_time = self.get_start_time()
        while(temp_time < self.get_end_time()):
            print('current time : {}'.format(temp_time.get_time_str()))
            self.set_url(temp_time)
            self.get_html_page()
            self.update_price()
            # temp_time.add_minutes(10) ## update_price_in_ten_minutes()에서 1씩 10을 더하기 때문에 필요없다..
            #하루의 주식 시장 종료 시간까지 갔을 경우, 순회를 위해 temp_time을 다음날의 첫 시간으로 설정한다.
            if ((temp_time.get_hour() == self.get_end_time().get_hour()) and (temp_time.get_minute() >= self.get_end_time().get_minute())):
                if(temp_time.get_day() == self.get_end_time().get_day()):#end_date일 경우, 빠져나감
                    return
                if (temp_time.get_weekday() >= 4):#금요일일 경우, 토,일요일을 skip, 날짜를 월요일로 jump
                    temp_time.add_days(3)
                else:
                    temp_time.add_days(1)#금요일이 아닐 경우, 날짜를 다음 날로 jump
                
                #다음 날의 주식시장 시작시간 또는, 월요일 주식시장의 시작시간으로 set한다.
                temp_time.set_time(temp_time.get_year(), temp_time.get_month(), temp_time.get_day(), 9, 10)
        
    def update_db(self):
        self.table_name = "{}_hour".format(self.str_code)
        self.db_manager = KospiDBManager(self.table_name)

        #2009-05-04 00:00:00(19자리), 가격(실수:16자리 중 소수8자리), 거래량(실수:16자리 중 소수 1자리)
        str_query = "CREATE TABLE '{0}' (Date WCHAR(19), Close FLOAT(16, 8), BasePrice FLOAT(16,8), Volume FLOAT(16,1))".format(self.table_name)
        self.db_manager.execute_query(str_query)
        self.db_manager.apply_to_db()

        price_table_keys = list(self.price_table.keys())
        volume_table_keys = list(self.volume_table.keys())
        print('type price:{0}, volume:{1}'.format(type(price_table_keys[0]), type(volume_table_keys[0])))
        for price_date, volume_date in zip(price_table_keys, volume_table_keys):
            price_date_str = price_date.replace(microsecond=0).isoformat().replace('T',' ')
            str_query = "INSERT INTO '{0}'(Date, Close, BasePrice) VALUES ('{1}', {2}, {3})".format(\
                self.table_name, \
                price_date_str, \
                self.price_table[price_date], \
                self.price_table[price_date],
                )
            # print(str_query)
            self.db_manager.execute_query(str_query)
            self.db_manager.apply_to_db()

            volume_date_str = volume_date.replace(microsecond=0).isoformat().replace('T',' ')
            str_query = "UPDATE '{0}' SET Volume = {1} WHERE Date = '{2}'".format(\
                self.table_name,\
                self.volume_table[volume_date],\
                volume_date_str)
            # print(str_query)
            self.db_manager.execute_query(str_query)
            self.db_manager.apply_to_db()


'''
yahoo finance + pandas datareader
 - to collect price every day
'''
class DailyCollector(Collector):
    def __init__(self, code, start_time, end_time):
        Collector.__init__(self, code, start_time, end_time)

    def read_stock_data(self):
        start = self.get_start_time().get_datetime()
        end = self.get_end_time().get_datetime()
        self.web_data_frame = pd_reader.DataReader(self.str_code+".KS", "yahoo", start, end)
        self.write_db_from_web_api_data(self.web_data_frame)

    def write_db_from_web_api_data(self, web_data_frame):
        self.table_name = "{}_day".format(self.str_code)
        self.db_manager = KospiDBManager(self.table_name)
        connection = self.db_manager.get_connection()
        web_data_frame.to_sql(self.table_name, connection, if_exists='replace')
        print('==== readed stock data info =====')
        kospi_db = pd.read_sql("SELECT * FROM '{}'".format(self.table_name), connection, index_col = 'Date')
        print(kospi_db.head)

start_time = TimeUtillHelper(2009, 5, 1)
end_time = TimeUtillHelper(2019, 6, 20)
daily_collector = DailyCollector("035420", start_time, end_time)
daily_collector.read_stock_data()

start_time = TimeUtillHelper(2019, 7, 29, 9, 10, 00)
end_time = TimeUtillHelper(2019, 8, 2, 15, 30, 00)
hourly_collector = HourlyCollector("035420", start_time, end_time)
hourly_collector.read_stock_data()
hourly_collector.update_db()