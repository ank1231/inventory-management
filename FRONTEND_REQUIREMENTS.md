# 프론트엔드 개발 상세요건 문서

## 1. 기술 스택 및 도구

### 1.1 핵심 기술
- **HTML5**: 시맨틱 마크업
- **CSS3**: 스타일링
- **JavaScript**: ES6+ (바닐라 JS)
- **Bootstrap 5.3**: UI 프레임워크
- **Chart.js 4.0**: 데이터 시각화

### 1.2 추가 라이브러리
- **DataTables 1.13**: 테이블 관리
- **SweetAlert2**: 알림 및 확인 대화상자
- **Day.js**: 날짜 처리
- **Axios**: HTTP 통신
- **Font Awesome 6**: 아이콘

### 1.3 개발 도구
- **VS Code**: 에디터
- **Live Server**: 로컬 개발 서버
- **Chrome DevTools**: 디버깅

## 2. 프로젝트 구조

```
frontend/
├── templates/
│   ├── base.html           # 기본 레이아웃 템플릿
│   ├── index.html          # 대시보드
│   ├── inventory.html      # 재고 관리
│   ├── sales.html          # 판매 관리
│   ├── reports.html        # 리포트
│   └── components/
│       ├── navbar.html     # 네비게이션 바
│       ├── sidebar.html    # 사이드바
│       └── footer.html     # 푸터
│
├── static/
│   ├── css/
│   │   ├── style.css       # 메인 스타일
│   │   ├── dashboard.css   # 대시보드 스타일
│   │   ├── inventory.css   # 재고 페이지 스타일
│   │   ├── sales.css       # 판매 페이지 스타일
│   │   └── reports.css     # 리포트 페이지 스타일
│   │
│   ├── js/
│   │   ├── main.js         # 공통 기능
│   │   ├── api.js          # API 통신
│   │   ├── dashboard.js    # 대시보드 로직
│   │   ├── inventory.js    # 재고 관리 로직
│   │   ├── sales.js        # 판매 관리 로직
│   │   ├── reports.js      # 리포트 로직
│   │   ├── charts.js       # 차트 설정
│   │   └── utils.js        # 유틸리티 함수
│   │
│   └── img/
│       ├── logo.png
│       └── favicon.ico
```

## 3. 페이지별 상세 요구사항

### 3.1 공통 레이아웃 (base.html)

#### 3.1.1 헤더
```html
<!-- 네비게이션 구조 -->
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
        <a class="navbar-brand">
            <img src="/static/img/logo.png" height="30">
            재고관리시스템
        </a>
        <div class="navbar-nav ms-auto">
            <span class="navbar-text">admin</span>
            <button class="btn btn-outline-light ms-2">로그아웃</button>
        </div>
    </div>
</nav>
```

#### 3.1.2 사이드바
```html
<!-- 사이드바 메뉴 구조 -->
<div class="sidebar">
    <ul class="nav flex-column">
        <li class="nav-item">
            <a class="nav-link" href="/">
                <i class="fas fa-dashboard"></i> 대시보드
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="/inventory">
                <i class="fas fa-boxes"></i> 재고 관리
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="/sales">
                <i class="fas fa-shopping-cart"></i> 판매 관리
            </a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="/reports">
                <i class="fas fa-chart-bar"></i> 리포트
            </a>
        </li>
    </ul>
</div>
```

### 3.2 대시보드 페이지 (index.html)

#### 3.2.1 요약 카드
```html
<!-- KPI 카드 구조 -->
<div class="row mb-4">
    <div class="col-md-3">
        <div class="card text-white bg-primary">
            <div class="card-body">
                <h5 class="card-title">총 재고 수량</h5>
                <h2 class="card-text" id="totalQuantity">0</h2>
                <small>전체 상품 수량</small>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-success">
            <div class="card-body">
                <h5 class="card-title">총 재고 가치</h5>
                <h2 class="card-text" id="totalValue">₩0</h2>
                <small>재고 금액 합계</small>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-warning">
            <div class="card-body">
                <h5 class="card-title">오늘 매출</h5>
                <h2 class="card-text" id="todayRevenue">₩0</h2>
                <small>당일 판매액</small>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-info">
            <div class="card-body">
                <h5 class="card-title">오늘 순이익</h5>
                <h2 class="card-text" id="todayProfit">₩0</h2>
                <small>마진 적용 후</small>
            </div>
        </div>
    </div>
</div>
```

