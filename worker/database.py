import psycopg2

def save_prediction(order_id, description, corretiva, melhoria):
    conn = psycopg2.connect(
        dbname="classification",
        user="mba",
        password="mba2025",
        host="postgres"
    )
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO predictions (id, description, corretiva, melhoria) VALUES (%s, %s, %s, %s)",
        (order_id, description, corretiva, melhoria)
    )
    conn.commit()
    cur.close()
    conn.close()