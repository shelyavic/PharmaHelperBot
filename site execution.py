import requests
from pprint import pprint

def make_drug_url(drug_url):
    return 'https://apteka.103.by' + drug_url + 'minsk/'

search_name = 'уголь'
search_url = 'https://pharmacy-search.103.by/suggest/all?q='
search_response = requests.get(search_url + search_name)
search_response_json = search_response.json()
drugs = search_response_json['data'][0]['entities']
pprint(drugs)
for i in range(len(drugs)):
    print(i, '.', drugs[i]['title'], sep='')
choice = int(input())
print(drugs[choice]['title'])
drug_url_piece = drugs[choice]['url']
drug_url_full = make_drug_url(drug_url_piece)
print(drug_url_full)
drug_site_response = requests.get(drug_url_full)#ответ на запрос сайта друга
drug_html = drug_site_response.text
print(drug_html)


#%%