#### 3.2.2 빠른 판매 입력
```html
<!-- 빠른 판매 입력 폼 -->
<div class="card">
    <div class="card-header">
        <h5>빠른 판매 입력</h5>
    </div>
    <div class="card-body">
        <form id="quickSaleForm">
            <div class="row">
                <div class="col-md-3">
                    <select class="form-select" id="productSelect" required>
                        <option value="">상품 선택</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <input type="number" class="form-control" 
                           placeholder="수량" min="1" required>
                </div>
                <div class="col-md-2">
                    <select class="form-select" required>
                        <option value="">플랫폼</option>
                        <option value="A">A 플랫폼</option>
                        <option value="B">B 플랫폼</option>
                        <option value="C">C 플랫폼</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-primary">
                        판매 등록
                    </button>
                </div>
            </div>
        </form>
    </div>
</div>
```

#### 3.2.3 차트 영역
```html
<!-- 차트 컨테이너 -->
<div class="row mt-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">판매 추이</div>
            <div class="card-body">
                <canvas id="salesTrendChart"></canvas>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">플랫폼별 매출</div>
            <div class="card-body">
                <canvas id="platformRevenueChart"></canvas>
            </div>
        </div>
    </div>
</div>
```

### 3.3 재고 관리 페이지 (inventory.html)

#### 3.3.1 툴바
```html
<!-- 재고 관리 툴바 -->
<div class="d-flex justify-content-between mb-3">
    <div>
        <button class="btn btn-primary" data-bs-toggle="modal" 
                data-bs-target="#addProductModal">
            <i class="fas fa-plus"></i> 상품 추가
        </button>
        <button class="btn btn-success" id="exportBtn">
            <i class="fas fa-download"></i> CSV 내보내기
        </button>
    </div>
    <div class="d-flex">
        <input type="text" class="form-control me-2" 
               placeholder="상품 검색..." id="searchInput">
        <button class="btn btn-outline-secondary" id="searchBtn">
            <i class="fas fa-search"></i>
        </button>
    </div>
</div>
```

#### 3.3.2 재고 테이블
```html
<!-- DataTable 구조 -->
<table id="inventoryTable" class="table table-striped">
    <thead>
        <tr>
            <th>ID</th>
            <th>상품명</th>
            <th>가격</th>
            <th>A 마진(%)</th>
            <th>B 마진(%)</th>
            <th>C 마진(%)</th>
            <th>재고 수량</th>
            <th>재고 가치</th>
            <th>작업</th>
        </tr>
    </thead>
    <tbody>
        <!-- 동적 생성 -->
    </tbody>
</table>
```

#### 3.3.3 상품 추가/수정 모달
```html
<!-- 상품 모달 -->
<div class="modal fade" id="productModal">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">상품 정보</h5>
                <button type="button" class="btn-close" 
                        data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form id="productForm">
                    <div class="mb-3">
                        <label class="form-label">상품명</label>
                        <input type="text" class="form-control" 
                               name="name" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">가격</label>
                        <input type="number" class="form-control" 
                               name="price" min="0" required>
                    </div>
                    <div class="row">
                        <div class="col-md-4">
                            <label class="form-label">A 마진(%)</label>
                            <input type="number" class="form-control" 
                                   name="margin_a" min="0" max="100">
                        </div>
                        <div class="col-md-4">
                            <label class="form-label">B 마진(%)</label>
                            <input type="number" class="form-control" 
                                   name="margin_b" min="0" max="100">
                        </div>
                        <div class="col-md-4">
                            <label class="form-label">C 마진(%)</label>
                            <input type="number" class="form-control" 
                                   name="margin_c" min="0" max="100">
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">재고 수량</label>
                        <input type="number" class="form-control" 
                               name="quantity" min="0" required>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" 
                        data-bs-dismiss="modal">취소</button>
                <button type="submit" class="btn btn-primary" 
                        form="productForm">저장</button>
            </div>
        </div>
    </div>
</div>
```

