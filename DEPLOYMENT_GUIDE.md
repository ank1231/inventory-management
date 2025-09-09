# 클라우드 배포 가이드

## 1단계: GitHub 리포지토리 생성

1. GitHub.com에 로그인
2. "New repository" 클릭
3. Repository name: "inventory-management-system"
4. Public/Private 선택
5. "Create repository" 클릭

## 2단계: 로컬 코드를 GitHub에 푸시

```bash
# GitHub 리포지토리 URL 추가
git remote add origin https://github.com/[your-username]/inventory-management-system.git

# 코드 푸시
git push -u origin master
```

## 3단계: ElephantSQL 데이터베이스 설정

1. https://www.elephantsql.com/ 접속
2. 회원가입 또는 로그인
3. "Create New Instance" 클릭
4. Name: "inventory-db"
5. Plan: "Tiny Turtle (Free)" 선택
6. Region: 가장 가까운 지역 선택
7. "Create" 클릭
8. Details 페이지에서 URL 복사 (postgresql://...)

## 4단계: Render.com 웹 서비스 생성

1. https://render.com/ 접속
2. 회원가입 또는 로그인
3. Dashboard에서 "New +" → "Web Service" 클릭
4. "Build and deploy from a Git repository" 선택
5. GitHub 계정 연결 및 리포지토리 선택

## 5단계: Render 서비스 설정

### 기본 설정
- Name: inventory-management
- Region: Singapore (또는 가까운 지역)
- Branch: master
- Root Directory: 비워둠
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

### 환경 변수 설정
"Environment" 탭에서 다음 변수들 추가:

1. DATABASE_URL
   - Value: ElephantSQL에서 복사한 PostgreSQL URL

2. SECRET_KEY
   - Value: 랜덤 문자열 생성 (예: `python -c "import secrets; print(secrets.token_hex(32))"`)

3. ADMIN_USERNAME
   - Value: admin (원하는 관리자 이름)

4. ADMIN_EMAIL
   - Value: admin@example.com (실제 이메일)

5. ADMIN_PASSWORD
   - Value: 강력한 비밀번호 설정

## 6단계: 배포

1. "Create Web Service" 클릭
2. 자동으로 빌드 및 배포 시작
3. 빌드 로그 확인
4. 배포 완료 후 제공된 URL로 접속

## 7단계: 첫 로그인

1. https://[your-app].onrender.com 접속
2. 설정한 ADMIN_USERNAME과 ADMIN_PASSWORD로 로그인

## 문제 해결

### 빌드 실패 시
- requirements.txt 파일 확인
- Python 버전 호환성 확인

### 데이터베이스 연결 실패 시
- DATABASE_URL 환경 변수 확인
- ElephantSQL 대시보드에서 연결 상태 확인

### 로그인 실패 시
- 환경 변수가 올바르게 설정되었는지 확인
- Render 로그에서 관리자 계정 생성 메시지 확인

## 추가 사용자 관리

현재는 초기 관리자 계정만 자동 생성됩니다. 추가 사용자 관리 기능이 필요한 경우:
1. 관리자 패널 구현
2. 사용자 등록 페이지 추가
3. 권한 관리 시스템 구현

## 데이터 마이그레이션

기존 SQLite 데이터를 PostgreSQL로 마이그레이션하려면:
1. 로컬에서 데이터 내보내기 스크립트 실행
2. PostgreSQL로 데이터 가져오기
3. 데이터 무결성 확인