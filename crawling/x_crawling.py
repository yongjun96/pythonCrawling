import re
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


import time

options = Options()
# options.add_argument("user-data-dir=C:\\Users\\practice960426@gmail.com\\AppData\\Local\\Google\\Chrome\\User Data")  # 맥용
options.add_argument('--user-data-dir=C:\\crawling')  # 윈도우용
# options.add_argument("--headless=new")  # 필요 시 헤드리스 모드

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")


driver = webdriver.Chrome(options=options)
driver.get("https://x.com")

time.sleep(2)


# try:
#     # 로그인 버튼이 클릭 가능할 때까지 기다림
#     login_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//a[@href='/login']"))
#     )
#     login_button.click()  # 로그인 버튼 클릭
#     print("로그인 버튼 클릭 완료")
# except Exception as e:
#     print("오류 발생:", e)
#
# time.sleep(2)
#
# try:
#     # 이메일 입력 필드가 보일 때까지 기다림
#     email_input = WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located((By.NAME, "text"))  # 또는 By.CSS_SELECTOR로도 가능
#     )
#     email_input.send_keys("danji0123456@naver.com")
#     print("이메일 입력 완료")
# except Exception as e:
#     print("오류 발생:", e)
#
#
# time.sleep(2)
#
# try:
#     # "다음" 텍스트를 가진 span 요소가 클릭 가능할 때까지 기다림
#     next_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//span[span[text()='다음']]"))
#     )
#     next_button.click()  # "다음" 텍스트를 가진 span 요소 클릭
#     print("다음 버튼 클릭 완료")
# except Exception as e:
#     print("오류 발생:", e)
#
# time.sleep(2)
#
# try:
#     # 해당 인풋 요소가 로드될 때까지 기다림
#     password_input = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.NAME, "text"))  # name 속성을 사용하여 요소 찾기
#     )
#     password_input.send_keys("@yongjun960426")  # 비밀번호 입력
#     print("계정 이름 입력 완료")
# except Exception as e:
#     print("오류 발생:", e)
#
# time.sleep(2)
#
# try:
#     # '다음' 텍스트가 포함된 span 요소가 로드될 때까지 기다림
#     next_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//span[text()='다음']"))
#     )
#     next_button.click()  # '다음' 버튼 클릭
#     print("다음 버튼 클릭 완료")
# except Exception as e:
#     print("오류 발생:", e)
#
# time.sleep(2)
#
# try:
#     # 비밀번호 입력 필드가 로드될 때까지 기다림
#     password_input = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.NAME, "password"))
#     )
#     password_input.send_keys("dydwns!1004")  # 비밀번호 입력
#     print("비밀번호 입력 완료")
# except Exception as e:
#     print("오류 발생:", e)
#
# time.sleep(2)
#
# try:
#     # '로그인하기' 버튼이 로드될 때까지 기다림
#     login_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//span[text()='로그인하기']"))
#     )
#     login_button.click()  # 로그인하기 버튼 클릭
#     print("로그인하기 버튼 클릭 완료")
# except Exception as e:
#     print("오류 발생:", e)

# ------------------------- 로그인 완료

try:
    # Search 인풋 요소가 로드될 때까지 기다림
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='SearchBox_Search_Input']"))
    )
    search_input.clear()
    search_input.send_keys("korean")
    search_input.send_keys(Keys.ENTER)  # 엔터키 입력
    print("검색어 입력 완료")
except Exception as e:
    print("오류 발생:", e)

time.sleep(2)

tweets = driver.find_elements(By.XPATH, '//article[@role="article"]')

time.sleep(2)

# ----------------------------------------- 여기 부터 본문 크롤링

from selenium.webdriver.common.by import By
import csv
import time

# ✅ 검색어 리스트 (원하는 만큼 추가 가능)
search_keywords = ["korean"]

for keyword in search_keywords:
    print(f"\n🔍 '{keyword}' 검색 시작")

    # ✅ 검색창에 검색어 입력
    try:
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='SearchBox_Search_Input']"))
        )
        search_input.clear()
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.ENTER)
        print("   └ 검색어 입력 완료")
    except Exception as e:
        print("   ❌ 검색창 오류:", e)
        continue

    time.sleep(2)

    # ✅ 스크롤 및 게시물 수집
    scroll_pause_time = 1.5
    scroll_step = 500
    max_attempts = 200
    scroll_retry_limit = 5

    attempt = 0
    same_batch_count = 0
    previous_batch = []
    scroll_retries = 0
    collected_posts = []

    while attempt < max_attempts:
        attempt += 1
        new_keys = []
        new_authors = []

        articles = driver.find_elements(By.XPATH, '//article[@role="article"]')
        articles_with_position = [
            (article, driver.execute_script("return arguments[0].getBoundingClientRect().top;", article))
            for article in articles
        ]
        articles_sorted = sorted(articles_with_position, key=lambda x: x[1])

        for article, _ in articles_sorted:
            try:
                tweet_container = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']")
                hashtag_elements = article.find_elements(
                    By.XPATH,
                    ".//a[contains(@href, '/hashtag/') and contains(@class, 'css-1jxf684')]"
                )
                hashtags = [tag.text for tag in hashtag_elements]
                for tag in hashtag_elements:
                    driver.execute_script("arguments[0].remove();", tag)

                tweet_text = tweet_container.text.strip()
                username_element = article.find_element(By.XPATH, ".//span[contains(@class,'css-1jxf684')]")
                username = username_element.text.strip() if username_element else "이름 없음"

                collected_posts.append({
                    "username": username,
                    "text": tweet_text,
                    "hashtags": hashtags,
                    "time": article.find_element(By.XPATH, ".//time").get_attribute("datetime") if article.find_elements(By.XPATH, ".//time") else "작성일 없음"
                })

                key = f"{username}_{tweet_text}"
                new_keys.append(key)
                new_authors.append(username)

            except Exception:
                continue

        print(f"   🔁 스크롤 {attempt}회차 - 새 게시물 {len(new_authors)}개 (총 {len(collected_posts)}개)")
        if new_authors:
            print(f"      └ 수집된 작성자: {', '.join(new_authors)}")

        if len(collected_posts) == len(previous_batch):
            same_batch_count += 1
        else:
            same_batch_count = 0
            scroll_retries = 0

        previous_batch = list(collected_posts)

        if same_batch_count >= 4:
            if scroll_retries >= scroll_retry_limit:
                print("   🛑 더 이상 게시물이 없어 수집 종료")
                break
            else:
                print(f"   ⏫ 스크롤 재시도 중... ({scroll_retries + 1}/{scroll_retry_limit})")
                driver.execute_script("window.scrollBy(0, -1000);")
                time.sleep(scroll_pause_time)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_pause_time)
                scroll_retries += 1
                continue

        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        time.sleep(scroll_pause_time)

    # ✅ 중복 제거
    seen_keys = set()
    filtered_posts = []
    for post in collected_posts:
        key = f"{post['username']}_{post['text']}"
        if key in seen_keys:
            continue
        seen_keys.add(key)
        filtered_posts.append(post)

    # ✅ 검색어 기반 파일명 (공백 제거)
    safe_keyword = keyword.replace(" ", "_")
    output_filename = f"{safe_keyword}_twitter_posts.csv"

    with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["username", "time", "text", "hashtags"])
        writer.writeheader()
        for post in filtered_posts:
            writer.writerow({
                "username": post["username"],
                "time": post["time"],
                "text": post["text"],
                "hashtags": ', '.join(post["hashtags"])
            })

    print(f"📁 저장 완료: {output_filename} (총 {len(filtered_posts)}개 게시물)")
