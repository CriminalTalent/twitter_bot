# 🤖 구글 시트 연동 트위터 봇

구글 시트에서 대사를 가져와서 30분마다 자동으로 트윗하는 봇입니다. GitHub Actions으로 무료 운영 가능!

## 📋 필요한 것들

1. **GitHub 계정**
2. **트위터 개발자 계정**
3. **구글 클라우드 계정** (무료)
4. **구글 시트**

## 🚀 설정 방법

### 1️⃣ 트위터 API 설정

1. [developer.twitter.com](https://developer.twitter.com) 접속
2. 개발자 계정 신청 및 앱 생성
3. 다음 키들을 메모:
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret

### 2️⃣ 구글 시트 준비

1. **구글 시트 생성**
   ```
   A열에 트윗할 대사들 입력:
   
   A1: 트윗내용 (헤더)
   A2: 좋은 아침입니다! 🌅
   A3: 오늘도 화이팅! 💪
   A4: 휴식도 중요해요 ☕
   ...
   ```

2. **시트 공유 설정**
   - 공유 → 링크가 있는 모든 사용자 → 보기 권한
   - 링크 복사해서 메모

### 3️⃣ 구글 클라우드 API 설정

1. [console.cloud.google.com](https://console.cloud.google.com) 접속
2. 새 프로젝트 생성
3. **API 및 서비스** → **라이브러리**
4. 다음 API들 활성화:
   - Google Sheets API
   - Google Drive API

5. **사용자 인증 정보** → **사용자 인증 정보 만들기** → **서비스 계정**
6. 서비스 계정 생성 후 **키 추가** → **새 키 만들기** → **JSON**
7. 다운로드한 JSON 파일 내용 전체를 메모

### 4️⃣ GitHub 레포지토리 설정

1. **새 레포지토리 생성**
2. **파일 구조 만들기**:
   ```
   your-repo/
   ├── .github/
   │   └── workflows/
   │       └── twitter-bot.yml
   ├── twitter_bot.py
   ├── requirements.txt
   └── README.md
   ```

3. **GitHub Secrets 설정**
   - 레포지토리 → Settings → Secrets and variables → Actions
   - 다음 secrets 추가:
     ```
     TWITTER_API_KEY: (트위터 API Key)
     TWITTER_API_SECRET: (트위터 API Secret)
     TWITTER_ACCESS_TOKEN: (트위터 Access Token)
     TWITTER_ACCESS_TOKEN_SECRET: (트위터 Access Token Secret)
     GOOGLE_SHEET_URL: (구글 시트 공유 링크)
     GOOGLE_SERVICE_ACCOUNT_JSON: (JSON 파일 전체 내용)
     ```

### 5️⃣ 배포 및 실행

1. **모든 파일을 GitHub에 푸시**
2. **Actions 탭에서 실행 확인**
3. **수동 테스트**: Actions → Twitter Bot → Run workflow

## 📝 구글 시트 사용법

**A열에 트윗할 내용을 한 줄씩 입력하세요:**

| A열 (트윗내용) |
|----------------|
| 좋은 아침입니다! 🌅 |
| 오늘도 화이팅하세요! 💪 |
| 잠깐의 휴식도 중요해요 ☕ |
| 새로운 도전을 응원합니다! 🚀 |
| 감사한 마음으로 하루를 마무리해요 🌙 |

- **실시간 업데이트**: 시트를 수정하면 다음 트윗부터 반영
- **길이 제한**: 280자 초과시 자동으로 "..." 처리
- **이모지 사용 가능**: 🔥💪🌈✨ 등 자유롭게 사용

## ⚡ 주요 기능

- **30분마다 자동 트윗**
- **구글 시트에서 실시간 대사 로드**
- **랜덤 선택으로 중복 방지**
- **강력한 에러 처리**
- **무료 운영** (GitHub Actions 월 2,000분 무료)

## 🔧 커스터마이징

### 트윗 주기 변경
`.github/workflows/twitter-bot.yml` 파일에서:
```yaml
schedule:
  - cron: '*/15 * * * *'  # 15분마다
  - cron: '0 */2 * * *'   # 2시간마다
  - cron: '0 9,18 * * *'  # 매일 9시, 18시
```

### 여러 시트 사용
`twitter_bot.py`에서 워크시트 변경:
```python
self.worksheet = self.gc.open_by_key(sheet_id).worksheet('시트명')
```

## 🚨 주의사항

- **API 한도**: 트위터 무료 플랜은 월 1,500트윗
- **스팸 방지**: 의미있는 내용으로 구성
- **봇 표시**: 프로필에 봇임을 명시 권장
- **백업**: 중요한 대사는 따로 백업

## 🛠️ 문제해결

### GitHub Actions가 실행되지 않을 때
1. 레포지토리가 public인지 확인
2. Actions 권한 설정 확인 (Settings → Actions → General)

### 트윗이 올라가지 않을 때
1. Twitter API 키 확인
2. Actions 로그에서 에러 메시지 확인
3. 계정 상태 및 권한 확인

### 구글 시트를 읽지 못할 때
1. 시트 공유 설정 확인 (링크가 있는 모든 사용자)
2. Google Sheets API 활성화 확인
3. 서비스 계정 JSON 키 확인

## 📞 도움이 필요하면

GitHub Issues에 문제를 올려주세요! 🙋‍♂️
