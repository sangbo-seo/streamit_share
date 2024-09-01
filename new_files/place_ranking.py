import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

@st.cache_resource
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_place_info(html):
    soup = BeautifulSoup(html, "html.parser")
    all_items = soup.select('div.sc-q8es3i')
    
    non_ad_places = []
    for item in all_items:
        img = item.select_one('img.icon')
        if img and 'ad-marker' not in img['src']:
            title = item.select_one('strong.marker_title')
            place_id = item.get('id', '').split('-')[-1]
            if title and place_id:
                non_ad_places.append((title.text.strip(), place_id))
    
    return non_ad_places

# Streamlit 앱 시작
st.title('네이버 지도 플레이스 정보')

# URL 입력 필드
url = st.text_input('네이버 지도 URL을 입력하세요:')

if url:
    try:
        driver = get_driver()
        driver.get(url)
        
        # 페이지 로딩을 위한 대기 시간
        time.sleep(5)
        
        # HTML 가져오기
        html = driver.page_source
        
        # 플레이스 정보 추출
        places = get_place_info(html)
        
        # 결과 표시
        if places:
            st.subheader('플레이스 정보:')
            for index, (title, place_id) in enumerate(places, start=1):
                st.write(f"{index}. {title} (ID: {place_id})")
        else:
            st.warning('추출된 플레이스 정보가 없습니다.')
        
        driver.quit()
    except Exception as e:
        st.error(f'오류가 발생했습니다: {str(e)}')
else:
    st.info('네이버 지도 URL을 입력하면 플레이스 정보를 표시합니다.')

# 주의사항 추가
st.markdown('---')
st.write('주의: 이 앱은 교육 목적으로 만들어졌으며, 네이버의 이용 약관을 준수해야 합니다.')