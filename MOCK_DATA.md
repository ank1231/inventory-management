# Mock 데이터 정의서

## 1. Mock 데이터 사용 영역

### 1.1 완전 Mock 데이터 영역
아래 항목들은 실제 연동이 필요하나 현재 구현에서는 Mock 데이터로 처리됩니다:

#### 외부 플랫폼 연동
- **실제 필요**: 각 플랫폼(A, B, C)의 실제 API 연동
- **Mock 처리**: 플랫폼 정보를 하드코딩된 상수로 처리
- **영향**: 실시간 플랫폼 수수료율 변경 반영 불가

#### 결제 시스템
- **실제 필요**: PG사 연동, 결제 검증
- **Mock 처리**: 모든 결제를 성공으로 가정
- **영향**: 실제 금융 거래 불가

#### 배송 추적
- **실제 필요**: 택배사 API 연동
- **Mock 처리**: 배송 상태를 수동 입력
- **영향**: 실시간 배송 추적 불가

#### 사용자 인증
- **실제 필요**: OAuth, SSO 등 인증 시스템
- **Mock 처리**: 하드코딩된 단일 사용자 (admin/admin)
- **영향**: 다중 사용자 지원 불가, 보안 취약

### 1.2 부분 Mock 데이터 영역

#### 이메일 알림
- **실제 필요**: SMTP 서버 설정
- **Mock 처리**: 콘솔 로그로 대체
- **영향**: 실제 이메일 발송 불가

#### 백업 시스템
- **실제 필요**: 클라우드 스토리지 연동
- **Mock 처리**: 로컬 파일 시스템에 저장
- **영향**: 외부 백업 불가

## 2. Mock 데이터 상세

### 2.1 초기 상품 데이터
```python
MOCK_PRODUCTS = [
    {
        "id": 1,
        "name": "물건 a",
        "price": 23000,
        "margin_a": 30,  # A 플랫폼 마진율 (%)
        "margin_b": 25,  # B 플랫폼 마진율 (%)
        "margin_c": 19,  # C 플랫폼 마진율 (%)
        "quantity": 40
    },
    {
        "id": 2,
        "name": "물건 b",
        "price": 62000,
        "margin_a": 23,
        "margin_b": 45,
        "margin_c": 40,
        "quantity": 20
    },
    {
        "id": 3,
        "name": "물건 c",
        "price": 94000,
        "margin_a": 50,
        "margin_b": 40,
        "margin_c": 17,
        "quantity": 56
    },
    {
        "id": 4,
        "name": "물건 d",
        "price": 5000,
        "margin_a": 20,
        "margin_b": 23,
        "margin_c": 10,
        "quantity": 94
    },
    {
        "id": 5,
        "name": "물건 e",
        "price": 35000,
        "margin_a": 25,
        "margin_b": 30,
        "margin_c": 22,
        "quantity": 30
    },
    {
        "id": 6,
        "name": "물건 f",
        "price": 48000,
        "margin_a": 35,
        "margin_b": 28,
        "margin_c": 20,
        "quantity": 45
    },
    {
        "id": 7,
        "name": "물건 g",
        "price": 15000,
        "margin_a": 18,
        "margin_b": 20,
        "margin_c": 15,
        "quantity": 60
    },
    {
        "id": 8,
        "name": "물건 h",
        "price": 72000,
        "margin_a": 40,
        "margin_b": 35,
        "margin_c": 30,
        "quantity": 25
    },
    {
        "id": 9,
        "name": "물건 i",
        "price": 28000,
        "margin_a": 22,
        "margin_b": 25,
        "margin_c": 18,
        "quantity": 50
    },
    {
        "id": 10,
        "name": "물건 j",
        "price": 86000,
        "margin_a": 45,
        "margin_b": 42,
        "margin_c": 38,
        "quantity": 15
    }
]
```

### 2.2 Mock 판매 데이터 (테스트용)
```python
MOCK_SALES = [
    {
        "id": 1,
        "product_id": 2,  # 물건 b
        "sale_date": "2024-01-15",
        "quantity": 5,
        "platform": "A",
        "revenue": 310000,  # 62000 * 5
        "profit": 238700   # 310000 * (1 - 0.23)
    },
    {
        "id": 2,
        "product_id": 4,  # 물건 d
        "sale_date": "2024-01-15",
        "quantity": 30,
        "platform": "B",
        "revenue": 150000,  # 5000 * 30
        "profit": 115500   # 150000 * (1 - 0.23)
    },
    {
        "id": 3,
        "product_id": 1,  # 물건 a
        "sale_date": "2024-01-14",
        "quantity": 10,
        "platform": "C",
        "revenue": 230000,  # 23000 * 10
        "profit": 186300   # 230000 * (1 - 0.19)
    }
]
```