### 3.4 판매 관리 페이지 (sales.html)

#### 3.4.1 판매 입력 폼
```html
<!-- 판매 입력 섹션 -->
<div class="card mb-4">
    <div class="card-header">
        <h5>판매 등록</h5>
    </div>
    <div class="card-body">
        <form id="saleForm">
            <div class="row">
                <div class="col-md-3">
                    <label class="form-label">판매일</label>
                    <input type="date" class="form-control" 
                           name="sale_date" required>
                </div>
                <div class="col-md-3">
                    <label class="form-label">상품</label>
                    <select class="form-select" name="product_id" required>
                        <option value="">선택...</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <label class="form-label">수량</label>
                    <input type="number" class="form-control" 
                           name="quantity" min="1" required>
                    <small class="text-muted">재고: <span id="stockInfo">0</span>개</small>
                </div>
                <div class="col-md-2">
                    <label class="form-label">플랫폼</label>
                    <select class="form-select" name="platform" required>
                        <option value="">선택...</option>
                        <option value="A">A 플랫폼</option>
                        <option value="B">B 플랫폼</option>
                        <option value="C">C 플랫폼</option>
                    </select>
                </div>
                <div class="col-md-2 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary w-100">
                        판매 등록
                    </button>
                </div>
            </div>
        </form>
    </div>
</div>
```

#### 3.4.2 판매 내역 테이블
```html
<!-- 판매 내역 -->
<div class="card">
    <div class="card-header d-flex justify-content-between">
        <h5>판매 내역</h5>
        <div>
            <input type="date" class="form-control" id="filterDate">
        </div>
    </div>
    <div class="card-body">
        <table id="salesTable" class="table">
            <thead>
                <tr>
                    <th>판매일</th>
                    <th>상품명</th>
                    <th>수량</th>
                    <th>플랫폼</th>
                    <th>매출</th>
                    <th>순이익</th>
                    <th>작업</th>
                </tr>
            </thead>
            <tbody>
                <!-- 동적 생성 -->
            </tbody>
        </table>
    </div>
</div>
```

### 3.5 리포트 페이지 (reports.html)

#### 3.5.1 기간 선택기
```html
<!-- 리포트 기간 선택 -->
<div class="card mb-4">
    <div class="card-body">
        <div class="row">
            <div class="col-md-3">
                <label class="form-label">기간 선택</label>
                <select class="form-select" id="periodSelect">
                    <option value="daily">일간</option>
                    <option value="weekly">주간</option>
                    <option value="monthly">월간</option>
                    <option value="custom">사용자 지정</option>
                </select>
            </div>
            <div class="col-md-3">
                <label class="form-label">시작일</label>
                <input type="date" class="form-control" id="startDate">
            </div>
            <div class="col-md-3">
                <label class="form-label">종료일</label>
                <input type="date" class="form-control" id="endDate">
            </div>
            <div class="col-md-3 d-flex align-items-end">
                <button class="btn btn-primary w-100" id="generateReport">
                    리포트 생성
                </button>
            </div>
        </div>
    </div>
</div>
```

