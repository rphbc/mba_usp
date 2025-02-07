import time
import pika


while True:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost",credentials=pika.PlainCredentials("guest", "guest")))
    channel = connection.channel()
    channel.queue_declare(queue="mba_usp", durable=True)
    channel.basic_publish(exchange="", routing_key="mba_usp", body="Processar mensagem! + ueba")
    connection.close()
    time.sleep(5)