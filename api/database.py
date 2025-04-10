import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        dbname="classification",
        user="mba",
        password="mba2025",
        host="postgres"
    )

def get_prediction(order_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT description, corretiva, melhoria FROM predictions WHERE id = %s", (order_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row