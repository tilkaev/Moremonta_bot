import telebot
from telebot import types
import time
from utils import *
from bot_data import *

from start_help_handler import start_help_handler
from show_profile_handler import show_profile_handler
from registration_handler_state import registration_handler_state
from callback_handler import callback_handler
from echo_all_handler import echo_all_handler



    
bot.callback_query_handler(func=lambda call: True)(callback_handler)
bot.message_handler(func=lambda message: message.chat.id in user_context_state and user_context_state[message.chat.id] == StateBot.Registration)(registration_handler_state)
bot.message_handler(commands=['profile'])(show_profile_handler)
bot.message_handler(commands=['start', 'help'])(start_help_handler)
bot.message_handler(func=lambda message: True)(echo_all_handler)




if __name__ == '__main__':
    bot.polling(none_stop=True)



       


'''
@bot.message_handler(commands=['menu'])
def show_menu(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text='Кнопка 1', callback_data='button1')
    button2 = telebot.types.InlineKeyboardButton(text='Кнопка 2', callback_data='button2')
    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)'''
