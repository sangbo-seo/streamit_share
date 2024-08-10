import streamlit as st

import socket
import requests
import re
import random
import time
#import pyperclip
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from datetime import datetime

def scrape_website(url):
    # Webdriver 설정
    # Chrome WebDriver 경로 설정
    customService = Service()  # ChromeDriver의 경로로 변경하세요
    customOptions = Options()
  #chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않고 실행
    customOptions.add_argument("--window-size=600,800")  # 브라우저 창을 띄우지 않고 실행
  # 브라우저 열기
 
    driver = webdriver.Chrome(service=customService, options=customOptions)  
    driver.implicitly_wait(30)
    #site_url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https://m.naver.com/'
    
    # 웹 페이지 접근
    driver.get(url)
    
    # 여기에 스크래핑 로직 추가
    title = driver.title
    time.sleep(20)
    driver.quit()
    return title

# Streamlit 앱
st.title('Visit your place')

url = st.text_input('Enter a URL to visit:')
if st.button('Visit!'):
    if url:
        result = scrape_website(url)
        st.write(f"Title of the page: {result}")
    else:
        st.write("Please enter a URL")


        