from models import *
from bot_data import db



def get_user_by_telegram_id(telegram_id)-> User:
    query_profile = "select id, name, phone, street from Users where telegram_id = ?"
    result = db.execute_query(query_profile, (telegram_id))
    user = User()
    user.id = result[0]
    user.name = result[1]
    user.phone = result[2]
    user.street = result[3]
    return user


def get_device_by_id(device_id) -> Device:
    query = "select * from Devices where Devices.id = ?"
    params = device_id
    result_device = db.execute_query(query, params)[0]

    device = Device()
    device.id = result_device[0]
    device.name = result_device[1]
    return device
    

def get_price_by_device_id(device_id) -> list:
    query = "select MPrice.id, Serv.name, MPrice.price from MasterPrice MPrice join Services Serv on MPrice.service_id = Serv.id where device_id = ?"
    params = device_id
    result_price = db.execute_query(query, params)

    price = []
    for i in result_price:
        mp = MasterPrice()
        mp.id = i[0]
        mp._service_name = i[1]
        mp.price = i[2]
        price.append(mp)

    print("#", device_id, result_price)
    return price




