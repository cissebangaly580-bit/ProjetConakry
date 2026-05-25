import psycopg2
import psycopg2.extras

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="conakry_db",
        user="postgres",
        password="12345"
    )
    return conn