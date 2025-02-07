from dagster import AutomationCondition, asset, AssetExecutionContext
import pika

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "mba_usp"

@asset(automation_condition=AutomationCondition.on_cron("*/30 * * * * *"))
def rabbitmq_listener(context: AssetExecutionContext) -> str:
    """Asset que escuta a fila RabbitMQ e processa mensagens"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost",credentials=pika.PlainCredentials("guest", "guest")))
    channel = connection.channel()
    batch_size = 30
    messages = []

    for _ in range(batch_size):
        method_frame, header_frame, body = channel.basic_get(queue=QUEUE_NAME, auto_ack=False)
        if body:
            message = body.decode("utf-8")
            messages.append(message)
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        else:
            break
    
    connection.close()
    
    if messages:
        context.log.info(f"📩 Mensagens recebidas: {', '.join(messages)}")
        return "\n".join(messages)
    else:
        return "Nenhuma mensagem na fila"
