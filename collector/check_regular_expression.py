#-*- coding:utf-8 -*-
import re

# [<span class="tah p11">113,500</span>, <span class="tah p11">114,000</span>, <span class="tah p11">113,500</span>, <span class="tah p11">84,868</span>, <span class="tah p11">16,649</span>]
# item[0], tag: <class 'bs4.element.Tag'>, <span class="tah p11">113,500</span>

# str_html = "\<span class=\"tah p11\"\>113,500\<\/span\>, \<span class=\"tah p11\"\>114,000\<\/span\>, <span class="tah p11">113,500</span>, <span class="tah p11">84,868</span>, <span class="tah p11">16,649</span>"
# str_html = "\<span class=\"tah p11\"\>113,500\<\/span\>, \<span class=\"tah p11\"\>114,000\<\/span\>"
str_html = "\<span class=\"tah p11\"\>113,500\<\/span\>, \<span class=\"tah p11\"\>114,000\<\/span\>, \<span class=\"tah p11\"\>113,500\<\/span\>, \<span class=\"tah p11\"\>84,868\<\/span\>, \<span class=\"tah p11\"\>16,649\<\/span\>"

# p = re.compile('\<[a-zA-Z]+[^>]+[\>]')
# p = re.compile('(\<[a-zA-Z]+.*class\=\"tah p11\".*[\>])([^<]*)(\<\/[a-zA-Z]+\>)')
# p = re.compile('\<[a-zA-Z]+.*class\=\"tah p11\".*[\>]')
# p = re.compile('\<[a-zA-Z]+.*class\=\"tah p11\".*[\>]')
p = re.compile('\>[0-9,]+')
print(p.findall(str_html))