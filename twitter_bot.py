import tweepy
import random
import time
import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

class GoogleSheetsTwitterBot:
    def __init__(self):
        """
        구글 시트 연동 트위터 봇
        """
        # 환경변수에서 API 키 가져오기
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        
        # 구글 시트 정보
        self.sheet_url = os.getenv('GOOGLE_SHEET_URL')  # 구글 시트 공유 링크
        self.service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')  # JSON 파일 내용
        
        # 트위터 API 초기화
        self.init_twitter_api()
        
        # 구글 시트 초기화
        self.init_google_sheets()
    
    def init_twitter_api(self):
        """
        트위터 API 초기화
        """
        try:
            auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
            
            self.client = tweepy.Client(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                wait_on_rate_limit=True
            )
            
            print("✅ 트위터 API 연결 성공!")
            
        except Exception as e:
            print(f"❌ 트위터 API 연결 실패: {e}")
            raise
    
    def init_google_sheets(self):
        """
        구글 시트 API 초기화
        """
        try:
            # 서비스 계정 인증 정보 설정
            import json
            service_account_info = json.loads(self.service_account_json)
            
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets.readonly',
                'https://www.googleapis.com/auth/drive.readonly'
            ]
            
            credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
            self.gc = gspread.authorize(credentials)
            
            # 시트 ID 추출 (URL에서)
            sheet_id = self.sheet_url.split('/d/')[1].split('/')[0]
            self.worksheet = self.gc.open_by_key(sheet_id).sheet1
            
            print("✅ 구글 시트 연결 성공!")
            
        except Exception as e:
            print(f"❌ 구글 시트 연결 실패: {e}")
            raise
    
    def get_tweets_from_sheet(self):
        """
        구글 시트에서 트윗 대사 가져오기
        """
        try:
            # A열의 모든 값 가져오기 (첫 번째 행은 헤더로 제외)
            all_values = self.worksheet.col_values(1)
            
            # 헤더 제거하고 빈 값 필터링
            tweets = [tweet.strip() for tweet in all_values[1:] if tweet.strip()]
            
            if not tweets:
                print("⚠️ 구글 시트에 트윗 내용이 없습니다")
                return ["기본 트윗입니다! 🤖"]
            
            print(f"📋 구글 시트에서 {len(tweets)}개의 트윗 로드 완료")
            return tweets
            
        except Exception as e:
            print(f"❌ 구글 시트 읽기 실패: {e}")
            # 에러 발생시 기본 메시지 반환
            return [
                "좋은 하루 되세요! 🌞",
                "오늘도 화이팅! 💪",
                "새로운 하루, 새로운 기회! ✨"
            ]
    
    def post_random_tweet(self):
        """
        구글 시트에서 랜덤 트윗 게시
        """
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # 구글 시트에서 트윗 목록 가져오기
                tweets = self.get_tweets_from_sheet()
                
                # 랜덤 선택
                selected_tweet = random.choice(tweets)
                
                # 트윗 길이 체크 (280자 제한)
                if len(selected_tweet) > 270:  # 여유분 10자
                    selected_tweet = selected_tweet[:267] + "..."
                
                # 트윗 게시
                response = self.client.create_tweet(text=selected_tweet)
                
                print(f"✅ 트윗 성공!")
                print(f"📝 내용: {selected_tweet}")
                print(f"🆔 트윗 ID: {response.data['id']}")
                print(f"⏰ 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                return True
                
            except tweepy.TooManyRequests:
                print("⏳ API 한도 초과 - 15분 대기 중...")
                time.sleep(15 * 60)
                retry_count += 1
                
            except tweepy.Unauthorized:
                print("❌ 인증 오류: 트위터 API 키를 확인하세요")
                return False
                
            except tweepy.Forbidden:
                print("❌ 권한 오류: 계정 상태나 트윗 내용을 확인하세요")
                return False
                
            except Exception as e:
                print(f"❌ 예상치 못한 오류: {e}")
                retry_count += 1
                
                if retry_count < max_retries:
                    wait_time = retry_count * 30
                    print(f"⏳ {wait_time}초 후 재시도... ({retry_count}/{max_retries})")
                    time.sleep(wait_time)
        
        print(f"❌ {max_retries}번 시도 후 실패")
        return False
    
    def test_connection(self):
        """
        연결 테스트
        """
        try:
            # 트위터 연결 테스트
            me = self.client.get_me()
            print(f"✅ 트위터 연결 성공! 계정: @{me.data.username}")
            
            # 구글 시트 연결 테스트
            tweets = self.get_tweets_from_sheet()
            print(f"✅ 구글 시트 연결 성공! {len(tweets)}개 트윗 로드됨")
            
            return True
            
        except Exception as e:
            print(f"❌ 연결 테스트 실패: {e}")
            return False

def main():
    """
    메인 함수 - GitHub Actions에서 실행됨
    """
    try:
        print("🤖 트위터 봇 시작...")
        print(f"⏰ 실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 봇 초기화
        bot = GoogleSheetsTwitterBot()
        
        # 연결 테스트
        if not bot.test_connection():
            print("❌ 연결 테스트 실패 - 봇 종료")
            return
        
        # 랜덤 트윗 게시
        success = bot.post_random_tweet()
        
        if success:
            print("🎉 트윗 게시 완료!")
        else:
            print("😞 트윗 게시 실패")
            
    except Exception as e:
        print(f"❌ 봇 실행 중 치명적 오류: {e}")

if __name__ == "__main__":
    main()
