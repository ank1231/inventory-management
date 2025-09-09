# 재고관리시스템

쇼핑몰 재고 관리 시스템 - 네이버, 쿠팡, 자사몰 통합 관리

## 기능

- 재고 관리: 상품 등록, 수정, 삭제, 인라인 편집
- 판매 관리: 판매 기록, 수정, 삭제
- 리포트: 판매 분석, 재고 현황
- 멀티 플랫폼 지원: 네이버, 쿠팡, 자사몰
- 사용자 인증 시스템

## 설치 방법

### 로컬 개발 환경

1. 저장소 클론
```bash
git clone [your-repo-url]
cd 재고관리시스템
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. 필요 패키지 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 열고 필요한 값 설정
```

5. 애플리케이션 실행
```bash
python app.py
```

### 클라우드 배포 (Render.com)

1. GitHub에 코드 푸시
2. Render.com에서 새 Web Service 생성
3. GitHub 리포지토리 연결
4. 환경 변수 설정:
   - DATABASE_URL: PostgreSQL URL
   - SECRET_KEY: 비밀 키
   - ADMIN_USERNAME: 관리자 사용자명
   - ADMIN_EMAIL: 관리자 이메일
   - ADMIN_PASSWORD: 관리자 비밀번호

## 기본 로그인 정보

- 사용자명: admin
- 비밀번호: admin123!

첫 실행 시 자동으로 관리자 계정이 생성됩니다.

## 기술 스택

- Backend: Flask, Flask-Login
- Database: SQLite (로컬), PostgreSQL (클라우드)
- Frontend: Bootstrap 5
- Deployment: Render.com, ElephantSQL