from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file (useful for local dev)
load_dotenv()

app = Flask(__name__)

# Use ProxyFix to trust X-Forwarded-For from 1 proxy (Nginx)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

# Read DB configuration from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

@app.route('/ping')
def ping_pong():
    client_ip = request.remote_addr  # Real client IP thanks to ProxyFix

    conn = get_db_connection()
    if not conn:
        return "Error: Could not connect to the database.", 500

    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE ping_counts 
            SET hit_count = hit_count + 1, 
                last_ip = %s
            WHERE id = 1
        """, (client_ip,))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error updating database: {err}")
        conn.rollback()
        return "Error: Could not update the database.", 500
    finally:
        cursor.close()
        conn.close()

    return "<h1>pong</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)