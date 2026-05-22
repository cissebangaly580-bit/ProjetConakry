import psycopg2
import psycopg2.extras

DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "conakry_db",
    "user":     "postgres",
    "password": "12345"
}

PREFIX = "conakry_travel_hotel_"

def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

def get_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
