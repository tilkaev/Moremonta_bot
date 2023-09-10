from bot_data import *
from authorization import login
from handlers.find_phone_price_handler import find_phone_price_handler

# ALL MESSAGE
# Эхо-обработчик для всех остальных сообщений
def echo_all_handler(message):
    chat_id = message.chat.id

    if chat_id not in user_context_state:
        user_context_state[chat_id] = StateBot.PhonePriceSearch
        find_phone_price_handler(message)
        return

    if login(message) == False:
       return

    