#### 3.5.2 통계 카드
```html
<!-- 리포트 통계 -->
<div class="row mb-4">
    <div class="col-md-3">
        <div class="card border-primary">
            <div class="card-body text-center">
                <h6>총 판매 수량</h6>
                <h3 id="totalSalesQty">0</h3>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card border-success">
            <div class="card-body text-center">
                <h6>총 매출</h6>
                <h3 id="totalRevenue">₩0</h3>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card border-warning">
            <div class="card-body text-center">
                <h6>총 순이익</h6>
                <h3 id="totalProfit">₩0</h3>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card border-info">
            <div class="card-body text-center">
                <h6>평균 마진율</h6>
                <h3 id="avgMargin">0%</h3>
            </div>
        </div>
    </div>
</div>
```

## 4. JavaScript 기능 구현

### 4.1 API 통신 모듈 (api.js)
```javascript
// API 기본 설정
const API_BASE_URL = 'http://localhost:5000/api';

// API 함수들
const api = {
    // 재고 관련
    getProducts: () => axios.get(`${API_BASE_URL}/products`),
    getProduct: (id) => axios.get(`${API_BASE_URL}/products/${id}`),
    createProduct: (data) => axios.post(`${API_BASE_URL}/products`, data),
    updateProduct: (id, data) => axios.put(`${API_BASE_URL}/products/${id}`, data),
    deleteProduct: (id) => axios.delete(`${API_BASE_URL}/products/${id}`),
    
    // 판매 관련
    getSales: (params) => axios.get(`${API_BASE_URL}/sales`, { params }),
    createSale: (data) => axios.post(`${API_BASE_URL}/sales`, data),
    deleteSale: (id) => axios.delete(`${API_BASE_URL}/sales/${id}`),
    
    // 리포트 관련
    getReport: (params) => axios.get(`${API_BASE_URL}/reports`, { params }),
    exportCSV: () => axios.get(`${API_BASE_URL}/export/csv`, { responseType: 'blob' })
};
```

### 4.2 유틸리티 함수 (utils.js)
```javascript
// 숫자 포맷팅
function formatCurrency(amount) {
    return new Intl.NumberFormat('ko-KR', {
        style: 'currency',
        currency: 'KRW'
    }).format(amount);
}

// 날짜 포맷팅
function formatDate(date) {
    return dayjs(date).format('YYYY-MM-DD');
}

// 퍼센트 포맷팅
function formatPercent(value) {
    return `${value.toFixed(1)}%`;
}

// 에러 메시지 표시
function showError(message) {
    Swal.fire({
        icon: 'error',
        title: '오류',
        text: message
    });
}

// 성공 메시지 표시
function showSuccess(message) {
    Swal.fire({
        icon: 'success',
        title: '성공',
        text: message,
        timer: 2000
    });
}

// 확인 대화상자
function confirmAction(message) {
    return Swal.fire({
        icon: 'warning',
        title: '확인',
        text: message,
        showCancelButton: true,
        confirmButtonText: '확인',
        cancelButtonText: '취소'
    });
}
```

### 4.3 차트 설정 (charts.js)
```javascript
// 차트 기본 설정
Chart.defaults.font.family = 'Noto Sans KR';
Chart.defaults.color = '#666';

// 판매 추이 차트
function createSalesTrendChart(canvasId, data) {
    return new Chart(document.getElementById(canvasId), {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: '매출',
                data: data.revenue,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }, {
                label: '순이익',
                data: data.profit,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            return `${context.dataset.label}: ${formatCurrency(context.raw)}`;
                        }
                    }
                }
            }
        }
    });
}

// 플랫폼별 매출 차트
function createPlatformChart(canvasId, data) {
    return new Chart(document.getElementById(canvasId), {
        type: 'doughnut',
        data: {
            labels: ['A 플랫폼', 'B 플랫폼', 'C 플랫폼'],
            datasets: [{
                data: [data.A, data.B, data.C],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'right' }
            }
        }
    });
}
```

## 5. CSS 스타일링

