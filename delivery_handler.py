from bot_data import *
from authorization import login
from models import *
import json
from bot_data import user_context_confirm_delivery
from data_operations import *

user_context_order = {}

def delivery_handler(message):
    chat_id = message.chat.id

    # На всякий случай если будут разногласия
    if chat_id not in user_context_confirm_delivery:
        bot.send_message(chat_id, "Выберите телефон для заказа доставки!")
        return
    else:
        device_id = user_context_confirm_delivery[message.chat.id]["device_id"]

    # Сначала мы предоставляем данные по адресу доставки и номера телефона на проверку клиенту 
    if user_context_confirm_delivery[chat_id]["step"] == StateDelivery.Сonfirmation: 
        user = get_user_by_telegram_id(chat_id)

        text = f"""Пожалуйста, подтвердите, что информация о доставке верна ✅: 
📱 {get_device_by_id(device_id).name}
🛠 Переклей (замена стекла)
💲 Цена: {get_price_by_device_id(device_id)[0].price}
📍 Адрес: {user.street},
☎️ Телефон: {user.phone}

Если все верно, нажмите 'Вызвать курьера 🛴', если нет - уточните нужную информацию. 
        
Как только вы подтвердите информацию, мы обработаем ваш заказ и отправим вам сообщение с подтверждением ✅"""
        
        
        callback_data_1 = json.dumps({"callback": "[DELIVERY]", "args": [chat_id, "arg1_value", "arg2_value"]})
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton(text=f"Вызвать курьера 🛴", callback_data=f"[DELIVERY][Confirmed]"),
            types.InlineKeyboardButton(text=f"Уточнить адрес 📍", callback_data="[EditAddress]"),
            types.InlineKeyboardButton(text=f"Уточнить телефон ☎️", callback_data="[EditPhone]"),
            types.InlineKeyboardButton(text=f"ОТМЕНА", callback_data="[BACK]")
        ]
        keyboard.add(*buttons)

        bot.send_message(message.chat.id, text, reply_markup=keyboard)


    # 
    elif user_context_confirm_delivery[chat_id]["step"] == StateDelivery.EditPhone: 
        query_profile = "select name, phone, street from Users where telegram_id = ?"
        params = (message.chat.id)
        result_profile = db.execute_query(query_profile, params)
        query = """INSERT INTO Orders (
            [user_id]
           ,[master_prices_id]
           ,[pickup_address]
           ,[price]
           ,[order_status_id]
           ,[created_at]
            values (?, ?, ?, ?, ?, ?)"""
        price = get_price_by_device_id(user_context_confirm_delivery[message.chat.id]["device_id"])
        params = (message.chat.id, price[0].id, chat_id)
        db.execute(query, params)
        

    # 
    elif user_context_confirm_delivery[chat_id]["step"] == StateDelivery.EditAddress: 
        pass



    # Подтверждаем
    elif user_context_confirm_delivery[chat_id]["step"] == StateDelivery.Confirmed: 
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
            user_context_state[message.chat.id] = StateBot.PhonePriceSearch
            bot.send_message(
                chat_id, "Вы можете также узнать примерную стоимость ремонта своего телефона, просто написав мне его модель"
            )