
#%%

import os
import telebot
import apteka103by as parser
from Task import Task
import markups as m

TOKEN = os.environ.get('TOKEN',None)
if TOKEN == None:
    file = open('./config.txt',mode='r')
    TOKEN = file.read()
    file.close()

bot = telebot.TeleBot(TOKEN)
task = Task()


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id , 'Привет могу найти информацию по лекарству на сайте 103.by')
    if not task.isRunning:
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, 'Сколько тебе лет?')
        bot.register_next_step_handler(msg, askAge) #askSource
        task.isRunning = True

def askAge(message):
    chat_id = message.chat.id
    text = message.text
    if not text.isdigit():
        msg = bot.send_message(chat_id, 'Возраст должен быть числом, введи ещё раз.')
        bot.register_next_step_handler(msg, askAge) #askSource
        return
    bot.send_message(chat_id, 'Спасибо, я запомнил что тебе ' +
                     text + ' лет.', reply_markup=m.start_markup)
    task.isRunning = False

@bot.message_handler(commands=['find'])
def find_handler(message):
    msg = bot.send_message(message.chat.id,'Какое лекарство будем искать?')
    bot.register_next_step_handler(msg,find_drugs)
    task.isRunning = True

def find_drugs(message):
    chat_id = message.chat.id
    try:
        task.drugs = parser.find_drugs(message.text)
    except Exception as e:
        bot.send_message(chat_id, e)
        task.isRunning = False
    else:
        mess = ''
        for i in range(len(task.drugs)):
            mess += str(i)+'. ' + task.drugs[i]['title'] + '\n'
        msg = bot.send_message(message.chat.id, mess)
        bot.register_next_step_handler(msg,make_choice_and_find_drug)
        task.isRunning = True

def make_choice_and_find_drug(message):
    chat_id = message.chat.id
    text = message.text
    if not text.isdigit() or not (int(text)>=0 and int(text)<len(task.drugs) ) :
        msg = bot.send_message(chat_id,'Введи число от 0'+ ' до '+
                               str(len(task.drugs)-1))
        bot.register_next_step_handler(msg, make_choice_and_find_drug)
        return
    choice = int(text)
    drug_url_piece = task.drugs[choice]['url']
    drug_id = parser.get_drug_id(drug_url_piece)
    result_dict = parser.get_result(drug_id)
    for item in result_dict.items():
        mess = (item[0] + ':' + '\n'+'\n' + item[1])
        bot.send_message(chat_id, mess,reply_markup=m.start_markup)
#    splitted_text = util.split_string(mess, 3000)
#    for text in splitted_text:
#        bot.send_message(chat_id, text,reply_markup=m.start_markup)
    task.isRunning = False

@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.lower()
    chat_id = message.chat.id
    if text == "привет":
        bot.send_message(chat_id, 'Привет, я бот - парсер 103.by .',reply_markup=m.start_markup)
    elif text == "как дела?":
        bot.send_message(chat_id, 'Хорошо, а у тебя?',reply_markup=m.start_markup)
    else:
        bot.send_message(chat_id, 'Прости, я тебя не понял :(',reply_markup=m.start_markup)

@bot.message_handler(content_types=['photo'])
def text_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Красиво.',reply_markup=m.start_markup)

bot.polling(none_stop=True)

#%%