### 5.1 공통 스타일 (style.css)
```css
/* 변수 정의 */
:root {
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --success-color: #28a745;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
    --info-color: #17a2b8;
    --sidebar-width: 250px;
}

/* 레이아웃 */
body {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: #f8f9fa;
}

.wrapper {
    display: flex;
    min-height: 100vh;
}

/* 사이드바 */
.sidebar {
    width: var(--sidebar-width);
    background: linear-gradient(180deg, #343a40 0%, #212529 100%);
    min-height: 100vh;
    position: fixed;
    left: 0;
    top: 56px;
    z-index: 100;
}

.sidebar .nav-link {
    color: #adb5bd;
    padding: 12px 20px;
    transition: all 0.3s;
}

.sidebar .nav-link:hover {
    color: #fff;
    background-color: rgba(255,255,255,0.1);
}

.sidebar .nav-link.active {
    color: #fff;
    background-color: var(--primary-color);
}

/* 메인 컨텐츠 */
.main-content {
    margin-left: var(--sidebar-width);
    padding: 20px;
    width: calc(100% - var(--sidebar-width));
    margin-top: 56px;
}

/* 카드 */
.card {
    border: none;
    box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075);
    margin-bottom: 20px;
}

.card-header {
    background-color: #fff;
    border-bottom: 1px solid #e3e6f0;
    font-weight: 600;
}

/* 테이블 */
.table {
    font-size: 14px;
}

.table thead th {
    border-bottom: 2px solid #dee2e6;
    font-weight: 600;
    color: #495057;
}

/* 버튼 */
.btn {
    font-size: 14px;
    padding: 8px 16px;
}

/* 폼 */
.form-label {
    font-weight: 500;
    color: #495057;
    margin-bottom: 5px;
}

.form-control:focus,
.form-select:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
}

/* 반응형 */
@media (max-width: 768px) {
    .sidebar {
        transform: translateX(-100%);
        transition: transform 0.3s;
    }
    
    .sidebar.show {
        transform: translateX(0);
    }
    
    .main-content {
        margin-left: 0;
        width: 100%;
    }
}
```

## 6. 반응형 디자인

### 6.1 브레이크포인트
- **XS**: < 576px (모바일)
- **SM**: ≥ 576px (태블릿 세로)
- **MD**: ≥ 768px (태블릿 가로)
- **LG**: ≥ 992px (데스크톱)
- **XL**: ≥ 1200px (대형 데스크톱)

### 6.2 반응형 전략
- 모바일: 사이드바 숨김, 햄버거 메뉴
- 태블릿: 사이드바 축소, 카드 2열
- 데스크톱: 전체 레이아웃 표시

## 7. 성능 최적화

### 7.1 로딩 최적화
- 지연 로딩 (Lazy Loading)
- 코드 스플리팅
- 이미지 최적화
- CDN 사용

### 7.2 렌더링 최적화
- Virtual DOM 사용 검토
- 디바운싱/쓰로틀링
- 메모이제이션
- 웹 워커 활용

## 8. 접근성 (A11y)

### 8.1 ARIA 속성
- role 속성 사용
- aria-label 제공
- aria-describedby 활용

### 8.2 키보드 네비게이션
- Tab 순서 관리
- 포커스 표시
- 단축키 지원

## 9. 브라우저 호환성

### 9.1 지원 브라우저
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### 9.2 폴리필
- Promise
- Fetch API
- ES6 기능

## 10. 테스트 전략

### 10.1 단위 테스트
- 유틸리티 함수
- API 통신
- 데이터 검증

### 10.2 E2E 테스트
- 사용자 시나리오
- 폼 제출
- 네비게이션

## 11. 보안 고려사항

### 11.1 XSS 방지
- 입력값 sanitize
- innerHTML 사용 자제
- Content Security Policy

### 11.2 CSRF 방지
- CSRF 토큰 사용
- SameSite 쿠키

## 12. 국제화 (i18n)

### 12.1 언어 지원
- 한국어 (기본)
- 영어 (추후)

### 12.2 로케일
- 날짜 형식: YYYY-MM-DD
- 숫자 형식: 1,000
- 통화 형식: ₩1,000