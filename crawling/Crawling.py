import praw
import time  # time 모듈 임포트 추가
import pandas as pd

reddit = praw.Reddit(
    client_id="1ofVDcUQkMA4yYGcL_GcwQ",
    client_secret="QZ9FAwSqccYtIJ0PAVasvOMyf-0NbQ",
    redirect_uri="http://localhost:8080",
    user_agent="Equal-Initiative-602",
    token='164362093504778-c2yNCeWet99MDsNIJLcL_BZm6ZsF_g'  # Access Token
)

# 서브레딧 선택
subreddit = reddit.subreddit('KoreanLanguageShare')

# 게시물 크롤링
def crawl_subreddit(subreddit, limit=None):  # 모든 게시물 크롤링
    data = []  # 데이터를 저장할 리스트

    for submission in subreddit.new(limit=limit):
        print(f"Title: {submission.title}")
        print(f"Text: {submission.selftext}...")  # 본문 일부 출력

        # 댓글 크롤링
        submission.comments.replace_more(limit=0)
        comments = [comment.body for comment in submission.comments.list()]

        # 데이터 저장
        data.append({
            "Title": "제목 : "+submission.title,
            "Text": "내용 : "+submission.selftext,
            "Comments": "댓글 : \n".join(comments)  # 댓글 여러 개를 줄바꿈으로 저장
        })

        time.sleep(1)  # API 요청 속도 조절

    # CSV 파일 저장
    df = pd.DataFrame(data)
    df.to_csv("reddit_posts.csv", index=False, encoding="utf-8-sig")
    print("✅ 크롤링 완료! 'reddit_posts.csv' 파일로 저장되었습니다.")

# 크롤링 실행 (모든 게시물 크롤링)
crawl_subreddit(subreddit, limit=None)