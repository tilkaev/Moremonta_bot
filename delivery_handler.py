from bot_data import *
from authorization import login
from models import *
import json



def delivery_handler(message):
    chat_id = message.chat.id

    device_id = None
    # На всякий случай если будут разногласия
    if chat_id not in user_context_confirm_delivery:
        bot.send_message(chat_id, "Выберите телефон для заказа доставки!")
        return
    
    # Сначала мы предоставляем данные по адресу доставки и номера телефона на проверку клиенту 
    elif user_context_confirm_delivery[chat_id]== StateDelivery.Сonfirmation: 
        query_profile = "select name, phone, street from Users where telegram_id = ?"
        params = (message.chat.id)
        result_profile = db.execute_query(query_profile, params)

        text = f"""Пожалуйста, подтвердите, что информация о доставке верна ✅: 
        📍 Адрес: {result_profile[0][2]},
        ☎️ Телефон: {result_profile[0][1]}. 
        Если все верно, нажмите 'Все верно', если нет - уточните нужную информацию. 
        
        Как только вы подтвердите информацию, мы обработаем ваш заказ и отправим вам сообщение с подтверждением ✅"""
        
        
        callback_data_1 = json.dumps({"callback": "[DELIVERY]", "args": [chat_id, "arg1_value", "arg2_value"]})
        keyboard = types.InlineKeyboardMarkup()
        delivery_button = types.InlineKeyboardButton(text=f"Все верно, продолжить 🛴", callback_data=f"[DELIVERY][device_id]{device.id}")
        callback_button = types.InlineKeyboardButton(text=f"Уточнить адрес", callback_data="[BACK]")
        callback_button = types.InlineKeyboardButton(text=f"Уточнить телефон", callback_data="[BACK]")
        callback_button = types.InlineKeyboardButton(text=f"ОТМЕНА", callback_data="[BACK]")
        keyboard.add(delivery_button)
        keyboard.add(callback_button)


        bot.send_message(message.chat.id, text, reply_markup=keyboard)
        bot.send_message(chat_id, "        !")

    # 
    elif user_context_confirm_delivery[chat_id]== StateDelivery.EditPhone: 
        pass

    # 
    elif user_context_confirm_delivery[chat_id]== StateDelivery.EditAddress: 
        pass



    # Подтверждаем
    elif user_context_confirm_delivery[chat_id]== StateDelivery.Confirmed: 
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