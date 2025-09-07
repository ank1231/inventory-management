# 백엔드 개발 상세요건 문서

## 1. 기술 스택 및 도구

### 1.1 핵심 기술
- **Python 3.9+**: 프로그래밍 언어
- **Flask 2.3.0**: 웹 프레임워크
- **SQLAlchemy 2.0**: ORM
- **SQLite 3**: 데이터베이스
- **Marshmallow 3.20**: 직렬화/검증

### 1.2 추가 라이브러리
- **Flask-CORS**: CORS 처리
- **Flask-JWT-Extended**: JWT 인증 (추후)
- **python-dotenv**: 환경 변수
- **pandas**: 데이터 처리
- **openpyxl**: Excel 처리
- **APScheduler**: 스케줄링
- **logging**: 로깅

### 1.3 개발 도구
- **VS Code**: 에디터
- **Postman**: API 테스트
- **DB Browser for SQLite**: DB 관리
- **pytest**: 테스트

## 2. 프로젝트 구조

```
backend/
├── app.py                  # Flask 앱 진입점
├── config.py              # 설정 파일
├── requirements.txt       # 의존성 목록
├── .env                   # 환경 변수
├── .gitignore            # Git 제외 파일
│
├── api/                   # API 엔드포인트
│   ├── __init__.py
│   ├── products.py       # 재고 관련 API
│   ├── sales.py          # 판매 관련 API
│   ├── reports.py        # 리포트 API
│   └── export.py         # 내보내기 API
│
├── models/                # 데이터 모델
│   ├── __init__.py
│   ├── product.py        # 상품 모델
│   ├── sale.py           # 판매 모델
│   └── database.py       # DB 연결
│
├── services/              # 비즈니스 로직
│   ├── __init__.py
│   ├── inventory_service.py  # 재고 서비스
│   ├── sales_service.py      # 판매 서비스
│   └── report_service.py     # 리포트 서비스
│
├── schemas/               # 스키마 정의
│   ├── __init__.py
│   ├── product_schema.py # 상품 스키마
│   └── sale_schema.py    # 판매 스키마
│
├── utils/                 # 유틸리티
│   ├── __init__.py
│   ├── validators.py     # 검증 함수
│   ├── formatters.py     # 포맷팅
│   └── exceptions.py     # 커스텀 예외
│
├── migrations/            # DB 마이그레이션
│   └── init_db.py       # DB 초기화
│
├── tests/                 # 테스트
│   ├── __init__.py
│   ├── test_products.py
│   ├── test_sales.py
│   └── test_reports.py
│
└── logs/                  # 로그 파일
    └── app.log
```

## 3. 데이터베이스 설계

### 3.1 ERD (Entity Relationship Diagram)
```
┌──────────────┐         ┌──────────────┐
│   Products   │         │    Sales     │
├──────────────┤         ├──────────────┤
│ id (PK)      │──────┐  │ id (PK)      │
│ name         │      └──│ product_id(FK)│
│ price        │         │ sale_date    │
│ margin_a     │         │ quantity     │
│ margin_b     │         │ platform     │
│ margin_c     │         │ revenue      │
│ quantity     │         │ profit       │
│ created_at   │         │ created_at   │
│ updated_at   │         └──────────────┘
└──────────────┘
```

### 3.2 테이블 정의

#### Products 테이블
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    margin_a DECIMAL(5, 2) DEFAULT 0 CHECK (margin_a >= 0 AND margin_a <= 100),
    margin_b DECIMAL(5, 2) DEFAULT 0 CHECK (margin_b >= 0 AND margin_b <= 100),
    margin_c DECIMAL(5, 2) DEFAULT 0 CHECK (margin_c >= 0 AND margin_c <= 100),
    quantity INTEGER DEFAULT 0 CHECK (quantity >= 0),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_quantity ON products(quantity);
