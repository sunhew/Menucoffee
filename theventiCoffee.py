from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.chrome.options import Options as ChromeOptions
import json

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
folder_path = "theventi"
filename = f"{folder_path}/menutheventi_{current_date}.json"

# 웹드라이버 초기화 (Chrome 사용)
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)

# 방문할 URL 리스트
urls = [
    "https://www.theventi.co.kr/new2022/menu/all.html?mode=1",
    "https://www.theventi.co.kr/new2022/menu/all.html?mode=2",
    "https://www.theventi.co.kr/new2022/menu/all.html?mode=3",
    "https://www.theventi.co.kr/new2022/menu/all.html?mode=4",
    "https://www.theventi.co.kr/new2022/menu/all.html?mode=5",
    "https://www.theventi.co.kr/new2022/menu/all.html?mode=6",
]

# 데이터 추출을 위한 빈 리스트 생성
theventi_data = []

for url in urls:
    # 페이지 로드
    browser.get(url)
    
    # 페이지의 끝까지 스크롤 내리기
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # 잠시 대기 (로딩 완료를 위해)
    browser.implicitly_wait(5)

    # 업데이트된 페이지 소스를 변수에 저장
    html_source_updated = browser.page_source
    soup = BeautifulSoup(html_source_updated, 'html.parser')

    # 데이터 추출 (올바른 선택자로 수정 필요)
    tracks = soup.select("#contents > div > div > div.menu_list > ul > li")
    for track in tracks:
        name = track.select_one("#contents > div > div > div.menu_list > ul > li > a > div.txt_bx > p.tit").text.strip()  # 올바른 선택자로 수정
        image_url = track.select_one("#contents > div > div > div.menu_list > ul > li > a > div.img_bx > img").get('src').replace('/uploads', 'http://www.theventi.co.kr/uploads')  # 올바른 선택자로 수정

        theventi_data.append({
            "p.tit": name,  # 키 이름을 의미있게 수정
            "img": image_url  # 키 이름을 의미있게 수정
        })

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(theventi_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()
