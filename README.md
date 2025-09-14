# URL Shortener + QR (buly.kr API)

**Made by 인천영종고 오희찬**

URL 단축과 QR 코드 생성/해독을 한 번에 처리하는 웹 애플리케이션입니다.

## 주요 기능
- 🔗 URL 단축 (buly.kr API 연동)
- 📱 QR 코드 자동 생성
- 🔍 QR 이미지 해독
- 📋 원클릭 클립보드 복사
- 💾 QR 이미지 다운로드
- 🚀 서버리스 배포 지원

## 파일 구조
```
url-shortener-buly/
├── index.html          # 메인 웹 앱 (buly.kr API 연동)
├── standalone.html     # 독립 실행 버전 (API 없이 동작)
├── api/shorten.py      # Python Flask API
├── vercel.json         # Vercel 배포 설정
├── requirements.txt    # Python 의존성
└── .env.local         # 환경변수 (로컬 개발용)
```

## 로컬 개발

### 1. Vercel CLI 설치 및 실행
```bash
npm i -g vercel
cd url-shortener-buly
vercel dev
```

### 2. 환경변수 설정
`.env.local` 파일에 buly.kr API 정보가 포함되어 있습니다:
```
BULY_API_URL=https://alie.kr/api/shoturl.siso
BULY_CUSTOMER_ID=your_customer_id
BULY_PARTNER_API_ID=your_partner_api_id
```

### 3. 독립 실행 모드
서버 없이 바로 실행하려면 `standalone.html`을 브라우저에서 열어주세요.

## Vercel 배포

### 1. GitHub에 푸시
```bash
git remote add origin https://github.com/username/url-shortener-buly.git
git push -u origin main
```

### 2. Vercel 배포
```bash
vercel --prod
```

### 3. 환경변수 설정 (Vercel Dashboard)
- `BULY_API_URL`
- `BULY_CUSTOMER_ID`
- `BULY_PARTNER_API_ID`

## 기술 스택
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **QR Library**: QRCode.js, ZXing
- **Backend**: Python Flask (서버리스)
- **Deployment**: Vercel
- **API**: buly.kr URL Shortening Service

## 라이센스
© 2024 인천영종고 오희찬. All rights reserved.