from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def fetch_kbo_shorts():
    options = Options()

    # ✅ 서버 환경에서 필요한 옵션들 (Render, Railway 등)
    options.add_argument('--headless')  # GUI 없는 환경 필수
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1')

    # ✅ 크롬 드라이버 실행
    driver = webdriver.Chrome(options=options)

    # ✅ 네이버 KBO 모바일 페이지 접속
    url = "https://m.sports.naver.com/kbaseball/index"
    driver.get(url)
    time.sleep(3)

    shorts = []

    # ✅ 숏츠 카드 수집
    cards = driver.find_elements(By.CSS_SELECTOR, 'a[data-event-area^="keyword"]')
    for card in cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "span.sds-comps-text-ellipsis-1").text.strip()
        except:
            title = ""

        try:
            summary = card.find_element(By.CSS_SELECTOR, "span.sds-comps-ellipsis-content").text.strip()
            if summary.strip() == title.strip() or summary.startswith(title.strip()):
                summary = ""
        except:
            summary = ""

        try:
            link = card.get_attribute("href")
        except:
            link = ""

        try:
            image = card.find_element(By.TAG_NAME, "img").get_attribute("src")
        except:
            image = ""

        try:
            time_str = card.find_element(By.CSS_SELECTOR, "span.fds-shortents-compact-date").text.strip()
        except:
            time_str = ""

        shorts.append({
            "title": title,
            "summary": summary,
            "link": link,
            "image": image,
            "time": time_str
        })

    driver.quit()
    return shorts

# 🔧 단독 실행 테스트용 (배포 시 제거해도 됨)
if __name__ == "__main__":
    result = fetch_kbo_shorts()
    if not result:
        print("❌ 숏콘텐츠가 없습니다.")
    else:
        for i, item in enumerate(result, 1):
            print(f"{i}. 🎬 제목: {item['title']}\n   🔗 링크: {item['link']}\n   🖼️ 이미지: {item['image']}\n   📝 요약: {item['summary']}\n   🕒 시간: {item['time']}")
            print("-" * 60)
