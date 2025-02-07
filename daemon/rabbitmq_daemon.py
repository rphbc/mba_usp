import time
import requests
import pika
import json

DAGSTER_GRAPHQL_ENDPOINT = "http://localhost:3000/graphql"
RABBITMQ_HOST = "localhost"
QUEUE_NAME = "mba_usp"

def trigger_dagster_run():
    """Dispara uma execução do pipeline Dagster"""
    query = {
        "query": """
        mutation TriggerRun {
            launchPipelineExecution(
                executionParams: {
                    selector: { 
                        repositoryLocationName: "mba_usp_dagster_project", 
                        repositoryName: "mba_usp_dagster_project", 
                        jobName: "rabbitmq_pipeline" 
                    },
                    mode: "default"
                }
            ) {
                __typename
            }
        }
        """
    }

    response = requests.post(DAGSTER_GRAPHQL_ENDPOINT, json=query)
    if response.status_code == 200:
        print("✅ Dagster execution triggered successfully!")
    else:
        print(f"❌ Failed to trigger Dagster: {response.text}")

def on_message_received(ch, method, properties, body):
    """Callback quando uma mensagem chega na fila"""
    message = body.decode("utf-8")
    print(f"📩 Mensagem recebida: {message}")
    
    # Aciona o Dagster
    trigger_dagster_run()

    # Confirma recebimento da mensagem
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_rabbitmq_listener():
    """Inicia o listener que monitora o RabbitMQ"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message_received)

    print(f"🔍 Aguardando mensagens na fila '{QUEUE_NAME}'...")
    channel.start_consuming()

if __name__ == "__main__":
    while True:
        try:
            start_rabbitmq_listener()
        except Exception as e:
            print(f"❌ Erro no RabbitMQ Listener: {e}")
            time.sleep(5)  # Aguarda antes de tentar reconectar
