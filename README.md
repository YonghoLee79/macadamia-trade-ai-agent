# 마카다미아 무역 데이터 AI 에이전트 🌰

전세계 마카다미아 수출입 정보를 매일 자동으로 수집하고 AI 분석을 제공하는 **웹 기반 모바일 적응형** 시스템입니다.

## ✨ 주요 기능

- **📱 모바일 적응형 웹 인터페이스**: 모든 디바이스에서 최적화된 사용자 경험
- **🤖 AI 기반 분석**: OpenAI GPT-4를 활용한 전문적인 무역 동향 분석
- **📊 실시간 대시보드**: 차트와 그래프로 시각화된 무역 데이터
- **🔄 자동 데이터 수집**: UN Comtrade, 한국 관세청 등에서 자동 수집
- **📈 인터랙티브 차트**: Chart.js를 활용한 동적 데이터 시각화
- **📋 자동 보고서 생성**: 매일 생성되는 상세 분석 보고서
- **⚡ 실시간 업데이트**: 시스템 상태 및 데이터 실시간 모니터링
- **📲 텔레그램 알림**: 신규 데이터, 분석 결과, 시스템 상태를 텔레그램으로 실시간 알림

## 🚀 빠른 시작

### 로컬 실행

1. **저장소 클론**:
```bash
git clone https://github.com/YonghoLee79/macadamia-trade-ai-agent.git
cd macadamia-trade-ai-agent
```

2. **가상환경 생성 및 활성화**:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는 Windows의 경우: venv\Scripts\activate
```

3. **의존성 설치**:
```bash
pip install -r requirements.txt
```

4. **환경 변수 설정**:
```bash
cp .env.example .env
# .env 파일에서 OpenAI API 키 설정
```

5. **웹 애플리케이션 실행**:
```bash
python app.py
```

6. **브라우저에서 접속**:
   - http://localhost:5000

### 🌐 온라인 배포 (Heroku)

1. **Heroku CLI 설치 및 로그인**:
```bash
heroku login
```

2. **Heroku 앱 생성**:
```bash
heroku create your-app-name
```

3. **환경 변수 설정**:
```bash
heroku config:set OPENAI_API_KEY=your_openai_api_key
heroku config:set DATABASE_URL=your_database_url  # PostgreSQL
```

4. **배포**:
```bash
git push heroku main
```

## 📱 웹 인터페이스 기능

### 📊 대시보드
- **실시간 통계**: 총 거래 건수, 거래 금액, 데이터 기간
- **주요 수출국/수입국**: 바차트와 도넛차트로 시각화
- **일별 거래 동향**: 라인차트로 트렌드 표시

### 🧠 AI 분석
- **기간별 분석**: 1일, 7일, 30일 기간 선택
- **실시간 분석**: OpenAI GPT-4 기반 전문 분석
- **상세 인사이트**: 시장 동향, 가격 트렌드, 주요 변화 분석

### ⚙️ 제어판
- **수동 데이터 수집**: 버튼 클릭으로 즉시 데이터 수집
- **보고서 생성**: AI 분석 보고서 즉시 생성
- **시스템 상태 모니터링**: 실시간 시스템 상태 확인

### 📄 보고서 관리
- **보고서 목록**: 생성된 모든 보고서 관리
- **보고서 뷰어**: 모달로 보고서 내용 확인
- **자동 생성**: 매일 자동으로 생성되는 분석 보고서

## 🏗️ 프로젝트 구조

```
macadamia-trade-ai-agent/
├── app.py                  # Flask 웹 애플리케이션 메인
├── config.py               # 설정 파일
├── models.py               # 데이터베이스 모델
├── data_scraper.py         # 데이터 수집 모듈
├── ai_agent.py             # AI 분석 모듈
├── scheduler.py            # 작업 스케줄러
├── main.py                 # CLI 실행 파일
├── requirements.txt        # Python 의존성
├── Procfile               # Heroku 배포 설정
├── runtime.txt            # Python 버전 설정
├── .env.example           # 환경 변수 예시
├── .gitignore             # Git 무시 파일
├── README.md              # 프로젝트 문서
├── templates/             # HTML 템플릿
│   └── index.html         # 메인 웹 페이지
├── static/                # 정적 파일
│   ├── css/              # CSS 파일
│   └── js/               # JavaScript 파일
└── reports/               # 생성된 보고서 저장 폴더
```

## 🌍 API 엔드포인트

### RESTful API
- `GET /api/dashboard` - 대시보드 데이터
- `GET /api/analysis/<days>` - AI 분석 결과
- `POST /api/collect` - 수동 데이터 수집
- `GET /api/reports` - 보고서 목록
- `GET /api/report/<filename>` - 특정 보고서 내용
- `GET /api/status` - 시스템 상태

## 📊 수집되는 정보

- **🌍 국가**: 수출국/수입국 정보
- **🏢 업체**: 수출업체/수입업체명
- **📦 품목**: 마카다미아 제품 상세 정보 (HS Code 기준)
- **💰 금액**: USD 기준 거래금액
- **📏 수량**: 거래량 및 단위
- **📅 날짜**: 거래 날짜

## 🔧 환경 변수

`.env` 파일에 다음 변수들을 설정해야 합니다:

```bash
# OpenAI API Key (필수)
OPENAI_API_KEY=your_openai_api_key_here

