import requests
from pprint import pprint
import os
import apteka103by as apteka


class SimpleBot:
    def __init__(self, token):
        self.__token = token
        self.__api_url = "https://api.telegram.org/bot{}/".format(token)
        self.__offset = None
        
    def get_updates(self, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': self.__offset}
        resp = requests.get(self.__api_url + method, params)
        result_json = resp.json()['result']
        return result_json
    
    def get_last_update(self):
        updates = self.get_updates()

        while updates == []:
            updates = self.get_updates()

        last_update = updates[-1]
        self.__offset = last_update['update_id'] + 1
        return updates[-1]
    
    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.__api_url + method, params)
        return resp

def main():
    TOKEN = os.environ.get('TOKEN',None)
    if TOKEN == None:
        file = open('./config.txt')
        TOKEN = file.read()
        file.close()
    my_bot = SimpleBot(TOKEN)
#    second_upd = None
    while True:
#        if second_update == None:
#            first_upd = my_bot.get_last_update()
#        else:
#            first_upd = second_upd
        first_upd = my_bot.get_last_update()
        pprint(first_upd)
        first_upd_text = first_upd['message']['text']
        first_upd_id = first_upd['message']['chat']['id']
        try:
            drugs = apteka.find_drugs(first_upd_text)
        except Exception as e:
            my_bot.send_message(first_upd_id,e)
            continue
        drug = drugs[0]
        drug_id = apteka.get_drug_id(drug['url'])
#        message = apteka.get_result(drug_id)
#        my_bot.send_message(first_upd_id,message)
        result_array = apteka.get_result(drug_id)
        
        for item in result_array:    
            my_bot.send_message(first_upd_id,item)
        
        if result_array[-1] == None:
            my_bot.send_message(first_upd_id,'Нет дополнительной информации \
                                по препарату. \
                                Возможно, препарат отсутствует в продаже \n \
                                или отсутствует описание в принципе \n \
                                Попробуйте один из вариантов:')
            message = ''
            for i in range(len(drugs)):
                message +=( str(i) + '.' + drugs[i]['title']+'\n')
            my_bot.send_message(first_upd_id,message)
                                        
#        second_upd = my_bot.get_last_update()
#        second_upd_id = second_upd['message']['chat']['id']
#        if second_upd_id != first_upd_id:
#            continue            

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
        
        
#%%
    
    
    