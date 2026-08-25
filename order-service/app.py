import os
import uuid
from datetime import datetime
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://appuser:secret123@db:5432/appdb')
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)


#Fix 7 : In table schema SQL query, there was a syntax error for NOT NULL fixed.
TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(36) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_name VARCHAR(255),
    quantity INTEGER,
    total_price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def init_db():
    session = SessionLocal()
    try:
        session.execute(text(TABLE_SCHEMA))
        session.commit()
    except Exception as e:
        print(f"DB init failed: {e}")
    finally:
        session.close()

init_db()

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "order-service"}), 200

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order_id = str(uuid.uuid4())
    session = SessionLocal()
    try:
        stmt = text("""
            INSERT INTO orders (id, user_id, product_name, quantity, total_price)
            VALUES (:id, :user_id, :product_name, :quantity, :total_price)
        """)
        session.execute(stmt, {
            'id': order_id,
            'user_id': data['user_id'],
            'product_name': data['product_name'],
            'quantity': data['quantity'],
            'total_price': data['total_price']
        })
        session.commit()
        return jsonify({"order_id": order_id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/orders/user/<int:user_id>')
def get_user_orders(user_id):
    session = SessionLocal()
    try:
        stmt = text("SELECT * FROM orders WHERE user_id = :user_id ORDER BY created_at DESC")
        result = session.execute(stmt, {'user_id': user_id})
        orders = [dict(row) for row in result]
        return jsonify(orders)
    finally:
        session.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
