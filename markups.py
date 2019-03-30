# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 20:16:21 2019

@author: ilyas
"""
from telebot import types

start_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True,
                                         one_time_keyboard=True)
start_markup_btn = types.KeyboardButton('/start')
find_markup_btn = types.KeyboardButton('/find')
start_markup.add(start_markup_btn, find_markup_btn)
