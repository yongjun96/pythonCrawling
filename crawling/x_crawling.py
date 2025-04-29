import re

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


import time

options = Options()
options.add_argument("user-data-dir=C:\\Users\\practice960426@gmail.com\\AppData\\Local\\Google\\Chrome\\User Data")  # 윈도우용
# options.add_argument("--headless")  # 필요 시 헤드리스 모드

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
    search_input.send_keys("koreanlanguage")
    search_input.send_keys(Keys.ENTER)  # 엔터키 입력
    print("검색어 입력 완료")
except Exception as e:
    print("오류 발생:", e)

time.sleep(2)

tweets = driver.find_elements(By.XPATH, '//article[@role="article"]')

time.sleep(2)

for tweet in tweets:
    try:
        # 본문 텍스트
        text_element = tweet.find_element(By.XPATH, './/div[@lang]')
        text = text_element.text

        # 사용자 아이디
        user_element = tweet.find_element(By.XPATH, './/a[contains(@href, "/status")]/../../preceding-sibling::div//a[contains(@href, "/")]')
        user_id = user_element.text  # e.g. "@mirinae_io"

        # 날짜 (ISO 8601 format)
        time_element = tweet.find_element(By.XPATH, './/time')
        timestamp = time_element.get_attribute("datetime")  # e.g. "2024-08-09T02:29:35.000Z"

        # 해시태그 추출 (본문에서 정규표현식)
        hashtags = re.findall(r"#\w+", text)

        print("=== 트윗 ===")
        print("작성자:", user_id)
        print("날짜:", timestamp)
        print("본문:", text)
        print("해시태그:", hashtags)

    except Exception as e:
        print("오류 발생:", e)

time.sleep(2)



