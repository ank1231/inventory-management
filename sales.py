import sqlite3
from datetime import datetime, date
from typing import List, Dict, Optional
import database

class SalesManager:
    def __init__(self):
        database.init_database()
    
    def record_sale(self, product_id: int, sale_date: date, quantity: int, platform: str) -> Optional[int]:
        if platform not in ['네이버', '쿠팡', '자사몰']:
            raise ValueError("Platform must be 네이버, 쿠팡, or 자사몰")
        
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT price, margin_naver, margin_coupang, margin_self, quantity FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        
        if not product:
            conn.close()
            raise ValueError("Product not found")
        
        price, margin_naver, margin_coupang, margin_self, current_quantity = product
        
        if quantity > current_quantity:
            conn.close()
            raise ValueError(f"Insufficient stock. Available: {current_quantity}, Requested: {quantity}")
        
        margin_map = {'네이버': margin_naver, '쿠팡': margin_coupang, '자사몰': margin_self}
        margin = margin_map[platform]
        
        revenue = price * quantity
        profit = revenue * (1 - margin / 100)
        
        cursor.execute('''
            INSERT INTO sales (product_id, sale_date, quantity, platform, revenue, profit)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (product_id, sale_date, quantity, platform, revenue, profit))
        
        sale_id = cursor.lastrowid
        
        cursor.execute('UPDATE products SET quantity = quantity - ? WHERE id = ?', (quantity, product_id))
        
        conn.commit()
        conn.close()
        
        return sale_id
    
    def get_sales_by_date(self, start_date: date, end_date: date) -> List[Dict]:
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.id, s.product_id, p.name, s.sale_date, s.quantity, 
                   s.platform, s.revenue, s.profit, s.created_at
            FROM sales s
            JOIN products p ON s.product_id = p.id
            WHERE s.sale_date BETWEEN ? AND ?
            ORDER BY s.sale_date DESC, s.created_at DESC
        ''', (start_date, end_date))
        
        sales = []
        for row in cursor.fetchall():
            sales.append({
                'id': row[0],
                'product_id': row[1],
                'product_name': row[2],
                'sale_date': row[3],
                'quantity': row[4],
                'platform': row[5],
                'revenue': row[6],
                'profit': row[7],
                'created_at': row[8]
            })
        
        conn.close()
        return sales
    
    def get_sales_summary(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Dict:
        conn = database.get_connection()
        cursor = conn.cursor()
        
        where_clause = ""
        params = []
        
        if start_date and end_date:
            where_clause = "WHERE sale_date BETWEEN ? AND ?"
            params = [start_date, end_date]
        
        cursor.execute(f'''
            SELECT 
                COUNT(*) as total_sales,
                SUM(quantity) as total_quantity,
                SUM(revenue) as total_revenue,
                SUM(profit) as total_profit
            FROM sales {where_clause}
        ''', params)
        
        summary = cursor.fetchone()
        
        cursor.execute(f'''
            SELECT platform,
                   COUNT(*) as sales_count,
                   SUM(quantity) as quantity,
                   SUM(revenue) as revenue,
                   SUM(profit) as profit
            FROM sales {where_clause}
            GROUP BY platform
        ''', params)
        
        platform_stats = {}
        for row in cursor.fetchall():
            platform_stats[row[0]] = {
                'sales_count': row[1],
                'quantity': row[2],
                'revenue': row[3],
                'profit': row[4]
            }
        
        cursor.execute(f'''
            SELECT p.name, SUM(s.quantity) as total_sold, SUM(s.revenue) as total_revenue
            FROM sales s
            JOIN products p ON s.product_id = p.id
            {where_clause}
            GROUP BY s.product_id, p.name
            ORDER BY total_sold DESC
            LIMIT 5
        ''', params)
        
        top_products = []
        for row in cursor.fetchall():
            top_products.append({
                'name': row[0],
                'quantity_sold': row[1],
                'revenue': row[2]
            })
        
        conn.close()
        
        return {
            'total_sales': summary[0] or 0,
            'total_quantity': summary[1] or 0,
            'total_revenue': summary[2] or 0,
            'total_profit': summary[3] or 0,
            'platform_stats': platform_stats,
            'top_products': top_products
        }
    
    def get_product_sales_history(self, product_id: int) -> List[Dict]:
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, sale_date, quantity, platform, revenue, profit, created_at
            FROM sales
            WHERE product_id = ?
            ORDER BY sale_date DESC, created_at DESC
        ''', (product_id,))
        
        sales = []
        for row in cursor.fetchall():
            sales.append({
                'id': row[0],
                'sale_date': row[1],
                'quantity': row[2],
                'platform': row[3],
                'revenue': row[4],
                'profit': row[5],
                'created_at': row[6]
            })
        
        conn.close()
        return sales