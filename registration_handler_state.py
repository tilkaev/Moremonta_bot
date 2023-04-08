from bot_data import *
from show_profile_handler import show_profile_handler
import re


def registration_handler_state(message):
    """
    REGISTRATION

    Enum State Bot: Registration = 2
    
    Обработчик сообщений в состоянии регистрации
    """

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
            #bot.send_message(chat_id, 'Укажите ваш адрес для курьерской доставки')
            bot.send_message(chat_id, 'Укажите адрес для курьерской доставки, где забрать и вернуть телефон после ремонта.\nЕго можно будет изменить при заказе') # , мы гарантируем безопасность и конфиденциальность
    
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
            show_profile_handler(message)
            del user_context_registration[chat_id]
            user_context_state[message.chat.id] = StateBot.Profile
        
        
    #ent_message = bot.send_message(message.chat.id, "Выберите подоходящий телефон:", reply_markup=keyboard)
        
    # step: ['start', 'name', 'phone', 'street', 'pass']
    #if query_user_step != 'pass':
    #    registration(message, query_user_step)

