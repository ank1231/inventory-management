import sqlite3
from datetime import datetime
import os

DATABASE_NAME = "inventory.db"

def init_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        margin_a DECIMAL(5,2) NOT NULL,
        margin_b DECIMAL(5,2) NOT NULL,
        margin_c DECIMAL(5,2) NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        sale_date DATE NOT NULL,
        quantity INTEGER NOT NULL,
        platform VARCHAR(1) NOT NULL,
        revenue DECIMAL(10,2) NOT NULL,
        profit DECIMAL(10,2) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database '{DATABASE_NAME}' initialized successfully.")

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

if __name__ == "__main__":
    init_database()