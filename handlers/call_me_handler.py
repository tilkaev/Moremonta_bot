from telebot import types
from bot_data import bot


def call_me_handler(message):
    chat_id = message.chat.id

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text=f"Позвоню сам, напиши номер", callback_data=f"[CALL_ME][SEND_NUMBER]"),
        types.InlineKeyboardButton(text=f"Отмена", callback_data="[BACK]")
    ]
    keyboard.add(*buttons)

    text = "Направили запрос на обратный звонок ☎️ по вашему заказу 📦"

    bot.send_message(chat_id, text, reply_markup=keyboard)

def send_my_number(message):
    chat_id = message.chat.id
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text=f"Отмена", callback_data="[BACK]")
    ]
    keyboard.add(*buttons)

    text = "☎️ +7-953-110-93-30 - Клим"

    bot.edit_message_text(chat_id=chat_id, message_id=message.id, text=text, reply_markup=keyboard)

