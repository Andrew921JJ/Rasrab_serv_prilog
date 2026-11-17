from flask import Flask, jsonify
from app.db import db
from app.config import config

app = Flask(__name__)

# Инициализация пула при старте
@app.before_first_request
def init_db():
    db.connect()

@app.route('/health', methods=['GET'])
def health():
    try:
        conn = db.pool.get_connection()
        try:
            conn.ping(reconnect=True)
        finally:
            conn.close()
        return jsonify({"status": "ok", "db": "up", "service": config.SERVICE_NAME}), 200
    except Exception:
        return jsonify({"status": "error", "db": "down"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)