import sqlite3
from datetime import datetime
import os

DATABASE_NAME = "inventory.db"

def init_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Create products table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        options TEXT,
        price DECIMAL(10,2) NOT NULL,
        margin_naver DECIMAL(5,2) NOT NULL,
        margin_coupang DECIMAL(5,2) NOT NULL,
        margin_self DECIMAL(5,2) NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Check if columns exist and add them if they don't (migration)
    cursor.execute("PRAGMA table_info(products)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Add options column if it doesn't exist
    if 'options' not in columns:
        cursor.execute('ALTER TABLE products ADD COLUMN options TEXT')
        print("Added 'options' column to products table")
    
    # Rename margin columns if old ones exist
    if 'margin_a' in columns and 'margin_naver' not in columns:
        cursor.execute('ALTER TABLE products ADD COLUMN margin_naver DECIMAL(5,2)')
        cursor.execute('ALTER TABLE products ADD COLUMN margin_coupang DECIMAL(5,2)')
        cursor.execute('ALTER TABLE products ADD COLUMN margin_self DECIMAL(5,2)')
        cursor.execute('UPDATE products SET margin_naver = margin_a, margin_coupang = margin_b, margin_self = margin_c')
        print("Migrated margin columns to new platform names")
    
    # Create sales table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        sale_date DATE NOT NULL,
        quantity INTEGER NOT NULL,
        platform VARCHAR(10) NOT NULL,
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