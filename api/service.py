import json
import os
import time
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from joblib import load
import pandas as pd
import pika
from pydantic import BaseModel
from common.schema import OrderMessage

from database import get_prediction


# model = load('modelo.joblib')
# tranf = load('transf.joblib')


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:63342",
    "*"
]

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def serve_index():
    file_path = os.path.join("static", "index.html")
    return FileResponse(file_path)

def publish_to_queue(body: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-mba-usp'))
    channel = connection.channel()
    channel.queue_declare(queue='orders')
    channel.basic_publish(exchange='', routing_key='orders', body=json.dumps(body))
    connection.close()

def get_result_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-mba-usp'))
    channel = connection.channel()
    channel.queue_declare(queue='results')
    method_frame, header_frame, body = channel.basic_get(queue='results')
    connection.close()
    return body

class OrderRequest(BaseModel):
    description: str

@app.post("/order/")
async def create_order(request: OrderRequest):
    order_id = str(uuid.uuid4())
    description = request.description
    msg = OrderMessage(id=order_id, description=description).model_dump_json()
    publish_to_queue(msg)
    return {"message": "Ordem enviada", "order_id": order_id}


@app.get("/order/result/{order_id}")
async def get_result(order_id: str):
    row = get_prediction(order_id)
    if row:
        return {
            "description": row[0],
            "corretiva": row[1],
            "melhoria": row[2]
        }
    return {"message": "Resultado ainda não disponível"}