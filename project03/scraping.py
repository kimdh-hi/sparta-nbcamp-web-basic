from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests

client = MongoClient('localhost',27017)
db = client.dbsparta_plus_week3

driver = webdriver.Chrome('./chromedriver')

# SBS TV 맛집
url = "http://matstar.sbs.co.kr/location.html"

driver.get(url) # 해당 url페이지 로드
time.sleep(5) # 충분한 로딩시간을 위해 5초 대기

# 더보기 버튼 최대 10번까지 클릭
for i in range(10):
    try:
        btn_more = driver.find_element_by_css_selector("#foodstar-front-location-curation-more-self > div > button")
        btn_more.click()
        time.sleep(5)
    except NoSuchElementException:
        break

req = driver.page_source # 대기 후 완전히 로드된 페이지를 가져옴
driver.quit()

soup = BeautifulSoup(req, 'html.parser') # 가져온 페이지를 bs4로 파싱

# 맛집 카드 파싱
places = soup.select("ul.restaurant_list > div > div > li > div > a")

# 카드 내 상호명, 주소, 카테고리 .. 파싱
for place in places:
    title = place.select_one("strong.box_module_title").text
    address = place.select_one("div.box_module_cont > div > div > div.mil_inner_spot > span.il_text").text
    category = place.select_one("div.box_module_cont > div > div > div.mil_inner_kind > span.il_text").text
    show, episode = place.select_one("div.box_module_cont > div > div > div.mil_inner_tv > span.il_text").text.rsplit(" ", 1)

    # geocode api 호출을 위한 key를 포함하는 헤더 구성
    headers = {
        "X-NCP-APIGW-API-KEY-ID": "m6of6dku4g",
        "X-NCP-APIGW-API-KEY": "HZLvUDOzmUJ4PeZ4WTe8YtlREQuVYmFdWd3gYRgt"
    }

    # geocode api 호출 (주소를 기반으로 위도, 경도를 반환)
    r = requests.get(f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}", headers=headers)
    response = r.json()

    if response["status"] == "OK":
        if len(response["addresses"]) > 0:
            x = float(response["addresses"][0]["x"])
            y = float(response["addresses"][0]["y"])

            doc = {
                "title": title,
                "address": address,
                "category": category,
                "show": show,
                "episode": episode,
                "mapx": x,
                "mapy": y,
                "like":'0'
            }

            db.matjips.insert_one(doc)
        else:
            print(title, "좌표를 찾지 못했습니다")



