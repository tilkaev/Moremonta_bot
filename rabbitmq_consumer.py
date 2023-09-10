import pika, json, time
from bot import bot
import threading

'''
Body style (JSON)

JSON = '{"order_id": 2222, "chat_id": "123213123", "status_name": "Ready!"}'

data = json.loads(json_string)
'''

class RabbitMQConsumer:
    def __init__(self, host, queue):
        self.host = host
        self.queue = queue
        time.sleep(2)

    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = connection.channel()

        # 1 
        self.first_start_if_many_message(channel)
        # Other
        channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=True)
        
        print("[RabbitMQ] Start listening...")
        channel.start_consuming()
        
    def first_start_if_many_message(self, channel):
        unique_massage = {}

        method_frame, header_frame, body = channel.basic_get(queue=self.queue, auto_ack=True)
        while method_frame:
            data = json.loads(body)
            unique_massage[data.get("chat_id")] = data
            method_frame, header_frame, body = channel.basic_get(queue=self.queue, auto_ack=True)

        for data in unique_massage.values():
            text = self.get_text_to_sent(data)
            print(text)
            bot.send_message(chat_id=data["chat_id"], text=text)
            print(f" [x] Received {text}")
            
    def callback(self, ch, method, properties, body):
        if body:
            body = json.loads(body)
            text = self.get_text_to_sent(body)
            bot.send_message(chat_id=body["chat_id"], text=text)
            print(f" [x] Received {text}")

    def get_text_to_sent(self, body):
        if body:
            return str(f"Ваш заказ №{body['order_id']}\nИзменил статус\n{body['status_name']}")
        else:
            return 


consumer = RabbitMQConsumer(host="localhost", queue="moremonta-bot-order-status-changes")
consumer_thread = threading.Thread(target=consumer.run) # Создаем и запускаем поток для работы с RabbitMQ
consumer_thread.start()
