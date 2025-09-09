from flask_login import UserMixin
from flask_bcrypt import Bcrypt
import database_cloud as database
import os

bcrypt = Bcrypt()

class User(UserMixin):
    def __init__(self, id, username, email, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.is_admin = is_admin
    
    @staticmethod
    def create_user(username, email, password, is_admin=False):
        """새 사용자 생성"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # 비밀번호 해시화
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        try:
            if database.USE_POSTGRESQL:
                cursor.execute('''
                    INSERT INTO users (username, email, password_hash, is_admin)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                ''', (username, email, password_hash, is_admin))
                user_id = cursor.fetchone()[0]
            else:
                cursor.execute('''
                    INSERT INTO users (username, email, password_hash, is_admin)
                    VALUES (?, ?, ?, ?)
                ''', (username, email, password_hash, is_admin))
                user_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            return user_id
        except Exception as e:
            conn.close()
            raise e
    
    @staticmethod
    def get_by_username(username):
        """사용자명으로 사용자 조회"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if database.USE_POSTGRESQL:
            cursor.execute('SELECT id, username, email, is_admin FROM users WHERE username = %s', (username,))
        else:
            cursor.execute('SELECT id, username, email, is_admin FROM users WHERE username = ?', (username,))
        
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return User(user_data[0], user_data[1], user_data[2], user_data[3])
        return None
    
    @staticmethod
    def get_by_id(user_id):
        """ID로 사용자 조회"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if database.USE_POSTGRESQL:
            cursor.execute('SELECT id, username, email, is_admin FROM users WHERE id = %s', (user_id,))
        else:
            cursor.execute('SELECT id, username, email, is_admin FROM users WHERE id = ?', (user_id,))
        
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return User(user_data[0], user_data[1], user_data[2], user_data[3])
        return None
    
    @staticmethod
    def verify_password(username, password):
        """비밀번호 확인"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if database.USE_POSTGRESQL:
            cursor.execute('SELECT password_hash FROM users WHERE username = %s', (username,))
        else:
            cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return bcrypt.check_password_hash(result[0], password)
        return False
    
    @staticmethod
    def init_admin():
        """초기 관리자 계정 생성"""
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123!')
        
        # 이미 관리자가 있는지 확인
        if not User.get_by_username(admin_username):
            try:
                User.create_user(admin_username, admin_email, admin_password, is_admin=True)
                print(f"Admin user '{admin_username}' created successfully")
            except Exception as e:
                print(f"Failed to create admin user: {e}")