```

#### Sales 테이블
```sql
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    sale_date DATE NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    platform CHAR(1) NOT NULL CHECK (platform IN ('A', 'B', 'C')),
    revenue DECIMAL(10, 2) NOT NULL CHECK (revenue >= 0),
    profit DECIMAL(10, 2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE INDEX idx_sales_date ON sales(sale_date);
CREATE INDEX idx_sales_product ON sales(product_id);
CREATE INDEX idx_sales_platform ON sales(platform);
```

## 4. API 엔드포인트 상세

### 4.1 기본 설정
```python
# config.py
class Config:
    SECRET_KEY = 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///inventory.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'
    JSON_SORT_KEYS = False
    JSON_AS_ASCII = False
```

### 4.2 재고 관리 API

#### GET /api/products
**설명**: 전체 상품 목록 조회
```python
# Request
GET /api/products?page=1&limit=20&sort=name&order=asc&search=물건

# Response 200 OK
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "물건 a",
            "price": 23000,
            "margin_a": 30,
            "margin_b": 25,
            "margin_c": 19,
            "quantity": 40,
            "stock_value": 920000,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    ],
    "pagination": {
        "page": 1,
        "limit": 20,
        "total": 100,
        "pages": 5
    }
}
```

#### GET /api/products/{id}
**설명**: 특정 상품 조회
```python
# Request
GET /api/products/1

