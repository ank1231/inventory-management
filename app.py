from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, date, timedelta
import inventory
import sales
import database_cloud as database
from auth import User
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here-change-this')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '로그인이 필요합니다.'

manager = inventory.InventoryManager()
sales_manager = sales.SalesManager()

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.verify_password(username, password):
            user = User.get_by_username(username)
            if user:
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
        
        flash('아이디 또는 비밀번호가 올바르지 않습니다.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    products = manager.get_all_products()
    summary = manager.get_inventory_summary()
    return render_template('dashboard.html', products=products, summary=summary)

@app.route('/inventory')
@login_required
def inventory_page():
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'name')
    products = manager.get_all_products(search=search, sort_by=sort_by)
    # 인라인 편집 가능한 버전의 템플릿 사용
    return render_template('inventory_editable.html', products=products, search=search, sort_by=sort_by)

@app.route('/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        try:
            name = request.form['name']
            options = request.form.get('options', '')
            price = float(request.form['price'])
            margin_naver = float(request.form['margin_naver'])
            margin_coupang = float(request.form['margin_coupang'])
            margin_self = float(request.form['margin_self'])
            quantity = int(request.form['quantity'])
            
            manager.add_product(name, options, price, margin_naver, margin_coupang, margin_self, quantity)
            return redirect(url_for('inventory_page'))
        except Exception as e:
            return render_template('add_product.html', error=str(e))
    
    return render_template('add_product.html')

@app.route('/product/copy/<int:product_id>')
@login_required
def copy_product(product_id):
    product = manager.get_product(product_id)
    if not product:
        return redirect(url_for('inventory_page'))
    
    # 복사된 상품 정보를 전달
    product['quantity'] = 0  # 초기 재고는 0으로 설정
    
    return render_template('add_product.html', copy_from=product)

@app.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = manager.get_product(product_id)
    if not product:
        return redirect(url_for('inventory_page'))
    
    if request.method == 'POST':
        try:
            updates = {}
            if request.form.get('name'):
                updates['name'] = request.form['name']
            if request.form.get('options') is not None:
                updates['options'] = request.form['options']
            if request.form.get('price'):
                updates['price'] = float(request.form['price'])
            if request.form.get('margin_naver'):
                updates['margin_naver'] = float(request.form['margin_naver'])
            if request.form.get('margin_coupang'):
                updates['margin_coupang'] = float(request.form['margin_coupang'])
            if request.form.get('margin_self'):
                updates['margin_self'] = float(request.form['margin_self'])
            if request.form.get('quantity'):
                updates['quantity'] = int(request.form['quantity'])
            
            manager.update_product(product_id, **updates)
            return redirect(url_for('inventory_page'))
        except Exception as e:
            return render_template('edit_product.html', product=product, error=str(e))
    
    return render_template('edit_product.html', product=product)

@app.route('/product/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    manager.delete_product(product_id)
    return redirect(url_for('inventory_page'))

@app.route('/api/inventory/summary')
@login_required
def api_inventory_summary():
    summary = manager.get_inventory_summary()
    return jsonify(summary)

@app.route('/api/products')
@login_required
def api_products():
    products = manager.get_all_products()
    return jsonify(products)

@app.route('/api/products/bulk-update', methods=['POST'])
@login_required
def api_bulk_update_products():
    try:
        updates = request.json
        result = manager.bulk_update_products(updates)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/sales')
@login_required
def sales_page():
    today = date.today()
    start_date = request.args.get('start_date', today.strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', today.strftime('%Y-%m-%d'))
    
    sales_list = sales_manager.get_sales_by_date(start_date, end_date)
    summary = sales_manager.get_sales_summary(start_date, end_date)
    
    return render_template('sales.html', 
                         sales=sales_list, 
                         summary=summary,
                         start_date=start_date,
                         end_date=end_date)

@app.route('/sales/add', methods=['GET', 'POST'])
@login_required
def add_sale():
    if request.method == 'POST':
        try:
            product_id = int(request.form['product_id'])
            sale_date = request.form['sale_date']
            quantity = int(request.form['quantity'])
            platform = request.form['platform']
            
            sales_manager.record_sale(product_id, sale_date, quantity, platform)
            return redirect(url_for('sales_page'))
        except Exception as e:
            products = manager.get_all_products()
            return render_template('add_sale.html', products=products, error=str(e))
    
    products = manager.get_all_products()
    today = date.today().strftime('%Y-%m-%d')
    return render_template('add_sale.html', products=products, today=today)

@app.route('/sales/edit/<int:sale_id>', methods=['GET', 'POST'])
@login_required
def edit_sale(sale_id):
    sale = sales_manager.get_sale(sale_id)
    if not sale:
        return redirect(url_for('sales_page'))
    
    if request.method == 'POST':
        try:
            product_id = int(request.form['product_id'])
            sale_date = request.form['sale_date']
            quantity = int(request.form['quantity'])
            platform = request.form['platform']
            
            sales_manager.update_sale(sale_id, product_id, sale_date, quantity, platform)
            return redirect(url_for('sales_page'))
        except Exception as e:
            products = manager.get_all_products()
            return render_template('edit_sale.html', sale=sale, products=products, error=str(e))
    
    products = manager.get_all_products()
    return render_template('edit_sale.html', sale=sale, products=products)

@app.route('/sales/delete/<int:sale_id>', methods=['POST'])
@login_required
def delete_sale(sale_id):
    sales_manager.delete_sale(sale_id)
    return redirect(url_for('sales_page'))

@app.route('/reports')
@login_required
def reports_page():
    today = date.today()
    
    period = request.args.get('period', 'week')
    
    if period == 'day':
        start_date = today
        end_date = today
    elif period == 'week':
        start_date = today - timedelta(days=7)
        end_date = today
    elif period == 'month':
        start_date = today - timedelta(days=30)
        end_date = today
    else:
        start_date = request.args.get('start_date', today - timedelta(days=7))
        end_date = request.args.get('end_date', today)
    
    sales_summary = sales_manager.get_sales_summary(start_date, end_date)
    inventory_summary = manager.get_inventory_summary()
    
    return render_template('reports.html',
                         sales_summary=sales_summary,
                         inventory_summary=inventory_summary,
                         start_date=start_date,
                         end_date=end_date,
                         period=period)

if __name__ == '__main__':
    # 데이터베이스 초기화
    database.init_database()
    # 초기 관리자 계정 생성
    User.init_admin()
    app.run(debug=True, port=5000)