import os
import psycopg

def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "eventstream"),
        user=os.getenv("DB_USER", "eventstream"),
        password=os.getenv(
            "DB_PASSWORD",
            "eventstream_dev_only",
        ),
    )
