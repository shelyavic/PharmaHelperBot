from time import time
t_start = time()

import requests
from bs4 import BeautifulSoup



def make_drug_url(drug_url):
    return 'https://apteka.103.by' + drug_url + 'minsk/'


search_name = 'уголь'
search_url = 'https://pharmacy-search.103.by/suggest/all?q='
search_response = requests.get(search_url + search_name)
search_response_json = search_response.json()
drugs = search_response_json['data'][0]['entities']

for i in range(len(drugs)):
    print(i, '.', drugs[i]['title'], sep='')

choice = int(input())
print(drugs[choice]['title'])
drug_url_piece = drugs[choice]['url']
drug_url_full = make_drug_url(drug_url_piece)
print(drug_url_full)
drug_site_response = requests.get(drug_url_full)
drug_html = drug_site_response.text
print(drug_html)
print('---------------------------------------------------------------------')
soup = BeautifulSoup(markup=drug_html, features='html.parser')
print(soup.prettify())


t_finish = time()
elapsed = t_finish - t_start
print(elapsed)

#%%
help('fdsa'.find)
#%%
from bs4 import BeautifulSoup
file = open('sinupret.html',encoding='UTF-8')
soup = BeautifulSoup(file)
file.close()
#%%
import gc
print(soup.prettify())
tag = soup.a
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
help()


#for tag in soup.find_all('a'):




