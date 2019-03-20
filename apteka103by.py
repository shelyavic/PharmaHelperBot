import requests
from bs4 import BeautifulSoup
#import re


#%%
    
def find_drugs(search_name='синупрет'):
    """
    Function for searhing drugs on 103.by
    Gets string and returns a list of dictionaries:
        [{'title': 'Title0', 'url': '/url0/'},
         {'title': 'Title1', 'url': '/url1/'},
         {'title': 'Title2', 'url': '/url2/'}
         and so on...]
    """
    search_url = 'https://pharmacy-search.103.by/suggest/all?q='
    search_response = requests.get(search_url + search_name)
    search_response_json = search_response.json()
    drugs = search_response_json['data'][0]['entities']
    return drugs

def get_drug_id(drug_url_piece):
    """Returns drug id"""
    drug_url_full = 'https://apteka.103.by' + drug_url_piece + 'minsk/'
    drug_site_response = requests.get(drug_url_full)
    drug_html = drug_site_response.text
    soup = BeautifulSoup(markup=drug_html, features='html.parser')
    
    #find with standart BS function
    tag_st = soup.find('a',attrs={'data-drug':True})
    drug_id = tag_st['data-drug']
    
    """
    #find with regular expression(HARD)
    match = re.search("data-drug=\"(\d+)\"",drug_html)
    print(match.group(1))
    
    #find with regular expression(EASY)
    tag_re = soup.find(re.compile(r"^a"),attrs={'data-drug':re.compile(r"\d+")})
    print('RegExp: ',tag_re)
    print(tag_re['data-drug'])
    
    #find with css selectors
    tag_css = soup.select_one('a[data-drug]')
    print(tag_css)
    print(tag_css['data-drug'])
    """
    
    return drug_id

def get_result(drug_id):
    url = 'https://apteka.103.by/api/v2/sku/'
    response = requests.get(url+str(drug_id))
    response_json = response.json()
    drug_passport = response_json['data']['drug']
    result = (drug_passport['title'] + '\n' + 
              "Форма:" + drug_passport['mainForm'] +
              drug_passport['pharmaceuticalForm'] + '\n' +
              "Производитель:" + drug_passport['manufacturer'] +'\n' +
              'Международное непатентованное название (МНН):' +
              drug_passport['mnn'] + '\n' +
              'Фармакотерапевтическая группа (ФТГ):' +
              drug_passport['ftg'] + '\n\n' +
              'Инструкция по применению:' + '\n')
#    print(drug_passport['title'])
#    print("Форма:", drug_passport['mainForm'],drug_passport['pharmaceuticalForm'])
#    print("Производитель:", drug_passport['manufacturer'])
#    print('Международное непатентованное название (МНН):',
#      drug_passport['mnn'])
#    print('Фармакотерапевтическая группа (ФТГ):',
#      drug_passport['ftg'])
#    print('Инструкция по применению')

    html = response_json['data']['instruction']['text']
    drug_soup = BeautifulSoup(
        markup=html, 
        features='html.parser')
    for tag in drug_soup.find_all(string=True):
        result+=(tag.string+'\r')
    return result


#%%
#drug_input = str(input("Какое лекарство будем искать?\n"))
#drugs = search_drug(drug_input)
#for i in range(len(drugs)):
#    print(i, '.', drugs[i]['title'], sep='')
#    
#choice = int(input())
#drug_url_piece = drugs[choice]['url']
#drug_id = get_drug_id(drug_url_piece)
#result = get_result(drug_id)
#print(result)
#
#




