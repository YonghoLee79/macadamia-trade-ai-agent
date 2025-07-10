FROM python:3.12-slim

# 시스템 패키지 업데이트 및 PostgreSQL 개발 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# pip 업그레이드
RUN pip install --upgrade pip

COPY requirements.txt .

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 시작 스크립트에 실행 권한 부여
RUN chmod +x start.sh

EXPOSE 8080

# Railway에서 PORT 환경변수를 제공하지 않는 경우를 대비해 기본값 설정
ENV PORT=8080

CMD ["./start.sh"]
