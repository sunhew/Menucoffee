from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json
import os

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
folder_path = "coffeebanhada"
filename = f"{folder_path}/menucoffeebanhada_{current_date}.json"

# 폴더 생성
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 웹드라이버 초기화 (Chrome 사용)
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 로드해야 하는 페이지
url = 'https://coffeebanhada.com/main/menu/list4.php?page_type=1'
browser.get(url)

# '더보기' 버튼이 나타날 때까지 기다림 (최대 20초)
while True:
    try:
        more_button = WebDriverWait(browser, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".line_btn"))
        )
        if more_button:
            more_button.click()  # '더보기' 버튼 클릭
            print("Clicked '더보기' button.")
            time.sleep(2)  # 페이지 로딩 대기
    except Exception as e:
        print("더보기 버튼을 찾을 수 없음:", e)
        break

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# 데이터 추출
coffeebanhada_data = []
items = soup.select("div.menu_introduce_wrap ul.menu_introduce li a")

print(f"Found {len(items)} items.")  # 디버깅용 출력

# 각 항목에서 데이터 추출
for item in items:
    try:
        name = item.select_one("p.title").text.strip()
        image_url = item.select_one("img").get('src').replace('/data', 'https://coffeebanhada.com/data')
        
        coffeebanhada_data.append({
            "title": name,
            "imageURL": image_url
        })
    except Exception as e:
        print(f"Error extracting data from item: {e}")

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(coffeebanhada_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()

print(f"Data successfully saved to {filename}")
