# 마카다미아 무역 데이터 AI 에이전트

전세계 마카다미아 수출입 정보를 매일 자동으로 수집하고 AI 분석을 제공하는 시스템입니다.

## 주요 기능

- **자동 데이터 수집**: UN Comtrade, 한국 관세청 등에서 마카다미아 무역 데이터 수집
- **AI 분석**: OpenAI GPT-4를 활용한 무역 동향 분석
- **일일 보고서**: 매일 자동 생성되는 상세 분석 보고서
- **데이터베이스 저장**: SQLite/PostgreSQL 지원

## 설치 방법

1. 저장소 클론:
```bash
git clone https://github.com/yourusername/macadamia-trade-agent.git
cd macadamia-trade-agent
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정:
```bash
cp .env.example .env
# .env 파일에서 API 키 설정
```

4. 데이터베이스 초기화:
```bash
python main.py --mode collect
```

## 사용 방법

### 스케줄러 실행 (매일 자동)
```bash
python main.py --mode schedule
```

### 수동 데이터 수집
```bash
python main.py --mode collect
```

### 분석만 실행
```bash
python main.py --mode analyze --days 7
```

## 수집되는 정보

- **국가**: 수출국/수입국 정보
- **업체**: 수출업체/수입업체명
- **품목**: 마카다미아 제품 상세 정보 (HS Code 기준)
- **금액**: USD 기준 거래금액
- **수량**: 거래량 및 단위
- **날짜**: 거래 날짜

## 보고서 예시

일일 보고서는 `reports/` 폴더에 저장되며 다음 내용을 포함합니다:

- 주요 수출국/수입국 동향
- 거래량 및 금액 변화
- 주요 무역업체 분석
- 가격 트렌드
- 시장 인사이트

## 기술 스택

- Python 3.8+
- SQLAlchemy (데이터베이스 ORM)
- OpenAI GPT-4 (AI 분석)
- BeautifulSoup (웹 스크래핑)
- Schedule (작업 스케줄링)

## 라이선스

MIT License

## 기여 방법

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
