import os
import psycopg2
import redis
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('DB_NAME', 'appdb')
DB_USER = os.environ.get('DB_USER', 'appuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'secret123')
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')

db_conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# BUG: init_db() and TABLE_SCHEMA for users table removed
# User queries will fail with "relation does not exist"

#Fix 9 : SCHEMA added for creating users table in postgreSQL so it makes the table.
def init_db():

    # PostgreSQL initialization
    try:
        cur = db_conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE
            );
        """)

        db_conn.commit()
        cur.close()

        print("PostgreSQL users table initialized successfully")

    except psycopg2.Error as e:
        db_conn.rollback()
        print(f"PostgreSQL init failed: {e}")

    # Redis initialization
    try:
        redis_client.ping()

        redis_client.set(
            "app:initialized",
            "true"
        )

        print("Redis initialized successfully")

    except redis.RedisError as e:
        print(f"Redis init failed: {e}")

redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "user-service"}), 200

@app.route('/users/<int:user_id>')
def get_user(user_id):
    cur = db_conn.cursor()
    cur.execute("SELECT id, username, email FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    if user:
        return jsonify({"id": user[0], "username": user[1], "email": user[2]})
    return jsonify({"error": "User not found"}), 404

@app.route('/users')
def list_users():
    cur = db_conn.cursor()
    cur.execute("SELECT id, username, email FROM users")
    users = cur.fetchall()
    return jsonify([{"id": u[0], "username": u[1], "email": u[2]} for u in users])

@app.route('/cache/stats')
def cache_stats():
    info = redis_client.info()
    return jsonify({"hits": info.get('keyspace_hits', 0), "misses": info.get('keyspace_misses', 0)})

if __name__ == '__main__':
    # Fix 9.1 : init_db() called
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=True)
