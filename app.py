from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, date, timedelta
import inventory
import sales
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

manager = inventory.InventoryManager()
sales_manager = sales.SalesManager()

@app.route('/')
def index():
    products = manager.get_all_products()
    summary = manager.get_inventory_summary()
    return render_template('dashboard.html', products=products, summary=summary)

@app.route('/inventory')
def inventory_page():
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'name')
    products = manager.get_all_products(search=search, sort_by=sort_by)
    return render_template('inventory.html', products=products, search=search, sort_by=sort_by)

@app.route('/product/add', methods=['GET', 'POST'])
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

@app.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
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
def delete_product(product_id):
    manager.delete_product(product_id)
    return redirect(url_for('inventory_page'))

@app.route('/api/inventory/summary')
def api_inventory_summary():
    summary = manager.get_inventory_summary()
    return jsonify(summary)

@app.route('/api/products')
def api_products():
    products = manager.get_all_products()
    return jsonify(products)

@app.route('/sales')
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

@app.route('/reports')
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
    app.run(debug=True, port=5000)