import telebot
from MSSQL import MSSQL
from telebot import types
import time
from helpers import *
from enums import *
import re
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
db = MSSQL()

user_context_registration = {}
user_context_state = {}



# START HELP
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    #user_id = message.chat.id
    bot.reply_to(message, "Привет, я бот Moremonta!")

    user_context_state[message.chat.id] = StateBot.Start
    if message.chat.id in user_context_registration:
        del user_context_registration[message.chat.id]

    if login(message):
        print("#Authorized")


# REGISTRATION
# State registration 
@bot.message_handler(func=lambda message: message.chat.id in user_context_state and user_context_state[message.chat.id] == StateBot.Registration)
def registration_state(message):
    chat_id = message.chat.id
    user_context_state[message.chat.id] = StateBot.Registration

    if chat_id not in user_context_registration:
        user_context_registration[chat_id] = {'name': None, 'phone': None, 'street': None,  'step': 'name'}
        bot.send_message(chat_id, 'Для регистрации укажите ваше имя')

    elif user_context_registration[chat_id]['step'] == 'name':
        if len(message.text) >= 100:
            bot.send_message(chat_id, 'Имя не может быть длинным. Повторите!')
        else:
            user_context_registration[chat_id]['name'] = message.text
            user_context_registration[chat_id]['step'] = 'phone'
            bot.send_message(chat_id, 'Укажите ваш номер телефона в формате\n+79999999999')

    elif user_context_registration[chat_id]['step'] == 'phone':
        phone_number = message.text.replace(" ", "")
        if re.match(r'^\+7\d{10}$', phone_number) == None:
            bot.send_message(chat_id, 'Ошибка. Укажите номер в формате\n+79999999999')
        else:
            user_context_registration[chat_id]['phone'] = message.text
            user_context_registration[chat_id]['step'] = 'street'
            bot.send_message(chat_id, 'Укажите ваш адрес доставки')
        

    elif user_context_registration[chat_id]['step'] == 'street':
        if len(message.text) >= 100:
            bot.send_message(chat_id, 'Адрес не может быть длиннее 100 символов. Повторите!')
        
        else:                    
            user_context_registration[chat_id]['street'] = message.text

            name = user_context_registration[chat_id]['name']
            phone = user_context_registration[chat_id]['phone']
            street = user_context_registration[chat_id]['street']

            #db.execute(f"update U set U.name = '{name}', U.phone = '{phone}', U.street = '{street}', U.is_registered = 1 from Users U where U.telegram_id = '{chat_id}'")
            query = "UPDATE Users SET name=?, phone=?, street=?, is_registered=1 WHERE telegram_id=?"
            params = (name, phone, street, chat_id)
            db.execute(query, params)
            
            bot.send_message(chat_id, f"Спасибо за регистрацию")
            show_profile(message)
            del user_context_registration[chat_id]
            user_context_state[message.chat.id] = StateBot.Profile
        


def login(message):
    query = "select is_registered from Users where telegram_id = ?"
    params = (message.chat.id)
    query_user_step = db.execute_query(query, params)

    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="РЕГИСТРАЦИЯ", callback_data="[REGISTRATION]")
    keyboard.add(callback_button)

    if query_user_step == []:  # Если пользователь не создан создаем
        bot.send_message(message.chat.id, "Вы не зарегистрированный пользователь, пожалуйста пройдите регистрацию!", reply_markup=keyboard)
        #Создаем пользователя с этапом start
        
        query = "insert into Users (type_id, telegram_id, is_registered, name) values (3, ?, 0,  'start')"
        params = (message.chat.id)
        db.execute(query, params)


    elif query_user_step[0][0] == False: # Пользовательсоздан без авторизации
       bot.send_message(message.chat.id, "Профиль не прошел регистрацию! Пройдите регистрацию повторно.", reply_markup=keyboard)
       
        
    else: # Пользователь авторизован
        return True
    
    return False
        



    
        
        
    #ent_message = bot.send_message(message.chat.id, "Выберите подоходящий телефон:", reply_markup=keyboard)
        
    # step: ['start', 'name', 'phone', 'street', 'pass']
    #if query_user_step != 'pass':
    #    registration(message, query_user_step)


# SHOW PROFILE
@bot.message_handler(commands=['profile'])
def show_profile(message):

    if login(message):
        keyboard = types.InlineKeyboardMarkup()
        but_chg = types.InlineKeyboardButton(text="Изменить данные", callback_data="[EDIT_PROFILE]")
        callback_button = types.InlineKeyboardButton(text=f"ОТМЕНА", callback_data="[BACK]")
        keyboard.add(but_chg)
        keyboard.add(callback_button)

        '''but_chg_name = types.InlineKeyboardButton(text="Имя", callback_data="[EDIT_PROFILE]name")
        but_chg_phone = types.InlineKeyboardButton(text="Телефон", callback_data="[EDIT_PROFILE]phone")
        but_chg_street = types.InlineKeyboardButton(text="Адрес", callback_data="[EDIT_PROFILE]street")
        callback_button = types.InlineKeyboardButton(text=f"ОТМЕНА", callback_data="[BACK]")
        keyboard.add(but_chg_name)
        keyboard.add(but_chg_phone)
        keyboard.add(but_chg_street)'''

        query_profile = "select name, phone, street from Users where telegram_id = ?"
        params = (message.chat.id)
        result_profile = db.execute_query(query_profile, params)
        
        bot.send_message(message.chat.id, f"Ваш профиль: \nИмя: {result_profile[0][0]}\nТелефон: {result_profile[0][1]}\nАдрес: {result_profile[0][2]}", reply_markup=keyboard)
    


