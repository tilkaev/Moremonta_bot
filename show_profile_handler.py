from bot_data import *
from authorization import login

# SHOW PROFILE
#@bot.message_handler(commands=['profile'])
def show_profile_handler(message):
    chat_id = message.chat.id

    #user_context_state[chat_id] = StateBot.Profile

    if login(message):
        return
        
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
    

