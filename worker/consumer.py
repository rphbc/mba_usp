# worker/consumer.py
import time
from joblib import load
from utils import final_pre_process
from common.schema import OrderMessage
import pika, json
import pandas as pd

from database import save_prediction

model = load('modelo.joblib')
tranf = load('transf.joblib')


def connect_to_rabbitmq(retries=10, delay=5):
    for attempt in range(retries):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-mba-usp'))
            channel = connection.channel()
            return connection, channel
        except pika.exceptions.AMQPConnectionError:
            print(f"Tentativa {attempt+1}/{retries} falhou. Tentando novamente em {delay}s...")
            time.sleep(delay)
    raise Exception("Não foi possível conectar ao RabbitMQ após várias tentativas.")

conn, ch = connect_to_rabbitmq()
ch.queue_declare(queue='orders')
ch.queue_declare(queue='results')

def callback(ch, method, properties, body):
    msg = json.loads(body)
    msg = json.loads(msg)
    desc_clean = final_pre_process(msg["description"])
    transf_desc = tranf.transform(pd.Series([desc_clean]))
    pred = model.predict_proba(transf_desc)[0]

    save_prediction(
        order_id=msg["id"],
        description=msg["description"],
        corretiva=float(pred[0]*100),
        melhoria=float(pred[1]*100)
    )

ch.basic_consume(queue='orders', on_message_callback=callback, auto_ack=True)
print("Worker aguardando mensagens...")
ch.start_consuming()