# Response 200 OK
{
    "success": true,
    "data": {
        "id": 1,
        "name": "물건 a",
        "price": 23000,
        "margin_a": 30,
        "margin_b": 25,
        "margin_c": 19,
        "quantity": 40,
        "stock_value": 920000,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
}

# Response 404 Not Found
{
    "success": false,
    "error": "Product not found"
}
```

#### POST /api/products
**설명**: 새 상품 등록
```python
# Request
POST /api/products
Content-Type: application/json
{
    "name": "물건 e",
    "price": 35000,
    "margin_a": 25,
    "margin_b": 30,
    "margin_c": 22,
    "quantity": 30
}

# Response 201 Created
{
    "success": true,
    "data": {
        "id": 5,
        "name": "물건 e",
        "price": 35000,
        "margin_a": 25,
        "margin_b": 30,
        "margin_c": 22,
        "quantity": 30,
        "stock_value": 1050000
    },
    "message": "Product created successfully"
}

# Response 400 Bad Request
{
    "success": false,
    "error": "Product name already exists"
}
```

#### PUT /api/products/{id}
**설명**: 상품 정보 수정
```python
# Request
PUT /api/products/1
Content-Type: application/json
{
    "name": "물건 a (수정)",
    "price": 25000,
    "quantity": 45
}

# Response 200 OK
{
    "success": true,
    "data": {
        "id": 1,
        "name": "물건 a (수정)",
        "price": 25000,
        "quantity": 45
    },
    "message": "Product updated successfully"
}
```

#### DELETE /api/products/{id}
**설명**: 상품 삭제
```python
# Request
DELETE /api/products/1

# Response 200 OK
{
    "success": true,
    "message": "Product deleted successfully"
}

# Response 400 Bad Request
{
    "success": false,
    "error": "Cannot delete product with sales history"
}
```

#### GET /api/products/summary
**설명**: 재고 요약 정보
```python
# Request
GET /api/products/summary

# Response 200 OK
{
    "success": true,
    "data": {
        "total_products": 10,
        "total_quantity": 500,
        "total_value": 25000000,
        "low_stock_products": 3,
        "out_of_stock_products": 0,
        "average_price": 50000,
        "average_margin": {
            "platform_a": 28.5,
            "platform_b": 31.2,
            "platform_c": 22.8
        }
    }
}
```

### 4.3 판매 관리 API

#### POST /api/sales
**설명**: 판매 등록
```python
# Request
POST /api/sales
Content-Type: application/json
{
    "product_id": 2,
    "sale_date": "2024-01-15",
    "quantity": 5,
    "platform": "A"
}

# Response 201 Created
{
    "success": true,
    "data": {
        "id": 1,
        "product_id": 2,
        "product_name": "물건 b",
        "sale_date": "2024-01-15",
        "quantity": 5,
        "platform": "A",
        "revenue": 310000,
        "profit": 238700,
        "margin_rate": 23
    },
    "message": "Sale recorded successfully"
}

# Response 400 Bad Request
{
    "success": false,
    "error": "Insufficient stock. Available: 20, Requested: 25"
}
```

#### GET /api/sales
**설명**: 판매 내역 조회
```python
# Request
GET /api/sales?start_date=2024-01-01&end_date=2024-01-31&platform=A

# Response 200 OK
{
    "success": true,
    "data": [
        {
            "id": 1,
            "product_id": 2,
            "product_name": "물건 b",
            "sale_date": "2024-01-15",
            "quantity": 5,
            "platform": "A",
            "revenue": 310000,
            "profit": 238700
        }
    ],
    "summary": {
        "total_sales": 1,
        "total_quantity": 5,
        "total_revenue": 310000,
        "total_profit": 238700
    }
}
```

#### DELETE /api/sales/{id}
**설명**: 판매 기록 삭제 (재고 복구)
```python
# Request
DELETE /api/sales/1

# Response 200 OK
{
    "success": true,
    "message": "Sale deleted and stock restored successfully"
}
```

### 4.4 리포트 API

#### GET /api/reports/daily
**설명**: 일일 리포트
```python
# Request
GET /api/reports/daily?date=2024-01-15

# Response 200 OK
{
    "success": true,
    "data": {
        "date": "2024-01-15",
        "sales": {
            "total_transactions": 10,
            "total_quantity": 50,
            "total_revenue": 2500000,
            "total_profit": 1875000,
            "platform_breakdown": {
                "A": {"transactions": 3, "revenue": 800000, "profit": 600000},
                "B": {"transactions": 4, "revenue": 900000, "profit": 675000},
                "C": {"transactions": 3, "revenue": 800000, "profit": 600000}
            }
        },
        "inventory": {
            "total_products": 10,
            "total_quantity": 450,
            "total_value": 22500000,
            "low_stock_alerts": ["물건 b", "물건 d"]
        },
        "top_products": [
            {"name": "물건 c", "quantity_sold": 20, "revenue": 1880000}
        ]
    }
}
```

#### GET /api/reports/period
**설명**: 기간별 리포트
```python
# Request
GET /api/reports/period?start_date=2024-01-01&end_date=2024-01-31

# Response 200 OK
{
    "success": true,
    "data": {
        "period": {
            "start": "2024-01-01",
            "end": "2024-01-31"
        },
        "summary": {
            "total_transactions": 150,
            "total_quantity": 750,
            "total_revenue": 37500000,
            "total_profit": 28125000,
            "average_daily_revenue": 1209677,
            "average_margin_rate": 25
        },
        "daily_trends": [
            {"date": "2024-01-01", "revenue": 1200000, "profit": 900000}
        ],
        "platform_performance": {
            "A": {"revenue": 12000000, "profit": 9000000, "transactions": 50},
            "B": {"revenue": 13000000, "profit": 9750000, "transactions": 55},
            "C": {"revenue": 12500000, "profit": 9375000, "transactions": 45}
        },
        "best_sellers": [
            {"product": "물건 c", "quantity": 150, "revenue": 14100000}
        ],
        "inventory_turnover": 2.5
    }
}
```

### 4.5 내보내기 API

#### GET /api/export/csv
**설명**: 재고 데이터 CSV 내보내기
```python
# Request
GET /api/export/csv

# Response 200 OK
Content-Type: text/csv
Content-Disposition: attachment; filename="inventory_20240115.csv"

"ID","상품명","가격","A마진(%)","B마진(%)","C마진(%)","재고수량","재고가치"
"1","물건 a","23000","30","25","19","40","920000"
```

#### GET /api/export/excel
**설명**: 전체 데이터 Excel 내보내기
```python
# Request
GET /api/export/excel?include_sales=true

# Response 200 OK
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename="inventory_report_20240115.xlsx"

[Binary Excel File]
```

## 5. 서비스 레이어 구현

### 5.1 재고 서비스 (inventory_service.py)
```python
class InventoryService:
    def __init__(self):
        self.db = get_db_session()
    
    def calculate_stock_value(self, product):
        """재고 가치 계산"""
        return product.price * product.quantity
    
    def check_low_stock(self, threshold=10):
        """낮은 재고 확인"""
        return Product.query.filter(Product.quantity < threshold).all()
    
    def update_stock(self, product_id, quantity_change):
        """재고 수량 업데이트"""
        product = Product.query.get_or_404(product_id)
        new_quantity = product.quantity + quantity_change
        
        if new_quantity < 0:
            raise ValueError("Insufficient stock")
        
        product.quantity = new_quantity
        product.updated_at = datetime.now()
        self.db.commit()
        return product
    
    def get_inventory_summary(self):
        """재고 요약 정보"""
        products = Product.query.all()
        
        return {
            'total_products': len(products),
            'total_quantity': sum(p.quantity for p in products),
            'total_value': sum(p.price * p.quantity for p in products),
            'low_stock_products': len([p for p in products if p.quantity < 10]),
            'out_of_stock_products': len([p for p in products if p.quantity == 0])
        }
```

### 5.2 판매 서비스 (sales_service.py)
```python
class SalesService:
    def __init__(self):
        self.db = get_db_session()
        self.inventory_service = InventoryService()
    
    def process_sale(self, product_id, quantity, platform, sale_date):
        """판매 처리"""
        # 상품 조회
        product = Product.query.get_or_404(product_id)
        
        # 재고 확인
        if product.quantity < quantity:
            raise ValueError(f"Insufficient stock. Available: {product.quantity}")
        
        # 마진율 가져오기
        margin_rate = getattr(product, f'margin_{platform.lower()}', 0) / 100
        
        # 매출 및 이익 계산
        revenue = product.price * quantity
        profit = revenue * (1 - margin_rate)
        
        # 판매 기록 생성
        sale = Sale(
            product_id=product_id,
            sale_date=sale_date,
            quantity=quantity,
            platform=platform,
            revenue=revenue,
            profit=profit
        )
        
        # 재고 차감
        self.inventory_service.update_stock(product_id, -quantity)
        
        # 저장
        self.db.add(sale)
        self.db.commit()
        
        return sale
    
    def cancel_sale(self, sale_id):
        """판매 취소 (재고 복구)"""
        sale = Sale.query.get_or_404(sale_id)
        
        # 재고 복구
        self.inventory_service.update_stock(sale.product_id, sale.quantity)
        
        # 판매 기록 삭제
        self.db.delete(sale)
        self.db.commit()
    
    def get_sales_by_period(self, start_date, end_date):
        """기간별 판매 조회"""
        return Sale.query.filter(
            Sale.sale_date.between(start_date, end_date)
        ).all()
    
    def calculate_platform_performance(self, sales):
        """플랫폼별 실적 계산"""
        performance = {'A': {}, 'B': {}, 'C': {}}
        
        for platform in ['A', 'B', 'C']:
            platform_sales = [s for s in sales if s.platform == platform]
            performance[platform] = {
                'transactions': len(platform_sales),
                'quantity': sum(s.quantity for s in platform_sales),
                'revenue': sum(s.revenue for s in platform_sales),
                'profit': sum(s.profit for s in platform_sales)
            }
        
        return performance
```

### 5.3 리포트 서비스 (report_service.py)
```python
class ReportService:
    def __init__(self):
        self.sales_service = SalesService()
        self.inventory_service = InventoryService()
    
    def generate_daily_report(self, date):
        """일일 리포트 생성"""
        # 당일 판매 데이터
        sales = Sale.query.filter(Sale.sale_date == date).all()
        
        # 판매 요약
        sales_summary = {
            'total_transactions': len(sales),
            'total_quantity': sum(s.quantity for s in sales),
            'total_revenue': sum(s.revenue for s in sales),
            'total_profit': sum(s.profit for s in sales)
        }
        
        # 플랫폼별 분석
        platform_breakdown = self.sales_service.calculate_platform_performance(sales)
        
        # 재고 현황
        inventory_summary = self.inventory_service.get_inventory_summary()
        
        # 베스트셀러
        product_sales = {}
        for sale in sales:
            if sale.product_id not in product_sales:
                product_sales[sale.product_id] = {'quantity': 0, 'revenue': 0}
            product_sales[sale.product_id]['quantity'] += sale.quantity
            product_sales[sale.product_id]['revenue'] += sale.revenue
        
        top_products = sorted(
            product_sales.items(),
            key=lambda x: x[1]['revenue'],
            reverse=True
        )[:5]
        
        return {
            'date': date,
            'sales': sales_summary,
            'platform_breakdown': platform_breakdown,
            'inventory': inventory_summary,
            'top_products': top_products
        }
    
    def generate_period_report(self, start_date, end_date):
        """기간별 리포트 생성"""
        sales = self.sales_service.get_sales_by_period(start_date, end_date)
        
        # 일별 추이
        daily_trends = {}
        for sale in sales:
            date_str = sale.sale_date.strftime('%Y-%m-%d')
            if date_str not in daily_trends:
                daily_trends[date_str] = {'revenue': 0, 'profit': 0}
            daily_trends[date_str]['revenue'] += sale.revenue
            daily_trends[date_str]['profit'] += sale.profit
        
        # 재고 회전율 계산
        days = (end_date - start_date).days + 1
        total_sold = sum(s.quantity for s in sales)
        avg_inventory = self.inventory_service.get_inventory_summary()['total_quantity']
        inventory_turnover = (total_sold / avg_inventory) * (365 / days) if avg_inventory > 0 else 0
        
        return {
            'period': {'start': start_date, 'end': end_date},
            'summary': {
                'total_transactions': len(sales),
                'total_quantity': sum(s.quantity for s in sales),
                'total_revenue': sum(s.revenue for s in sales),
                'total_profit': sum(s.profit for s in sales)
            },
            'daily_trends': daily_trends,
            'platform_performance': self.sales_service.calculate_platform_performance(sales),
            'inventory_turnover': round(inventory_turnover, 2)
        }
```

## 6. 스키마 및 검증

### 6.1 Marshmallow 스키마
```python
# schemas/product_schema.py
from marshmallow import Schema, fields, validate, validates, ValidationError

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    price = fields.Decimal(
        required=True,
        places=2,
        validate=validate.Range(min=0)
    )
    margin_a = fields.Decimal(
        places=2,
        validate=validate.Range(min=0, max=100),
        missing=0
    )
    margin_b = fields.Decimal(
        places=2,
        validate=validate.Range(min=0, max=100),
        missing=0
    )
    margin_c = fields.Decimal(
        places=2,
        validate=validate.Range(min=0, max=100),
        missing=0
    )
    quantity = fields.Int(
        validate=validate.Range(min=0),
        missing=0
    )
    stock_value = fields.Method("calculate_stock_value", dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    def calculate_stock_value(self, obj):
        return obj.price * obj.quantity
    
    @validates('name')
    def validate_name(self, value):
        # 중복 체크
        existing = Product.query.filter_by(name=value).first()
        if existing:
            raise ValidationError('Product name already exists')

# schemas/sale_schema.py
class SaleSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    product_name = fields.Method("get_product_name", dump_only=True)
    sale_date = fields.Date(required=True)
    quantity = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )
    platform = fields.Str(
        required=True,
        validate=validate.OneOf(['A', 'B', 'C'])
    )
    revenue = fields.Decimal(places=2, dump_only=True)
    profit = fields.Decimal(places=2, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    
    def get_product_name(self, obj):
        return obj.product.name if obj.product else None
```

## 7. 에러 처리

### 7.1 커스텀 예외
```python
# utils/exceptions.py
class AppException(Exception):
    """Base application exception"""
    status_code = 500
    message = "Internal server error"
    
    def __init__(self, message=None, status_code=None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)

class ValidationError(AppException):
    """Validation error"""
    status_code = 400

class NotFoundError(AppException):
    """Resource not found"""
    status_code = 404
    message = "Resource not found"

class InsufficientStockError(AppException):
    """Insufficient stock error"""
    status_code = 400
    
    def __init__(self, available, requested):
        message = f"Insufficient stock. Available: {available}, Requested: {requested}"
        super().__init__(message)

class DuplicateError(AppException):
    """Duplicate resource error"""
    status_code = 409
    message = "Resource already exists"
```

### 7.2 에러 핸들러
```python
# app.py
@app.errorhandler(AppException)
def handle_app_exception(error):
    response = {
        'success': False,
        'error': error.message
    }
    return jsonify(response), error.status_code

@app.errorhandler(404)
def handle_not_found(error):
    response = {
        'success': False,
        'error': 'Endpoint not found'
    }
    return jsonify(response), 404

@app.errorhandler(500)
def handle_internal_error(error):
    response = {
        'success': False,
        'error': 'Internal server error'
    }
    return jsonify(response), 500
```

## 8. 로깅

### 8.1 로깅 설정
```python
# config.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    if not app.debug:
        # 파일 핸들러
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Inventory Management System startup')
```

### 8.2 로깅 사용
```python
# 로깅 예시
@app.route('/api/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        app.logger.info(f"Creating product: {data.get('name')}")
        
        # 처리 로직
        product = ProductService().create(data)
        
        app.logger.info(f"Product created successfully: ID={product.id}")
        return jsonify({'success': True, 'data': product}), 201
        
    except Exception as e:
        app.logger.error(f"Error creating product: {str(e)}")
        raise
```

## 9. 보안

### 9.1 인증 (추후 구현)
```python
# JWT 설정 (준비)
JWT_SECRET_KEY = 'your-jwt-secret-key'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
```

### 9.2 입력 검증
```python
# validators.py
def validate_product_data(data):
    """상품 데이터 검증"""
    errors = []
    
    # 필수 필드 체크
    if not data.get('name'):
        errors.append('Product name is required')
    
    # 가격 검증
    price = data.get('price', 0)
    if price < 0:
        errors.append('Price must be non-negative')
    
    # 마진율 검증
    for platform in ['a', 'b', 'c']:
        margin = data.get(f'margin_{platform}', 0)
        if margin < 0 or margin > 100:
            errors.append(f'Margin for platform {platform.upper()} must be between 0 and 100')
    
    if errors:
        raise ValidationError('; '.join(errors))
    
    return True
```

### 9.3 CORS 설정
```python
# app.py
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

## 10. 성능 최적화

### 10.1 데이터베이스 최적화
- 인덱스 추가
- 쿼리 최적화
- 연결 풀링
- 캐싱

### 10.2 API 최적화
- 페이지네이션
- 필드 필터링
- 응답 압축
- 비동기 처리

## 11. 테스트

### 11.1 단위 테스트
```python
# tests/test_products.py
import pytest
from app import app
from models import Product

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_products(client):
    """상품 목록 조회 테스트"""
    response = client.get('/api/products')
    assert response.status_code == 200
    assert response.json['success'] == True

def test_create_product(client):
    """상품 생성 테스트"""
    data = {
        'name': 'Test Product',
        'price': 10000,
        'quantity': 50
    }
    response = client.post('/api/products', json=data)
    assert response.status_code == 201
    assert response.json['data']['name'] == 'Test Product'

def test_insufficient_stock(client):
    """재고 부족 테스트"""
    # 판매 시도
    data = {
        'product_id': 1,
        'quantity': 1000,  # 재고보다 많은 수량
        'platform': 'A'
    }
    response = client.post('/api/sales', json=data)
    assert response.status_code == 400
    assert 'Insufficient stock' in response.json['error']
```

## 12. 배포 준비

### 12.1 환경 변수
```bash
# .env
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-production-secret-key
DATABASE_URL=sqlite:///inventory.db
LOG_LEVEL=INFO
```

### 12.2 requirements.txt
```
Flask==2.3.0
Flask-CORS==4.0.0
Flask-JWT-Extended==4.5.0
SQLAlchemy==2.0.0
marshmallow==3.20.0
python-dotenv==1.0.0
pandas==2.0.0
openpyxl==3.1.0
APScheduler==3.10.0
pytest==7.4.0
```

### 12.3 실행 스크립트
```bash
#!/bin/bash
# run.sh

# 가상환경 활성화
source venv/bin/activate

# 환경 변수 로드
export $(cat .env | xargs)

# 데이터베이스 초기화
python migrations/init_db.py

# 서버 실행
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```