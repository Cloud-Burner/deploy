import pika
import random
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.exchange_declare(exchange='green_board_exchange', exchange_type='headers')
queue_count = 5
for i in range(queue_count):
    queue_name = f"green_board_queue_{i + 1}"
    channel.queue_declare(queue=queue_name)
    channel.queue_bind(exchange='green_board_exchange', queue=queue_name, arguments={"x-match": "all", "board": "green"})

message = json.dumps({"message": "Message for green board"})
random_queue = f"green_board_queue_{random.randint(1, queue_count)}"
channel.basic_publish(
    exchange='green_board_exchange',
    routing_key=random_queue,
    body=message,
    properties=pika.BasicProperties(
        headers={'board': 'green'}
    )
)

print(f"Sent message to {random_queue} with header 'board=green'")

connection.close()