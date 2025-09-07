import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import database

class InventoryManager:
    def __init__(self):
        database.init_database()
    
    def add_product(self, name: str, price: float, margin_naver: float, 
                   margin_coupang: float, margin_self: float, quantity: int = 0) -> int:
        if price < 0:
            raise ValueError("Price must be non-negative")
        if not (0 <= margin_naver <= 100 and 0 <= margin_coupang <= 100 and 0 <= margin_self <= 100):
            raise ValueError("Margins must be between 0 and 100")
        if quantity < 0:
            raise ValueError("Quantity must be non-negative")
        
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO products (name, price, margin_naver, margin_coupang, margin_self, quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, price, margin_naver, margin_coupang, margin_self, quantity))
        
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return product_id
    
    def get_product(self, product_id: int) -> Optional[Dict]:
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, price, margin_naver, margin_coupang, margin_self, quantity, 
                   created_at, updated_at
            FROM products
            WHERE id = ?
        ''', (product_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'price': row[2],
                'margin_naver': row[3],
                'margin_coupang': row[4],
                'margin_self': row[5],
                'quantity': row[6],
                'created_at': row[7],
                'updated_at': row[8]
            }
        return None
    
    def get_all_products(self, search: str = "", sort_by: str = "name") -> List[Dict]:
        conn = database.get_connection()
        cursor = conn.cursor()
        
        valid_sort = {
            'name': 'name',
            'price': 'price',
            'quantity': 'quantity',
            'value': 'price * quantity'
        }
        
        sort_column = valid_sort.get(sort_by, 'name')
        
        query = '''
            SELECT id, name, price, margin_naver, margin_coupang, margin_self, quantity,
                   price * quantity as value, created_at, updated_at
            FROM products
        '''
        
        params = []
        if search:
            query += " WHERE name LIKE ?"
            params.append(f'%{search}%')
        
        query += f" ORDER BY {sort_column}"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        products = []
        for row in rows:
            products.append({
                'id': row[0],
                'name': row[1],
                'price': row[2],
                'margin_naver': row[3],
                'margin_coupang': row[4],
                'margin_self': row[5],
                'quantity': row[6],
                'value': row[7],
                'created_at': row[8],
                'updated_at': row[9]
            })
        
        return products
    
    def update_product(self, product_id: int, **kwargs) -> bool:
        allowed_fields = ['name', 'price', 'margin_naver', 'margin_coupang', 'margin_self', 'quantity']
        
        if 'price' in kwargs and kwargs['price'] < 0:
            raise ValueError("Price must be non-negative")
        
        for margin in ['margin_naver', 'margin_coupang', 'margin_self']:
            if margin in kwargs and not (0 <= kwargs[margin] <= 100):
                raise ValueError(f"{margin} must be between 0 and 100")
        
        if 'quantity' in kwargs and kwargs['quantity'] < 0:
            raise ValueError("Quantity must be non-negative")
        
        fields_to_update = []
        values = []
        
        for field in allowed_fields:
            if field in kwargs:
                fields_to_update.append(f"{field} = ?")
                values.append(kwargs[field])
        
        if not fields_to_update:
            return False
        
        fields_to_update.append("updated_at = CURRENT_TIMESTAMP")
        values.append(product_id)
        
        conn = database.get_connection()
        cursor = conn.cursor()
        
        query = f"UPDATE products SET {', '.join(fields_to_update)} WHERE id = ?"
        cursor.execute(query, values)
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def delete_product(self, product_id: int) -> bool:
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def get_inventory_summary(self) -> Dict:
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_products,
                SUM(quantity) as total_quantity,
                SUM(price * quantity) as total_value,
                AVG(price) as avg_price
            FROM products
        ''')
        
        row = cursor.fetchone()
        
        cursor.execute('''
            SELECT name, quantity, price * quantity as value,
                   ROUND(100.0 * quantity / NULLIF((SELECT SUM(quantity) FROM products), 0), 2) as quantity_ratio
            FROM products
            ORDER BY quantity DESC
        ''')
        
        product_details = []
        for product_row in cursor.fetchall():
            product_details.append({
                'name': product_row[0],
                'quantity': product_row[1],
                'value': product_row[2],
                'quantity_ratio': product_row[3] or 0
            })
        
        conn.close()
        
        return {
            'total_products': row[0] or 0,
            'total_quantity': row[1] or 0,
            'total_value': row[2] or 0,
            'avg_price': round(row[3], 2) if row[3] else 0,
            'product_details': product_details
        }


if __name__ == "__main__":
    manager = InventoryManager()
    
    print("Testing InventoryManager...")
    
    product_id = manager.add_product("Test Product", 10000, 10, 15, 20, 50)
    print(f"Added product with ID: {product_id}")
    
    product = manager.get_product(product_id)
    print(f"Retrieved product: {product}")
    
    manager.update_product(product_id, price=12000, quantity=100)
    print("Updated product price and quantity")
    
    all_products = manager.get_all_products()
    print(f"All products: {all_products}")
    
    summary = manager.get_inventory_summary()
    print(f"Inventory summary: {summary}")