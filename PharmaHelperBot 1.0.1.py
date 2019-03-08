import datetime
import requests
import openpyxl
from pprint import pprint

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
        
    
class PharmaBot(SimpleBot):
    def __init__(self, token):
        super().__init__(token)
        self.__wb = openpyxl.load_workbook("grls-xlsx-light.xlsx")
        self.__sheet = self.__wb.active
        self.__headers = [cell.value for cell in  self.__sheet[1]]
        self.__drugs_names = [str(cell.value).lower() for cell in self.__sheet['C']]
    
    def find_drug(self,text):
        text = str(text).lower()
        ind = self.__drugs_names.index(text)
        row = [x.value for x in self.__sheet[ind]]
        return zip(self.__headers,row)
        
my_bot = PharmaBot(TOKEN)
greetings = ('здравствуй', 'привет', 'ку', 'здорово')
now = datetime.datetime.now()


def main():
    today = now.day
    hour = now.hour

    while True:

        last_update = my_bot.get_last_update()
        pprint(last_update)
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower() in greetings  and 6 <= hour < 12: #and today == now.day
            my_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings  and 12 <= hour < 17: #and today == now.day
            my_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings: #and today == now.day
            my_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
            today += 1
        else:
            try:
               search_result = my_bot.find_drug(last_chat_text)
            except ValueError:
                my_bot.send_message(last_chat_id,"Can not find {}".format(last_chat_text))
            else:
                for header,cell in search_result:
                    my_bot.send_message(last_chat_id,str(header)+' - '+ str(cell))
                
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
        
        
        
    
    
    
    
    
    
    
    