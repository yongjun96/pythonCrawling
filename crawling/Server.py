from flask import Flask, request
import praw

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # 인증 코드 받기
        code = request.args.get('code')
        if code:
            # Reddit API에 인증 코드로 액세스 토큰 요청
            reddit = praw.Reddit(
                client_id='1ofVDcUQkMA4yYGcL_GcwQ',
                client_secret='QZ9FAwSqccYtIJ0PAVasvOMyf-0NbQ',
                redirect_uri='http://localhost:8080',
                user_agent='myCrawlingApp:v1.0 (by /u/Equal-Initiative-602)'  # user_agent 추가
            )
            token = reddit.auth.authorize(code)
            return f'Access Token: {token}'
        else:
            return 'Error: No code provided!', 400
    except Exception as e:
        # 예외 처리 및 오류 로그 출력
        return f'Internal Server Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(port=8080)
