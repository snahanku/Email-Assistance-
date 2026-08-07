import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)

    print("Connected Successfully")

    cur = conn.cursor()
    cur.execute("SELECT version();")

    print(cur.fetchone())

    cur.close()
    conn.close()

except Exception as e:
    print("Connection Failed")
    print(e)


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def initialize_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS processed_emails (
            message_id TEXT PRIMARY KEY,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("Database Initialized Successfully")


def   is_processed(message_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM processed_emails WHERE message_id=%s;",
        (message_id,)
    )

    exists = cur.fetchone() is not None

    cur.close()
    conn.close()

    return exists

def mark_processed(message_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO processed_emails(message_id)
        VALUES(%s)
        ON CONFLICT (message_id) DO NOTHING;
    """, (message_id,))

    conn.commit()

    cur.close()
    conn.close()

if __name__ == "__main__":
    initialize_database()