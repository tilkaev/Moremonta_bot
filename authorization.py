from bot_data import *


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
