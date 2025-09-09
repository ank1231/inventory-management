import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 데이터베이스 URL (환경변수에서 가져오기)
DATABASE_URL = os.getenv('DATABASE_URL')
USE_POSTGRESQL = DATABASE_URL and DATABASE_URL.startswith('postgresql')

if USE_POSTGRESQL:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from urllib.parse import urlparse

def init_database():
    """데이터베이스 초기화 - SQLite와 PostgreSQL 모두 지원"""
    if USE_POSTGRESQL:
        # PostgreSQL 연결
        result = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            database=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        cursor = conn.cursor()
        
        # PostgreSQL 테이블 생성
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            options TEXT,
            price DECIMAL(10,2) NOT NULL,
            margin_naver DECIMAL(5,2) NOT NULL,
            margin_coupang DECIMAL(5,2) NOT NULL,
            margin_self DECIMAL(5,2) NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id SERIAL PRIMARY KEY,
            product_id INTEGER NOT NULL REFERENCES products(id),
            sale_date DATE NOT NULL,
            quantity INTEGER NOT NULL,
            platform VARCHAR(10) NOT NULL,
            revenue DECIMAL(10,2) NOT NULL,
            profit DECIMAL(10,2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 사용자 테이블 추가 (인증 시스템용)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
    else:
        # SQLite 연결 (기존 코드)
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        
        # SQLite 테이블 생성
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
        
        # 마이그레이션 체크
        cursor.execute("PRAGMA table_info(products)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'options' not in columns:
            cursor.execute('ALTER TABLE products ADD COLUMN options TEXT')
            print("Added 'options' column to products table")
        
        if 'margin_a' in columns and 'margin_naver' not in columns:
            cursor.execute('ALTER TABLE products ADD COLUMN margin_naver DECIMAL(5,2)')
            cursor.execute('ALTER TABLE products ADD COLUMN margin_coupang DECIMAL(5,2)')
            cursor.execute('ALTER TABLE products ADD COLUMN margin_self DECIMAL(5,2)')
            cursor.execute('UPDATE products SET margin_naver = margin_a, margin_coupang = margin_b, margin_self = margin_c')
            print("Migrated margin columns to new platform names")
        
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
        
        # 사용자 테이블 추가 (인증 시스템용)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized successfully ({'PostgreSQL' if USE_POSTGRESQL else 'SQLite'})")

def get_connection():
    """데이터베이스 연결 반환"""
    if USE_POSTGRESQL:
        result = urlparse(DATABASE_URL)
        return psycopg2.connect(
            database=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
    else:
        return sqlite3.connect('inventory.db')

def dict_factory(cursor, row):
    """SQLite 결과를 딕셔너리로 변환"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

if __name__ == "__main__":
    init_database()