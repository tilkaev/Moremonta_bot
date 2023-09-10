from bot_data import *
from authorization import login
from models import *
import json
from bot_data import user_context_confirm_delivery
from data_operations import *
import time

user_context_order = {}

def delivery_handler(message):
    chat_id = message.chat.id

    # Если будут разногласие
    if chat_id not in user_context_confirm_delivery:
        bot.send_message(chat_id, "Выберите телефон для заказа доставки!")
        return
    else:
        device_id = user_context_confirm_delivery[chat_id]["device_id"]

    # Сначала мы предоставляем данные по адресу доставки и номера телефона на проверку клиенту 
    if user_context_confirm_delivery[chat_id]["step"] == StateDelivery.Сonfirmation: 
        user = get_user_by_telegram_id(chat_id)

        text = f"""Пожалуйста, подтвердите, что информация о доставке верна ✅:

📱 {get_device_by_id(device_id).name}
🛠 Переклей (замена стекла)
💲 Цена: {get_price_by_device_id(device_id)[0].price}₽
📍 Адрес: {user.street}
☎️ Телефон: {user.phone}

Если все верно, нажмите 'Вызвать курьера 🛴✅', если нет - уточните нужную информацию. 
        
Как только вы подтвердите информацию, мы обработаем ваш заказ и отправим вам сообщение с подтверждением ✅"""

        user_context_order[chat_id] = {
            "device_id": device_id,
            "price_id": get_price_by_device_id(device_id)[0].id,
            "price": get_price_by_device_id(device_id)[0].price,
            "street": user.street,
            "phone": user.phone
        }
        
        
        callback_data_1 = json.dumps({"callback": "[DELIVERY]", "args": [chat_id, "arg1_value", "arg2_value"]})
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton(text=f"Вызвать курьера 🛴✅", callback_data=f"[DELIVERY][Confirmed]"),
            types.InlineKeyboardButton(text=f"Уточнить адрес 📍", callback_data="[EditAddress]"),
            types.InlineKeyboardButton(text=f"Уточнить телефон ☎️", callback_data="[EditPhone]"),
            types.InlineKeyboardButton(text=f"ОТМЕНА", callback_data="[BACK]")
        ]
        keyboard.add(*buttons)

        bot.send_message(chat_id, text, reply_markup=keyboard)


    # Подтверждение
    elif user_context_confirm_delivery[chat_id]["step"] == StateDelivery.Confirmed: 
        order = user_context_order[chat_id]
        user = get_user_by_telegram_id(chat_id)

        query = """INSERT INTO Orders (
            [user_id]
           ,[master_prices_id]
           ,[pickup_address]
           ,[price]
           ,[order_status_id]
           ,[created_at]) 
		   OUTPUT Inserted.ID
           VALUES (?, ?, ?, ?, ?, GETDATE())"""
        
        params = (get_user_by_telegram_id(chat_id).id, order["price_id"], order["street"], int(order["price"]), 1)
        result = db.execute_query(query, params)
        
        text = f"""Заказ №{result[0][0]} успешно создан ✅
Информация по заказу:

📱 {get_device_by_id(device_id).name}
🛠 Переклей (замена стекла)
💲 Цена: {get_price_by_device_id(device_id)[0].price}₽
📍 Адрес: {user.street}
☎️ Телефон: {user.phone}

В скором времени мы подтвердим ваш заказ и пришлем уведомление ✅"""

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton(text=f"Позвоните мне ☎️", callback_data=f"[ORDER][CALL_ME]"),
            types.InlineKeyboardButton(text=f"Отменить заказ", callback_data="[ORDER][REJECTION]"),
            types.InlineKeyboardButton(text=f"Скрыть", callback_data="[BACK]")
        ]
        keyboard.add(*buttons)

        user_context_confirm_delivery.pop(chat_id)
        user_context_state[chat_id] = None

        bot.edit_message_text(chat_id=chat_id, message_id=message.id, text=text, reply_markup=keyboard)



    # 
    elif user_context_confirm_delivery[chat_id]["step"] == StateDelivery.EditPhone: 
        pass
        

    # 
    elif user_context_confirm_delivery[chat_id]["step"] == StateDelivery.EditAddress: 
        pass




    return

    if 1:
        pass

    elif user_context_registration[chat_id]["step"] == "name":
        if message.text == "Профиль не прошел регистрацию! Пройдите регистрацию повторно.":  # Костыль #
            bot.send_message(chat_id, "Имя не может быть пустым. Повторите!")
        elif len(message.text) >= 100:
            bot.send_message(chat_id, "Имя не может быть длинным. Повторите!")
        else:
            user_context_registration[chat_id]["name"] = message.text
            user_context_registration[chat_id]["step"] = "phone"
            bot.send_message(
                chat_id, "Укажите ваш номер телефона в формате\n+79999999999"
            )

    elif user_context_registration[chat_id]["step"] == "phone":
        phone_number = message.text.replace(" ", "")
        if re.match(r"^\+7\d{10}$", phone_number) == None:
            bot.send_message(
                chat_id, "Ошибка. Укажите номер в формате\n+79999999999")
        else:
            user_context_registration[chat_id]["phone"] = message.text
            user_context_registration[chat_id]["step"] = "street"
            # bot.send_message(chat_id, 'Укажите ваш адрес для курьерской доставки')
            bot.send_message(
                chat_id,
                "Укажите адрес для курьерской доставки, где мы заберем и вернем телефон после ремонта.\n(Адрес можно будет изменить при заказе)",
            )  # , мы гарантируем безопасность и конфиденциальность

    elif user_context_registration[chat_id]["step"] == "street":
        if message.text == "Профиль не прошел регистрацию! Пройдите регистрацию повторно.":  # Костыль #
            bot.send_message(chat_id, "Адрес не может быть пустым. Повторите!")
        elif len(message.text) >= 100:
            bot.send_message(
                chat_id, "Адрес не может быть длиннее 100 символов. Повторите!"
            )

        else:
            user_context_registration[chat_id]["street"] = message.text

            name = user_context_registration[chat_id]["name"]
            phone = user_context_registration[chat_id]["phone"]
            street = user_context_registration[chat_id]["street"]

            # db.execute(f"update U set U.name = '{name}', U.phone = '{phone}', U.street = '{street}', U.is_registered = 1 from Users U where U.telegram_id = '{chat_id}'")
            query = "UPDATE Users SET name=?, phone=?, street=?, is_registered=1 WHERE telegram_id=?"
            params = (name, phone, street, chat_id)
            db.execute(query, params)

            bot.send_message(chat_id, f"Спасибо за регистрацию")
            bot.send_message(
                chat_id, "Вы можете просмотреть и изменить свой профиль введя команду /profile"
            )

            del user_context_registration[chat_id]
            user_context_state[chat_id] = StateBot.PhonePriceSearch
            bot.send_message(
                chat_id, "Вы можете также узнать примерную стоимость ремонта своего телефона, просто написав мне его модель"
            )