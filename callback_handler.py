from bot_data import *
from registration_handler_state import registration_handler_state
from find_phone_price_handler import *
from delivery_handler import delivery_handler

# CALLBACK
# @bot.callback_query_handler(func=lambda call: True)


def callback_handler(call):
    text = call.data
    chat_id = call.message.chat.id

    if text == "[BACK]":
        bot.delete_message(chat_id, call.message.message_id)

    elif text == "[REGISTRATION]":
        registration_handler_state(call.message)
        bot.delete_message(chat_id, call.message.message_id)

    elif text == "[EDIT_PROFILE]":
        user_context_state[chat_id] = StateBot.Profile
        db.execute(
            "UPDATE Users SET is_registered=0 WHERE telegram_id=?", chat_id)
        bot.send_message(
            chat_id, "Для изменения данных пройдите авторизацию повторно")
        user_context_state[chat_id] = StateBot.Registration
        bot.delete_message(chat_id, call.message.message_id)
        registration_handler_state(call.message)

    elif text[:11] == '[DEVICE_ID]':
        text = call.data[11:]
        user_context_state[chat_id] = StateBot.PhonePriceSearch
        # bot.answer_callback_query(callback_query_id=call.id, text='Вы нажали на кнопку с callback-данными "test"')
        #bot.send_message(chat_id, text)
        #bot.delete_message(chat_id, call.message.message_id)
        send_price_by_device_id(call.message, text)


    elif text[:21] == "[DELIVERY][device_id]":
        text = text[21:]
        user_context_state[chat_id] = StateBot.Delivery
        user_context_confirm_delivery[chat_id] = {
            "device_id": text,
            "step": StateDelivery.Сonfirmation,
        }
        delivery_handler(call.message)

        
    elif text[:21] == "[DELIVERY][Confirmed]":
        text = text[21:]
        user_context_state[chat_id] = StateBot.Confirmed
        delivery_handler(call.message)

