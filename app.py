import os
import datetime
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "app-db")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "appsecret")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        connect_timeout=3
    )


@app.route("/api/date", methods=["GET"])
def get_date():
    db_timestamp = None
    db_status = "connected"
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT CURRENT_TIMESTAMP;")
        result = cur.fetchone()
        if result:
            db_timestamp = str(result[0])
        cur.close()
        conn.close()
    except Exception as e:
        db_status = f"error: {str(e)}"

    current_date = datetime.datetime.now(datetime.timezone.utc).isoformat()

    return jsonify({
        "status": "success",
        "date": current_date,
        "db_timestamp": db_timestamp,
        "db_status": db_status,
        "service": "app-service",
        "containerized": True
    })


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Welcome to app-service",
        "endpoints": ["/api/date"]
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

