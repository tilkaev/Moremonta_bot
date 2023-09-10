from models import *
from bot_data import db



def get_orders_by_user_id(telegram_id) -> list:
    query = """SELECT Orders.id, Orders.price, Devices.name, OStatus.name, Orders.created_at
FROM Orders
join Users on Users.id = Orders.user_id
join MasterPrice MPrice on  MPrice.id = Orders.master_prices_id
join Devices on Devices.id = MPrice.device_id
join OrderStatuses OStatus on OStatus.id = Orders.order_status_id
where user_id = ? and order_status_id < 9 or Orders.created_at >= DATEADD(day, -1, GETDATE())"""

    result_orders = db.execute_query(query, (get_user_by_telegram_id(telegram_id).id))

    result = {}
    for i, item in enumerate(result_orders):
        result[i] = {
            "order_id": item[0],
            "price": item[1],
            "device_name": item[2],
            "order_status": item[3],
            "order_create": item[4],
        }

    return result

    

def get_user_by_telegram_id(telegram_id)-> User:
    query_profile = "select id, name, phone, street from Users where telegram_id = ?"
    result = db.execute_query(query_profile, (telegram_id))
    user = User()
    user.id = result[0][0]
    user.name = result[0][1]
    user.phone = result[0][2]
    user.street = result[0][3]
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




