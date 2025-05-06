import undetected_chromedriver as uc
import time
import pickle


# --------- 브라우저 옵션 ---------
# options = uc.ChromeOptions()
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("window-size=1280,800")
# options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36")
#
# driver = uc.Chrome(options=options, headless=False)
#
# # --------- 로그인 페이지 열기 ---------
# driver.get("https://discord.com/login")
# print("🔐 Discord에 로그인하고 텍스트 채널로 이동하세요.")
# print("⏳ 최대 60초 동안 서버 채널 진입 대기 중...")
#
# # --------- 채널 감지 대기 ---------
# valid_channel_url = None
# for i in range(60):
#     current_url = driver.current_url
#     if "/channels/" in current_url and "@me" not in current_url:
#         parts = current_url.strip("/").split("/")
#         if len(parts) >= 4 and parts[-2].isdigit() and parts[-1].isdigit():
#             valid_channel_url = current_url
#             print(f"✅ 서버 채널 페이지 감지됨: {current_url}")
#             break
#     print(f"⏳ 현재 위치: {current_url}")
#     time.sleep(1)
#
# # --------- 감지 실패 시 종료 ---------
# if not valid_channel_url:
#     print("❌ 제한 시간 내에 유효한 서버 채널 페이지로 이동하지 못했습니다.")
#     driver.quit()
#     exit()
#
# # --------- 쿠키 저장 ---------
# try:
#     with open("discord_cookies.pkl", "wb") as f:
#         pickle.dump(driver.get_cookies(), f)
#     print("✅ 쿠키 저장 완료")
# except Exception as e:
#     print(f"❌ 쿠키 저장 실패: {e}")
#
# # --------- localStorage 저장 ---------
# # --------- localStorage 저장 (토큰이 채워질 때까지 대기) ---------
# for i in range(20):
#     local_storage = driver.execute_script("return JSON.stringify(window.localStorage);")
#     if local_storage and "token" in local_storage:
#         with open("discord_local_storage.json", "w") as f:
#             f.write(local_storage)
#         print("✅ localStorage 저장 완료")
#         break
#     print("⏳ localStorage 채워질 때까지 대기 중...")
#     time.sleep(1)
# else:
#     print("⚠️ 20초 동안 localStorage에 token이 감지되지 않아 저장하지 않았습니다.")
#
# driver.quit()


#-----


# 대상 채널 URL
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import random
import csv
import os

CHANNEL_URL = "https://discord.com/channels/234492134806257665/476966840883478528"
OUTPUT_CSV = "output.csv"
EMAIL = "kim1016jh@naver.com"
PASSWORD = "kim5151782jh!"

options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("window-size=1280,800")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36")

unique_messages = set()
results = []

# 이전에 저장된 메시지 불러오기
def load_existing_messages():
    existing = set()
    if os.path.exists(f"results/{OUTPUT_CSV}"):
        with open(f"results/{OUTPUT_CSV}", newline='', encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if len(row) >= 3:
                    existing.add(f"{row[1]}|{row[2]}")
    return existing

try:
    unique_messages = load_existing_messages()
    driver = uc.Chrome(options=options, headless=False)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.get("https://discord.com/login")
    time.sleep(random.uniform(1.5, 3))

    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    time.sleep(random.uniform(1.5, 3))
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    time.sleep(random.uniform(1.5, 3))
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(random.uniform(3, 5))

    # 서버 클릭
    server_button = driver.find_element(By.CSS_SELECTOR, 'div[data-list-item-id="guildsnav___234492134806257665"]')
    driver.execute_script("arguments[0].scrollIntoView(true);", server_button)
    time.sleep(random.uniform(1.5, 3))
    server_button.click()

    # 채널 클릭
    channel_name = "초급_한국어_대화방"
    channel_element = driver.find_element(By.XPATH, f'//div[@class="name__2ea32 overflow__82b15" and text()="{channel_name}"]')
    driver.execute_script("arguments[0].scrollIntoView(true);", channel_element)
    time.sleep(random.uniform(1.5, 3))
    channel_element.click()
    time.sleep(random.uniform(1.5, 3))

    scroll_container = driver.find_element(By.CSS_SELECTOR, 'div.scroller__36d07.scrollerBase_d125d2.managedReactiveScroller_d125d2')

    previous_ids = set()
    no_change_count = 0
    max_no_change = 20

    while True:
        time.sleep(random.uniform(1.5, 2.5))
        messages = driver.find_elements(By.CSS_SELECTOR, 'li[id^="chat-messages"]')
        current_ids = {msg.get_attribute("id") for msg in messages if msg.get_attribute("id")}

        new_ids = current_ids - previous_ids
        if not new_ids:
            print("⏩ 새 메시지 없음. 다음 스크롤")
            no_change_count += 1
            if no_change_count >= max_no_change:
                break
        else:
            print(f"🔁 새 메시지 {len(new_ids)}개 렌더링됨. 크롤링 시작")
            no_change_count = 0
            for msg in messages:
                try:
                    msg_id = msg.get_attribute("id")
                    if msg_id not in previous_ids:
                        timestamp = msg.find_element(By.CSS_SELECTOR, 'time').get_attribute("datetime").strip()
                        username = msg.find_element(By.CSS_SELECTOR, 'span[class^="username_"]').text.strip()
                        content = msg.find_element(By.CSS_SELECTOR, 'div[class^="markup_"]').text.strip()
                        key = f"{username}|{content}"
                        if key not in unique_messages:
                            unique_messages.add(key)
                            results.append([timestamp, username, content])
                            print(f"📥 {username} - {content[:30]}")
                except Exception:
                    continue
            previous_ids |= new_ids

        scroll_distance = random.uniform(0.6, 0.95)
        try:
            driver.execute_script("arguments[0].scrollTop -= arguments[0].clientHeight * arguments[1]", scroll_container, scroll_distance)
        except Exception:
            print("⚠️ 스크롤 중 예외 발생. 종료.")
            break

except Exception as e:
    print(f"❌ 오류 발생: {e}")

finally:
    try:
        driver.quit()
    except:
        pass

    if results:
        os.makedirs("results", exist_ok=True)
        with open(f"results/{OUTPUT_CSV}", mode="a", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            if os.path.getsize(f"results/{OUTPUT_CSV}") == 0:
                writer.writerow(["Timestamp", "Username", "Content"])
            writer.writerows(results)
        print(f"✅ 저장 완료: results/{OUTPUT_CSV} ({len(results)}건)")
    else:
        print("⚠️ 수집된 메시지가 없습니다.")



# ----------------------------------------------------------------------------------------------------------------------
