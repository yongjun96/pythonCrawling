import os
import random
import tempfile
import time
import csv
import subprocess

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


options = Options()
# options.add_argument("user-data-dir=C:\\Users\\practice960426@gmail.com\\AppData\\Local\\Google\\Chrome\\User Data")  # 맥용
# options.add_argument('--user-data-dir=C:\\crawling')  # 윈도우용
# options.add_argument("--headless=new")  # 필요 시 헤드리스 모드

temp_profile = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={temp_profile}")

options.add_argument("--disable-blink-features=AutomationControlled")  # 셀레니움 탐지 회피
options.add_argument("--user-data-dir=/path/to/fresh/profile")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)
# driver.get("https://twitter.com")
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
#     password_input.send_keys("비밀번호 입력해.")  # 비밀번호 입력
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

# ----------------------------------------- 여기 부터 본문 크롤링

# 오토 핫키로 vpn 체인지
def change_protonvpn_server():
    ahk_script = r"C:/Users/pract/IdeaProjects/pythonCrawling/crawling/protonvpn_change_server.ahk"  # .ahk 경로
    ahk_exe = r"C:/Program Files/AutoHotkey/v2/AutoHotkey.exe"  # AHK 설치 경로

    try:
        subprocess.Popen([ahk_exe, ahk_script])
        print("🔁 ProtonVPN 서버 변경 시도 중...")
        time.sleep(10)  # VPN 변경/연결 기다리기
    except Exception as e:
        print(f"❌ VPN 변경 실패: {e}")

# ✅ 새 게시물 로딩 여부 확인 함수
def wait_for_new_articles(previous_count, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        current_articles = driver.find_elements(By.XPATH, '//article[@role="article"]')
        if len(current_articles) > previous_count:
            return True
        time.sleep(0.5)
    return False

# ✅ 로그 기록 함수
def log(message, level="INFO"):
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [{level}] {message}"
    print(formatted)
    with open("crawl_log.txt", "a", encoding="utf-8-sig") as f:
        f.write(formatted + "\n")

# ✅ 기존 CSV에서 저장된 key(username + text) 불러오기
def load_existing_keys(csv_path):
    existing_keys = set()
    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = f"{row['username']}_{row['text']}"
                existing_keys.add(key)
    return existing_keys

# ✅ 검색어 리스트
search_keywords = ["learn_korean"]

for keyword in search_keywords:
    log(f"🔍 '{keyword}' 검색 시작")
    output_filename = f"hashtag_{keyword.replace(' ', '_')}_post.csv"
    existing_keys = load_existing_keys(output_filename)
    seen_keys = set(existing_keys)

    try:
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='SearchBox_Search_Input']"))
        )
        search_input.clear()
        time.sleep(random.uniform(1, 2.5))
        search_input.send_keys(keyword)
        time.sleep(random.uniform(1, 2.5))
        search_input.send_keys(Keys.ENTER)
        time.sleep(random.uniform(1, 2.5))
        log("   └ 검색어 입력 완료")
    except Exception as e:
        log(f"   ❌ 검색창 오류: {e}", level="ERROR")
        continue

    scroll_step = 500
    max_attempts = 200
    scroll_retry_limit = 13

    attempt = 0
    same_batch_count = 0
    scroll_retries = 0
    no_post_growth_count = 0
    collected_posts = []
    previous_batch = []
    same_authors_repeat_count = 0
    last_author_set = None

    try:
        while attempt < max_attempts:
            attempt += 1
            new_posts = []
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

                    post = {
                        "username": username,
                        "text": tweet_text,
                        "hashtags": hashtags,
                        "time": article.find_element(By.XPATH, ".//time").get_attribute("datetime") if article.find_elements(By.XPATH, ".//time") else "작성일 없음"
                    }

                    key = f"{username}_{tweet_text}"
                    if key not in seen_keys:
                        seen_keys.add(key)
                        collected_posts.append(post)
                        new_posts.append(post)
                        new_authors.append(username)

                except Exception as e:
                    log(f"트윗 파싱 중 예외 발생: {e}", level="WARNING")
                    continue

            log(
                f"   ↺ 스크롤 {attempt}회차 - 새 게시물 {len(new_posts)}개 (총 {len(collected_posts)}개)\n"
                f"      └ 작성자: {', '.join(new_authors) if new_authors else '없음'}"
            )

            current_author_set = tuple(sorted(new_authors))
            if current_author_set == last_author_set:
                same_authors_repeat_count += 1
            else:
                same_authors_repeat_count = 1
            last_author_set = current_author_set
            force_scroll = same_authors_repeat_count >= 2

            if len(collected_posts) == len(previous_batch):
                same_batch_count += 1
            else:
                same_batch_count = 0
                scroll_retries = 0
                no_post_growth_count = 0

            previous_batch = list(collected_posts)

            if scroll_retries >= 5:
                log("⚠ ProtonVPN 서버 변경 시도 중 (스크롤 재시도 5회 초과)", level="WARNING")
                change_protonvpn_server()
                time.sleep(10)

            if same_batch_count >= 1 or force_scroll:
                scroll_retries += 1
                reason = "동일 작성자 구성 2회 반복 감지" if force_scroll else "새 게시물 없음"
                log(f"   ⬆ 스크롤 재시도 중... ({scroll_retries}/{scroll_retry_limit}) - 이유: {reason}")

                before_scroll_count = len(driver.find_elements(By.XPATH, '//article[@role="article"]'))

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(1.2, 2.5))

                loaded_time = random.randint(4, 6)
                loaded = wait_for_new_articles(before_scroll_count, timeout=loaded_time)

                if not loaded:
                    amount = random.randint(5000, 10000)
                    driver.execute_script(f"window.scrollBy(0, -{amount});")
                    time.sleep(random.uniform(1.2, 2.5))
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(random.uniform(1.2, 2.5))

                    after_scroll_count = len(driver.find_elements(By.XPATH, '//article[@role="article"]'))
                    if after_scroll_count == before_scroll_count:
                        no_post_growth_count += 1
                    else:
                        no_post_growth_count = 0

                    if no_post_growth_count >= 13:
                        log("   ⛔ 게시물 증가 없음 13회 반복 → 종료", level="WARNING")
                        break

                continue

            driver.execute_script(f"window.scrollBy(0, {scroll_step});")
            time.sleep(random.uniform(1, 2.5))

    except Exception as e:
        log(f"스크롤 루프 중 예외 발생: {e}", level="ERROR")

    finally:
        if not collected_posts:
            log("📭 저장할 게시물이 없습니다.", level="WARNING")
            continue

        try:
            with open(output_filename, mode='a', newline='', encoding='utf-8-sig') as file:
                writer = csv.DictWriter(file, fieldnames=["username", "time", "text", "hashtags"])
                if not os.path.getsize(output_filename):
                    writer.writeheader()
                for post in collected_posts:
                    writer.writerow({
                        "username": post["username"],
                        "time": post["time"],
                        "text": post["text"],
                        "hashtags": ', '.join(post["hashtags"])
                    })

            log(f"📁 저장 완료: {output_filename} (이번에 저장된 {len(collected_posts)}개 게시물)")
        except Exception as e:
            log(f"CSV 저장 중 오류 발생: {e}", level="ERROR")



