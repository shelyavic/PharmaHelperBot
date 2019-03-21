# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 22:28:27 2019

@author: ilyas
"""

import re
#%%
result = re.findall(r'\w.\b\w', 'AV is largest Analytics community of India')
print(result)
#%%
result = re.findall(r'@(\w+).(\w+)', 'abc.test@gmail.com, xyz@test.in, test.first@analyticsvidhya.com, first.test@rest.biz')
print(result)
#%%
result = re.findall(r'[aeiouAEIOU]\w+', 'AV is largest Analytics community of India')
print(result)
#%%
li = ['9999999999', '999999-999', '99999x9999']

for val in li:
    if re.match(r'[89]{1}[0-9]{9}', val) and len(val) == 10:
        print ('yes')
    else:
        print ('no')
#%%
line = 'asdf fjdk;afed,fjek,asdf,foo' # String has multiple delimiters (";",","," ").
result = re.findall(r'[^;,\s]+', line)
print (result)















#%%
html_doc = """
<html>
<head>
<title>The Dormouse's story</title>
</head>
<body>
    <p class="title"><b>The Dormouse's story</b></p>
    <p class="wrapper">
        <p class="story">
            Once upon a time there were three little sisters; and their names
            , →were <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>, 
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
            and <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>; 
            and they lived at the bottom of a well.
        </p>
    </p>
    <p class="story">...</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.prettify())
print()
#%%
a_string = soup.find(string="Lacie")
print(a_string) # u'Lacie'
print()
print(a_string.find_parents("a")) # [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
print()
print(a_string.find_parent("p")) # <p class="story">Once upon a time there were three little sisters; and their names
print()                            #, →were # <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>; # and they lived at the bottom of a well.</p>
print(a_string.find_parents("p")) # []
#%%
first_link = soup.a 
print(first_link) # <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
print()
print(first_link.find_all_next()) # [u'Elsie', u',\n', u'Lacie', u' and\n', u'Tillie', # u';\nand they lived at the bottom of a well.', u'\n\n', u'...', u'\n']
print()
print(first_link.find_next('p')) # <p class="story">...</p>
#%%
soup.select("title") # [<title>The Dormouse's story</title>]
#%%
soup.select("p:nth-of-type(3)") # [<p class="story">...</p>]
#%%
soup.select("body p") 
#%%
soup.select("body a")

#%%
soup.select("#link2 ~ .sister") 

#%%
soup.select("#link1 + .sister")

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
#%%

from bs4 import BeautifulSoup
file = open('sinupret.html',encoding='UTF-8')
soup = BeautifulSoup(file)
file.close()
#%%



#import gc
print(soup.prettify())
tag = soup.find
print(tag,'\n')
print(tag.attrs,'\n')
print(tag['class'],'\n')
print(type(tag.string),'\n')
print(str(tag.string),'\n')
tag.string.replace_with('Саня хуй соси')
print(tag.string,'\n')
print('==================')
head_tag = soup.head
print(type(head_tag.contents),'\n')
print(type(head_tag.children),'\n')
print(type(soup.descendants))















#%%
html_test = """
<html>
    <a>a1
        <b>b1
        <c>c1</c>
        <b>
        <b>b2
        <c>c2</c>
        </b>
    </a>
    <a>a2
        <d>d1
            <e>e1</e>
        </d>
    </a>
    <b>b3</b>
</html>
"""
from bs4 import BeautifulSoup
soup_test = BeautifulSoup(html_test, 'html.parser')
#%%
soup_test.select('html b')
#%%
soup_test.select()
#%%
