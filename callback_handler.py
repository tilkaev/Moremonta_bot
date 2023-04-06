from bot_data import *
from registration_handler_state import registration_handler_state

# CALLBACK
#@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    text = call.data
    chat_id = call.message.chat.id

    if text == "[BACK]":
        bot.delete_message(chat_id, call.message.message_id)

    elif text == "[REGISTRATION]":
        registration_handler_state(call.message)
        bot.delete_message(chat_id, call.message.message_id)

    elif text == "[EDIT_PROFILE]":
        db.execute("UPDATE Users SET is_registered=0 WHERE telegram_id=?", chat_id)
        bot.send_message(chat_id, "Для изменения данных пройдите авторизацию повторно")
        user_context_state[chat_id] = StateBot.Registration
        bot.delete_message(chat_id, call.message.message_id)
        registration_handler_state(call.message)
        
    elif call.data[:8] == '[DEVICE]':
        text = call.data[8:]
        #bot.answer_callback_query(callback_query_id=call.id, text='Вы нажали на кнопку с callback-данными "test"')
        bot.send_message(chat_id, text)
        bot.delete_message(chat_id, call.message.message_id)
    