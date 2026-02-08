import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    # Vercel usará esta variable que configuraremos en su panel
    url = os.getenv("DATABASE_URL")
    if url:
        return psycopg2.connect(url)
    
    # Esto es solo por si algo falla, pero lo ideal es usar la URL arriba
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port="5432"
    )