import requests
from pprint import pprint

import apteka103by as apteka


TOKEN = ""
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

        

#greetings = ('здравствуй', 'привет', 'ку', 'здорово')
#now = datetime.datetime.now()


def main():
    my_bot = SimpleBot(TOKEN)
    while True:
        last_update = my_bot.get_last_update()
        pprint(last_update)
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        drugs = apteka.find_drugs(last_chat_text)
        message = ''
        for i in range(len(drugs)):
            message +=( str(i) + '.' + drugs[i]['title']+'\n')
        my_bot.send_message(last_chat_id,message)
                
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
        
        
#%%
import apteka103by as apteka
drugs = apteka.find_drugs()
    
    
    
    