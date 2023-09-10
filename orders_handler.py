from bot_data import *
from authorization import login
from models import *
import json
from bot_data import user_context_confirm_delivery
from data_operations import get_orders_by_user_id
import time



def orders_handler(message):
    chat_id = message.chat.id

    orders = get_orders_by_user_id(chat_id)

    text_orders = ""
    for key, value in orders.items():
        text_orders += f"""
Номер заказа: №{value["order_id"]}
✅ Статус заказа: {value["order_status"]}
📱 {value["device_name"]}
💰 Стоимость: {value["price"]}₽
📅 Дата формирования: {str(value["order_create"])[:11]}\n"""

    text = f"""Ваши активные заказы ✅:\n{text_orders}"""

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text=f"Позвоните мне ☎️", callback_data=f"[ORDER][CALL_ME]"),
        types.InlineKeyboardButton(text=f"Скрыть", callback_data="[BACK]")
    ]
    keyboard.add(*buttons)

    bot.send_message(chat_id, text, reply_markup=keyboard)