### 2.3 Mock 사용자 데이터
```python
MOCK_USER = {
    "username": "admin",
    "password": "admin",  # 실제로는 해시 처리 필요
    "email": "admin@example.com",
    "role": "administrator",
    "created_at": "2024-01-01"
}
```

### 2.4 Mock 플랫폼 설정
```python
MOCK_PLATFORMS = {
    "A": {
        "name": "A 플랫폼",
        "api_endpoint": "https://api.platform-a.com",  # Mock URL
        "api_key": "mock_api_key_a",
        "status": "connected"  # 항상 연결됨으로 표시
    },
    "B": {
        "name": "B 플랫폼",
        "api_endpoint": "https://api.platform-b.com",
        "api_key": "mock_api_key_b",
        "status": "connected"
    },
    "C": {
        "name": "C 플랫폼",
        "api_endpoint": "https://api.platform-c.com",
        "api_key": "mock_api_key_c",
        "status": "connected"
    }
}
```

## 3. Mock 데이터 생성 함수

### 3.1 랜덤 판매 데이터 생성
```python
def generate_mock_sale():
    """테스트용 랜덤 판매 데이터 생성"""
    import random
    from datetime import datetime, timedelta
    
    product = random.choice(MOCK_PRODUCTS)
    platform = random.choice(['A', 'B', 'C'])
    quantity = random.randint(1, min(10, product['quantity']))
    
    # 마진율 가져오기
    margin_key = f"margin_{platform.lower()}"
    margin_rate = product[margin_key] / 100
    
    revenue = product['price'] * quantity
    profit = revenue * (1 - margin_rate)
    
    # 최근 30일 내 랜덤 날짜
    sale_date = datetime.now() - timedelta(days=random.randint(0, 30))
    
    return {
        "product_id": product['id'],
        "sale_date": sale_date.strftime("%Y-%m-%d"),
        "quantity": quantity,
        "platform": platform,
        "revenue": revenue,
        "profit": profit
    }
```

### 3.2 Mock 알림 생성
```python
def generate_mock_notification(type, message):
    """실제 알림 대신 콘솔 출력"""
    print(f"[MOCK NOTIFICATION - {type}] {message}")
    return {
        "status": "sent",
        "timestamp": datetime.now().isoformat(),
        "type": type,
        "message": message
    }
```

## 4. Mock 데이터 제한사항

### 4.1 기능적 제한
- 실시간 데이터 동기화 불가
- 외부 시스템과의 실제 연동 불가
- 멀티 유저 환경 테스트 불가
- 실제 금융 거래 처리 불가

### 4.2 데이터 제한
- 최대 1000개 상품만 효율적 처리
- 판매 기록은 메모리 제한에 따름
- 백업은 로컬 저장소 용량에 의존

## 5. 실제 구현 시 필요한 연동

### 5.1 우선순위 높음
1. **사용자 인증 시스템**: JWT, OAuth 2.0
2. **데이터베이스 서버**: PostgreSQL, MySQL
3. **플랫폼 API**: 각 판매 플랫폼의 공식 API

### 5.2 우선순위 중간
1. **이메일 서비스**: SendGrid, AWS SES
2. **백업 시스템**: AWS S3, Google Cloud Storage
3. **로깅 시스템**: ELK Stack, CloudWatch

### 5.3 우선순위 낮음
1. **배송 추적**: 택배사 API
2. **결제 시스템**: PG사 연동
3. **분석 도구**: Google Analytics, Mixpanel

## 6. Mock에서 실제로 전환 가이드

### 6.1 단계별 전환 계획
1. **Phase 1**: 데이터베이스 실제 서버로 이전
2. **Phase 2**: 사용자 인증 시스템 구현
3. **Phase 3**: 플랫폼 API 연동
4. **Phase 4**: 알림 및 백업 시스템 구현
5. **Phase 5**: 고급 기능 추가

### 6.2 전환 시 주의사항
- Mock 데이터와 실제 데이터 마이그레이션 계획 수립
- API 키 및 인증 정보 보안 관리
- 점진적 전환으로 서비스 중단 최소화
- 각 단계별 롤백 계획 수립