# 데이터베이스 URL (선택사항, 기본값: SQLite)
DATABASE_URL=sqlite:///macadamia_trade.db

# PostgreSQL 사용시 (프로덕션 환경)
# DATABASE_URL=postgresql://username:password@localhost/macadamia_trade

# Flask 설정
SECRET_KEY=your_secret_key_here
FLASK_ENV=development  # 또는 production
PORT=5000
```

## 🛠️ 기술 스택

### 백엔드
- **Python 3.9+**: 메인 프로그래밍 언어
- **Flask**: 웹 프레임워크
- **SQLAlchemy**: 데이터베이스 ORM
- **OpenAI GPT-4**: AI 분석 엔진
- **BeautifulSoup**: 웹 스크래핑
- **Schedule**: 작업 스케줄링
- **Pandas**: 데이터 처리
- **Requests**: HTTP 클라이언트
- **Gunicorn**: WSGI 서버

### 프론트엔드
- **HTML5/CSS3**: 마크업 및 스타일링
- **Bootstrap 5**: 반응형 UI 프레임워크
- **JavaScript (ES6+)**: 클라이언트 사이드 로직
- **Chart.js**: 데이터 시각화
- **Font Awesome**: 아이콘

### 데이터 소스
- **UN Comtrade**: 국제 무역 통계 데이터
- **한국 관세청**: 한국 수출입 데이터 
- **TradeMap**: 국제무역센터 무역 데이터

## 📱 모바일 최적화

- **반응형 디자인**: 모든 디바이스에서 최적화
- **터치 친화적**: 모바일 터치 인터페이스 지원
- **빠른 로딩**: 최적화된 리소스 로딩
- **오프라인 지원**: 캐시된 데이터로 오프라인 작업

## 🔒 보안

- **환경 변수**: 민감한 정보는 환경 변수로 관리
- **CORS 설정**: 적절한 Cross-Origin 설정
- **Input 검증**: 모든 사용자 입력 검증
- **Secret Key**: Flask 세션 보안

## 📈 모니터링

- **실시간 상태**: 시스템 상태 실시간 모니터링
- **에러 로깅**: 상세한 에러 로그 기록
- **성능 추적**: API 응답 시간 모니터링
- **자동 알림**: 시스템 이상 상황 알림

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

MIT License

## 📞 지원

문의사항이나 버그 리포트는 [Issues](https://github.com/YonghoLee79/macadamia-trade-ai-agent/issues)에 등록해주세요.

## 🎯 로드맵

- [ ] 다국어 지원 (영어, 중국어, 일본어)
- [ ] 실시간 알림 시스템
- [ ] 모바일 앱 버전
- [ ] 고급 필터링 및 검색
- [ ] 데이터 익스포트 기능
- [ ] 사용자 인증 시스템

---

**💻 개발자**: YonghoLee (todenny@me.com)  
**📅 생성일**: 2025년 7월 10일  
**🌟 버전**: 2.0 (웹 버전)
