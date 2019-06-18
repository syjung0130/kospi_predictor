#-*- coding:utf-8 -*-
from __future__ import unicode_literals
import sys
import urllib
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup
import chardet

# 검색결과를 요청해서 html로 가져옴
# html = bytes('', encoding='utf-8')
def get_html_page(str_total_word):
    html = bytes('', encoding='EUC-KR')
    str_html = ""
    try:
        print('=== scrapper ===')
        html = urlopen(str_total_word).read()
        print("success..")

        # print('*** encoding type: {0}'.format(chardet.detect(html)))
        str_html = html.decode('utf-8', 'ignore')
        print('type: {0}, html: \n{1}'.format(type(str_html), str_html))

    except HTTPError as e:
        print("exception 1")
        print(e.code)
    except URLError as e:
        print("exception 2")
        print(e.code)

str_search_base = "https://finance.naver.com/"
str_item_page = "item/sise_day.nhn?code="
str_code = "035420"
str_total_word = str_search_base + str_item_page + str_code
print("url : {}", str_total_word)

get_html_page(str_total_word)

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