# CALLBACK
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    text = call.data
    chat_id = call.message.chat.id

    if text == "[BACK]":
        bot.delete_message(chat_id, call.message.message_id)

    elif text == "[REGISTRATION]":
        registration_state(call.message)
        bot.delete_message(chat_id, call.message.message_id)

    elif text == "[EDIT_PROFILE]":
        db.execute("UPDATE Users SET is_registered=0 WHERE telegram_id=?", chat_id)
        bot.send_message(chat_id, "Для изменения данных пройдите авторизацию повторно")
        user_context_state[chat_id] = StateBot.Registration
        bot.delete_message(chat_id, call.message.message_id)
        registration_state(call.message)
        
    elif call.data[:8] == '[DEVICE]':
        text = call.data[8:]
        #bot.answer_callback_query(callback_query_id=call.id, text='Вы нажали на кнопку с callback-данными "test"')
        bot.send_message(chat_id, text)
        bot.delete_message(chat_id, call.message.message_id)
    
    



   



@bot.message_handler(commands=['menu'])
def show_menu(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text='Кнопка 1', callback_data='button1')
    button2 = telebot.types.InlineKeyboardButton(text='Кнопка 2', callback_data='button2')
    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)

   


# ALL MESSAGE
@bot.message_handler(func=lambda message: True)
def echo_all(message):

    query_profile = "select Ds.name from Brands Br, Devices Ds where Br.id = Ds.brand_id and Ds.name like ?"
    params = f"%{str(message.text).replace(' ', '%')}%"
    result_devices = db.execute_query(query_profile, params)

    result_devices = [i[0] for i in result_devices]
    print("#", result_devices)

    if len(result_devices) > 10:
        bot.reply_to(message, f"{message.text} - не могу найти телефон в базе!")

    elif len(result_devices) > 1:
        #result =  difflib_searcher(message.text, query_devices)
        #bot.reply_to(message, "{0}\n - выберите из этого списка!".format( "\n".join(query_devices) ))

        keyboard = types.InlineKeyboardMarkup()
        for device in result_devices:
            callback_button = types.InlineKeyboardButton(text=f"{device}", callback_data=f"[DEVICE]{device}")
            keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text=f"ОТМЕНА", callback_data="[BACK]")
        keyboard.add(callback_button)

        sent_message = bot.send_message(message.chat.id, "Выберите подоходящий телефон:", reply_markup=keyboard)
                
    elif len(result_devices) == 1:
        bot.reply_to(message, "{0} - этот телефон есть в базе!".format(result_devices[0]))

    else:
        bot.reply_to(message, "{0} - такого телефона нету в базе!".format(message.text))
        

        
    '''
    # First finding brand
    query_brands = db.select("select name, id from Brands")
    print(query_brands)
    temp = [i[0] for i in query_brands]
    result =  difflib_searcher(message.text.split()[0], temp)
    
    if result is None:
        bot.reply_to(message, f"{message.text} - не могу найти телефон в базе!")
        return
    
    index = 0
    for i, item in enumerate(query_brands):
        if item[0] == result:
            index = item[1]
            break
    
    # Second finding device
    #query_devices = db.select(f"select name from Devices where brand_id = {index}")
    query_devices = db.select("select Ds.name from Brands Br, Devices Ds where brand_id = {0} and  Br.id = Ds.brand_id and Ds.name like '%{1}%'".format(index, message.text.replace(" ", "%")))
    query_devices = [i[0] for i in query_devices]
    print(query_devices) 
    result =  difflib_searcher(message.text, query_devices)
    
    if result is None:
        bot.reply_to(message, f"{message.text} - не могу найти телефон в базе!")
        return

    bot.reply_to(message, "{0} - такой телефона есть в базе!".format(result[0]))'''

    '''
    query = "select Ds.name from Brands Br, Devices Ds where Br.id = Ds.brand_id and Ds.name like '%{0}%'".format(str(message.text).replace(" ", "%"))
    result = db.select(query)
    
    if result != [] and len(result)<=10:
        bot.reply_to(message, "{0} - такой телефона есть в базе!".format(result[0]))
    else:
        bot.reply_to(message, "{0} - такого телефона нет в базе!".format(message.text))'''





bot.polling()
