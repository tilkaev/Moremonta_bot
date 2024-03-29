from bot_data import *
from registration_handler_state import registration_handler_state
from handlers.find_phone_price_handler import *
from handlers.delivery_handler import delivery_handler
from handlers.call_me_handler import *

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


    elif text[:16] == "[ORDER][CALL_ME]":
        text = text[16:]
        user_context_state[chat_id] = None
        call_me_handler(call.message)

    elif text[:22] == "[CALL_ME][SEND_NUMBER]":
        user_context_state[chat_id] = None
        send_my_number(call.message)


    elif text[:21] == "[DELIVERY][device_id]":
        text = text[21:]
        user_context_state[chat_id] = StateBot.Delivery
        user_context_confirm_delivery[chat_id] = {
            "device_id": text,
            "step": StateDelivery.Сonfirmation,
        }
        delivery_handler(call.message)
        
    elif text[:21] == "[DELIVERY][EditAddress]":
        text = text[21:]
        user_context_confirm_delivery[chat_id]["step"] = StateDelivery.EditAddress
        delivery_handler(call.message)

    elif text[:21] == "[DELIVERY][EditPhone]":
        text = text[21:]
        user_context_confirm_delivery[chat_id]["step"] = StateDelivery.EditPhone
        delivery_handler(call.message)

    elif text[:21] == "[DELIVERY][Confirmed]":
        text = text[21:]
        if chat_id not in user_context_confirm_delivery:
            user_context_state[chat_id] = StateBot.PhonePriceSearch
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.id, text="Повторите выбор устройства!")
            return

        user_context_confirm_delivery[chat_id]["step"] = StateDelivery.Confirmed
        delivery_handler(call.message)

