import streamlit as st
from urllib.parse import quote, unquote
import random
import time
from PIL import Image
import requests
import urllib.request
import json
from datetime import datetime
import importlib.util
import os
from konlpy.tag import Komoran
import pandas as pd
from collections import Counter
import re

def load_module(module_name):
    module_path = os.path.join('new_files', f'{module_name}.py')
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def random_delay(min_delay=30, max_delay=150):
    """랜덤한 시간 동안 지연시키는 함수"""
    delay = random.uniform(min_delay, max_delay)
    print(f"Sleeping for {delay:.2f} seconds")
    time.sleep(delay)

def getResult(client_id, client_secret, keyword_list):    
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    keyword = keyword_list
    encText = urllib.parse.quote(keyword) 
    
    shop_url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&display=100&start=1" #100순위
    
    request = urllib.request.Request(shop_url) 
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode == 200):
        response_body = response.read()
        json_str = response_body.decode('utf-8')
    else:
        st.error(f"Error Code: {rescode}")
        return []
    
    json_object = json.loads(json_str) #json 변환
    
    # 결과 리스트
    results = []
    for i in range(0, min(10, len(json_object['items']))):  # 상위 5개의 결과만 표시
        title = json_object['items'][i]['title'].replace('<b>', "").replace('</b>', "")
        mallName = json_object['items'][i]['link']
        bloggerID = json_object['items'][i]['bloggerlink'].replace('blog.naver.com/', "")
        results.append({
            "Title": title,
            "Blogger ID": bloggerID,
            "Link": mallName
        })
    
    return results




st.title('플레이스 랭킹 앱')

# place_ranking.py 모듈 로드
place_ranking = load_module('place_ranking')

# place_ranking.py의 main 함수 실행 (만약 존재한다면)
if hasattr(place_ranking, 'main'):
    place_ranking.main()
else:
    st.error("place_ranking.py에 main 함수가 없습니다.")

# 또는 place_ranking.py의 특정 함수들을 직접 호출할 수 있습니다
# 예를 들어:
# if hasattr(place_ranking, 'show_rankings'):
#     place_ranking.show_rankings()



def count_characters(text):
    """텍스트의 글자수를 계산하는 함수"""
    # 전체 글자수
    total_chars = len(text)
    chars_without_spaces = len(text.replace(' ', ''))
    
    # 한글만 추출하여 계산
    korean_text = re.findall('[가-힣]', text)
    korean_chars = len(korean_text)
    
    # 공백을 포함한 한글 텍스트 추출
    korean_text_with_spaces = re.sub('[^가-힣\s]', '', text)
    korean_chars_with_spaces = len(korean_text_with_spaces)
    korean_chars_without_spaces = len(korean_text_with_spaces.replace(' ', ''))
    
    # 단어 수와 줄 수
    words = len(text.split())
    lines = len(text.splitlines())
    
    return {
        'total_chars': total_chars,                          # 전체 글자수 (공백 포함)
        'chars_without_spaces': chars_without_spaces,        # 전체 글자수 (공백 제외)
        'korean_chars_with_spaces': korean_chars_with_spaces,    # 한글 글자수 (공백 포함)
        'korean_chars_without_spaces': korean_chars_without_spaces,  # 한글 글자수 (공백 제외)
        'korean_chars': korean_chars,                        # 순수 한글 글자수
        'words': words,                                      # 단어 수
        'lines': lines                                       # 줄 수
    }

def analyze_text(text, analyzer):
    """텍스트 분석을 수행하는 함수"""
    try:
        # 글자수 분석
        char_counts = count_characters(text)
        
        # 형태소 분석
        pos_results = analyzer.pos(text)
        morphs = analyzer.morphs(text)
        nouns = analyzer.nouns(text)
        
        # 빈도 분석
        noun_count = Counter(nouns)
        freq_df = pd.DataFrame(noun_count.most_common(), columns=['단어', '빈도'])
        freq_df.index = range(1, len(freq_df) + 1)
        
        # 품사 태깅 결과를 DataFrame으로 변환
        pos_df = pd.DataFrame(pos_results, columns=['단어', '품사'])
        pos_df.index = range(1, len(pos_df) + 1)
        
        return {
            'freq_df': freq_df,
            'pos_df': pos_df,
            'morphs': morphs,
            'nouns': nouns,
            'char_counts': char_counts
        }
    except Exception as e:
        st.error(f"분석 중 오류가 발생했습니다: {str(e)}")
        return None


# 페이지 설정
st.set_page_config(
    page_title="한글 형태소 분석기",
    page_icon="🇰🇷",
    layout="wide"
)

# 제목
st.title("한글 형태소 분석기 🇰🇷")

try:
    # Komoran 초기화
    analyzer = Komoran()
    
    # 사이드바 설정
    st.sidebar.title("설정")
    st.sidebar.markdown("""
    ### 사용 방법
    1. 분석할 텍스트를 입력하세요
    2. 분석 결과는 자동으로 업데이트됩니다
    
    ### 형태소 분석기 정보
    - 사용 분석기: Komoran
    - 개발: Shineware
    """)
    
    # 메인 영역
    text_input = st.text_area(
        "분석할 텍스트를 입력하세요:",
        height=200,
        placeholder="여기에 텍스트를 입력하세요..."
    )
    
    if text_input:
        # 분석 수행
        results = analyze_text(text_input, analyzer)
        
        if results:
            # 글자수 통계 표시
            st.markdown("### 📊 텍스트 통계")
            
            # 전체 글자수
            st.markdown("#### 전체 글자수")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("전체 글자수 (공백 포함)", 
                            results['char_counts']['total_chars'])
            with col2:
                st.metric("전체 글자수 (공백 제외)", 
                            results['char_counts']['chars_without_spaces'])
            
            # 한글 글자수
            st.markdown("#### 한글 글자수")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("한글 글자수 (공백 포함)", 
                            results['char_counts']['korean_chars_with_spaces'])
            with col2:
                st.metric("한글 글자수 (공백 제외)", 
                            results['char_counts']['korean_chars_without_spaces'])
            
            # 기타 통계
            st.markdown("#### 기타 통계")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("순수 한글 문자 수", 
                            results['char_counts']['korean_chars'])
            with col2:
                st.metric("단어 수", 
                            results['char_counts']['words'])
            with col3:
                st.metric("줄 수", 
                            results['char_counts']['lines'])
            
            st.markdown("---")
            
            # 탭 생성
            tab1, tab2, tab3, tab4 = st.tabs([
                "빈도 분석", "품사 태깅", "형태소", "명사"
            ])
            
            # 탭1: 빈도 분석
            with tab1:
                st.subheader("단어 빈도 분석")
                
                # 데이터프레임 스타일링
                st.markdown("""
                <style>
                .dataframe {
                    font-size: 1.1rem;
                    font-family: sans-serif;
                }
                .dataframe th {
                    background-color: #f0f2f6;
                    padding: 10px;
                }
                .dataframe td {
                    padding: 8px;
                }
                </style>
                """, unsafe_allow_html=True)
                
                st.dataframe(
                    results['freq_df'],
                    use_container_width=True,
                    hide_index=False
                )
                
                if len(results['freq_df']) > 0:
                    st.subheader("상위 10개 단어 빈도 차트")
                    top_10 = results['freq_df'].head(10)
                    st.bar_chart(
                        data=top_10.set_index('단어')['빈도'],
                        use_container_width=True
                    )
            
            # 탭2: 품사 태깅
            with tab2:
                st.subheader("품사 태깅 결과")
                st.dataframe(
                    results['pos_df'],
                    use_container_width=True,
                    hide_index=False
                )
            
            # 탭3: 형태소
            with tab3:
                st.subheader("형태소 분석 결과")
                morphs_text = ', '.join(results['morphs'])
                st.text_area(
                    "형태소 목록:",
                    value=morphs_text,
                    height=200,
                    disabled=True
                )
            
            # 탭4: 명사
            with tab4:
                st.subheader("명사 추출 결과")
                nouns_text = ', '.join(results['nouns'])
                st.text_area(
                    "명사 목록:",
                    value=nouns_text,
                    height=200,
                    disabled=True
                )
            
            # 형태소 분석 통계
            st.markdown("### 📊 형태소 분석 통계")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("총 형태소 수", len(results['morphs']))
            with col2:
                st.metric("고유 명사 수", len(set(results['nouns'])))
            with col3:
                st.metric("총 단어 수", len(results['pos_df']))
            
except Exception as e:
    st.error(f"프로그램 초기화 중 오류가 발생했습니다: {str(e)}")



#--------------------------
# 제목 설정
st.title("한글 글자수 세기")

# 사용자로부터 텍스트 입력받기
user_input = st.text_area("텍스트를 입력하세요:")

# 공백 포함 글자 수
total_char_count = len(user_input)

# 공백 제외 글자 수
char_count_no_spaces = len(user_input.replace(" ", ""))

# 한글과 영어 구분
korean_text = ''.join([char for char in user_input if '가' <= char <= '힣'])
english_text = ''.join([char for char in user_input if 'a' <= char.lower() <= 'z'])


if st.button('글자수 계산'):
    # 결과 출력
    st.write(f"입력한 텍스트의 총 글자 수 (공백 포함): {total_char_count}자")
    st.write(f"입력한 텍스트의 글자 수 (공백 제외): {char_count_no_spaces}자")
    #st.write(f"한글 글자 수: {len(korean_text)}자")
    #st.write(f"영어 글자 수: {len(english_text)}자")



# Streamlit 앱 제목
st.title("형태소 분석기 가기")

# 사용자로부터 URL 입력받기
url = 'https://whereispost.com/morpheme/#google_vignette'

# 버튼 클릭 시 JavaScript로 새 창 열기
if st.button('새 창으로 열기'):
    js_code = f"""
    <script type="text/javascript">
        window.open("{url}");
    </script>
    """
    st.components.v1.html(js_code)



# Streamlit UI
st.title('네이버 블로그 순위 조회')

client_id = st.text_input('Client ID')
client_secret = st.text_input('Client Secret', type="password")
keyword = st.text_input('키워드를 입력하세요')

if st.button('검색'):
    if client_id and client_secret and keyword:
        results = getResult(client_id, client_secret, keyword)
        if results:
            for i, result in enumerate(results):
                st.write(f"**{i+1}. {result['Title']}**")
                st.write(f"  - Blogger ID: {result['Blogger ID']}")
                st.write(f"  - [Link]({result['Link']})")
        else:
            st.write("검색 결과가 없습니다.")
    else:
        st.error("Client ID, Client Secret, 그리고 키워드를 모두 입력하세요.")





# Streamlit 앱 제목
st.title("URL 인코딩 및 디코딩 도구")

# 사용자에게 입력 받을 URL 텍스트
input_url = st.text_input("변환할 URL을 입력하세요:")

# 인코딩 및 디코딩 버튼
if st.button("인코딩"):
    encoded_url = quote(input_url)
    st.write("인코딩된 URL:~~", encoded_url)

if st.button("디코딩"):
    decoded_url = unquote(input_url)
    st.write("디코딩된 URL:~~", decoded_url)


# Streamlit 앱 제목
st.title("플레이스 순서대로 방문[철인29호]")


# 저장된 이미지 파일 경로
image_path = 'image.jpg'

# 이미지 열기
image = Image.open(image_path)

# 이미지 화면에 표시
st.image(image, caption='네이버 좋댓펌 프로그램/ 플레이스 방문 실행 프로그램 화면', use_column_width=True)


# 초기 상태 설정
if 'stop' not in st.session_state:
    st.session_state.stop = False

# 사용자로부터 URL 입력받기
urls =[
"https://m.search.naver.com/p/crd/rd?m=1&px=298&py=2144&sx=298&sy=544&vw=1074&vh=966&p=ir1s5lqptusssnRX4g8ssssstYV-195184&q=%EC%9A%A9%EC%9D%B8%ED%9A%8C%EC%9D%98%EC%8B%A4&ie=utf8&rev=1&ssc=tab.m.all&f=m&w=m&s=5z2PPdQfbZSXAXKZLOfytQ%3D%3D&time=1723678774854&abt=%5B%7B%22eid%22%3A%22SHP-SUPER-ITEM%22%2C%22vid%22%3A%228%22%7D%2C%7B%22eid%22%3A%22SURF%22%2C%22vid%22%3A%224%22%7D%5D&a=loc_plc.tit&r=5&i=1938513684&u=https%3A%2F%2Fm.place.naver.com%2Fplace%2F1938513684%3Fentry%3Dpll&cr=2",
"https://m.search.naver.com/p/crd/rd?m=1&px=311&py=1745&sx=311&sy=345&vw=1074&vh=966&p=ir1s9wqVWdossUWx5m4ssssst7o-386506&q=%EA%B8%B0%ED%9D%A5%EB%B9%84%EC%83%81%EC%A3%BC%EC%82%AC%EB%AC%B4%EC%8B%A4%ED%95%B4%EC%8B%9C%EC%8A%A4&ie=utf8&rev=1&ssc=tab.m.all&f=m&w=m&s=5z2PPdQfbZSXAXKZLOfytQ%3D%3D&time=1723678995050&abt=%5B%7B%22eid%22%3A%22SHP-SUPER-ITEM%22%2C%22vid%22%3A%228%22%7D%2C%7B%22eid%22%3A%22SURF%22%2C%22vid%22%3A%224%22%7D%5D&a=loc_plc.tit&r=2&i=1696946583&u=https%3A%2F%2Fm.place.naver.com%2Fplace%2F1696946583%3Fentry%3Dpll&cr=2",
"https://m.search.naver.com/p/crd/rd?m=1&px=328&py=3255&sx=328&sy=455&vw=1074&vh=966&p=ir0%2FPlqVOZwss6Xhef4ssssssdK-077166&q=%EA%B0%95%EB%82%A8%EC%97%AD%ED%9A%8C%EC%9D%98%EC%8B%A4&ie=utf8&rev=1&ssc=tab.m.all&f=m&w=m&s=5z2PPdQfbZSXAXKZLOfytQ%3D%3D&time=1723678612277&abt=%5B%7B%22eid%22%3A%22SHP-SUPER-ITEM%22%2C%22vid%22%3A%228%22%7D%2C%7B%22eid%22%3A%22SURF%22%2C%22vid%22%3A%224%22%7D%5D&a=loc_plc.tit&r=10&i=1017990853&u=https%3A%2F%2Fm.place.naver.com%2Fplace%2F1017990853%3Fentry%3Dpll&cr=2",
"https://m.blog.naver.com/haesys_yi/223315051131",
"https://m.search.naver.com/p/crd/rd?m=1&px=680&py=6022&sx=680&sy=689&vw=1552&vh=1173&p=iYn00dp0iqdsshP71MGssssst4R-089733&q=%EC%9A%A9%EC%9D%B8%EB%B9%84%EC%83%81%EC%A3%BC%EC%82%AC%EB%AC%B4%EC%8B%A4&ie=utf8&rev=1&ssc=tab.m.all&f=m&w=m&s=Ju9S8jtHRhO5V%2Fz1Rw2I6YKF&time=1727263991041&abt=%5B%7B%22eid%22%3A%22RQT-UNIFY%22%2C%22vid%22%3A%227%22%7D%2C%7B%22eid%22%3A%22SHP-SUPER-ITEM%22%2C%22vid%22%3A%2235%22%7D%2C%7B%22eid%22%3A%22SURF-LOAD-PERF%22%2C%22vid%22%3A%227%22%7D%5D&a=loc_plc.tit&r=11&i=1649986581&u=https%3A%2F%2Fm.place.naver.com%2Fplace%2F1649986581%3Fentry%3Dpll&cr=4",
"https://cr.shopping.naver.com/adcr.nhn?x=bZiy9H07z6lSHRpEL%2Ffgcf%2F%2F%2Fw%3D%3DsJLD8jFGQnzHfjIWw7UkrOo5LQQd5fkKnO2WCfDo7sOdumLm5vzI2zDqtSj3lBP3rNhKaeN7z9HXlnOYq%2FygM8rlx9VaJZQAxjksaEbkPULb3%2Fkrlp8fLgAIaJXGbRb64pOr9sPYwajBkeE07IGGkJ52IwS1IXJuFZi%2BE6bgMs5ocmwbCUp1LdYvZC%2F3qEieeczoSDmYN%2Fqku09VdurWOesH6FihHtPZzi%2BJJF7qz2iq84OS6LYm2VrPehWjlu%2Fp3jj9KGBW69ZED30eD2DXGkKdCOcQaTEgdcZvPlLMx3SD%2FiivQCwwk7ARNHUz1%2ByPTw6ZjbtkbN7RD61dGUzg7G1qsmhWtsS26cBgiQoajA6pUz2badeBumVr1vM5KpiTLV9GnYTqcCY37qspitt6iMuDINHrnAoqKd1VtFE3jtgNcDG6BAQWxk4PIsLQnrb7rwc%2BmmZpbv%2FflVGXFwTg%2BjXa3Hust%2BTVeCcfaom5vRSifQ%2FdoOYcZ0N3q%2FiaZU%2F10i3%2BfSaB1gMhxGrlTqPYgoLLIQd3SQFH4CS8gZx%2FP9H3xZteYvE%2BrhRyBU9cFQEyygVi4CAXt57UZEOWoUZ94961yR5inm9VzW2KfaH2rnYiF6Lf38TLIXT66v%2B6bXAt3jnzHqxqBxt9J58EdOC0hNcF4oDDdb5ooU3BFGOa3lL5b%2BA0QDcIEXCIWHqFtSKK9dafFLdP0OImy8jJP1QKCyZhsFBsc8hm2v5vAk%2FruXHHVAqc7z%2BslBKVgm2nxZ2CUV3OdHgSE8LoEjTx9zpNPbFaRsOtQUnaEEbxBoHxZXOc%3D&nvMid=88250970603&catId=50007254",
"https://m.search.naver.com/p/crd/rd?m=1&px=382&py=2617&sx=382&sy=417&vw=1074&vh=966&p=ir1sQwqVWudssMFeL4lssssssr4-302279&q=%EC%9A%A9%EC%9D%B8%EB%B9%84%EC%83%81%EC%A3%BC%EC%82%AC%EB%AC%B4%EC%8B%A4&ie=utf8&rev=1&ssc=tab.m.all&f=m&w=m&s=5z2PPdQfbZSXAXKZLOfytQ%3D%3D&time=1723678866171&abt=%5B%7B%22eid%22%3A%22SHP-SUPER-ITEM%22%2C%22vid%22%3A%228%22%7D%2C%7B%22eid%22%3A%22SURF%22%2C%22vid%22%3A%224%22%7D%5D&a=loc_plc.tit&r=3&i=1898294606&u=https%3A%2F%2Fm.place.naver.com%2Fplace%2F1898294606%3Fentry%3Dpll&cr=2",
"https://m.search.naver.com/p/crd/rd?m=1&px=353&py=3937&sx=353&sy=337&vw=1074&vh=966&p=ir0%2FPlqVOZwss6Xhef4ssssssdK-077166&q=%EA%B0%95%EB%82%A8%EC%97%AD%ED%9A%8C%EC%9D%98%EC%8B%A4&ie=utf8&rev=1&ssc=tab.m.all&f=m&w=m&s=5z2PPdQfbZSXAXKZLOfytQ%3D%3D&time=1723678702337&abt=%5B%7B%22eid%22%3A%22SHP-SUPER-ITEM%22%2C%22vid%22%3A%228%22%7D%2C%7B%22eid%22%3A%22SURF%22%2C%22vid%22%3A%224%22%7D%5D&a=loc_plc.tit&r=14&i=1106199648&u=https%3A%2F%2Fm.place.naver.com%2Fplace%2F1106199648%3Fentry%3Dpll&cr=2",
"https://m.search.naver.com/p/crd/rd?m=1&px=482&py=931&sx=482&sy=731&vw=1074&vh=966&p=ir1uLlp0i0GssgBHMlwssssssyl-091465&q=%ED%83%9C%ED%92%8D%EA%B2%BD%EB%A1%9C&ie=utf8&rev=1&ssc=tab.m_news.all&f=m_news&w=m_news&s=5z2PPdQfbZSXAXKZLOfytQ%3D%3D&time=1723679302756&abt=%5B%7B%22eid%22%3A%22SHP-SUPER-ITEM%22%2C%22vid%22%3A%228%22%7D%2C%7B%22eid%22%3A%22SURF%22%2C%22vid%22%3A%224%22%7D%5D&a=nws*j.title&r=5&i=88156f73_000000000000000000471759&g=&u=https%3A%2F%2Fn.news.naver.com%2Farticle%2F448%2F0000471759%3Fsid%3D102",
"https://m.search.naver.com/p/crd/rd?m=1&px=60&py=1641&sx=60&sy=641&vw=265&vh=1142&p=iVZCSwprcI0ssAC77%2BVssssstZN-063466&q=%EC%9D%B4%EB%8C%80%EA%B3%B5%EA%B0%84%EB%8C%80%EC%97%AC%EC%B2%A0%EB%B6%80%EC%A7%80&ie=utf8&rev=1&ssc=tab.m.all&f=m&w=m&s=CE%2Fb%2BBdv45LE7NHz0aY2Gg%3D%3D&time=1723933802272&abt=%5B%7B%22eid%22%3A%22SHP-SUPER-ITEM%22%2C%22vid%22%3A%228%22%7D%5D&a=loc_plc.tit&r=1&i=1328568186&u=https%3A%2F%2Fm.place.naver.com%2Fplace%2F1328568186%3Fentry%3Dpll&cr=2",
"https://cr.shopping.naver.com/adcr.nhn?x=Sxyo9tY8Sz556j4lVTmalv%2F%2F%2Fw%3D%3DsCd2csxrMISV%2BsXhVgD2Y2Oy806JihL3GnEmZXCJWa6X5tiKZUBQMxkkEWTXZlvF0J%2FfGWgxwbajNyGqblMF3U13pPykeAew47hBo3jfBxDBgMHnVM3zOE17Fy9SuoHExW4qWbL2vEyBbDC3wBdyv%2BLcZ37YrGmisNh7yxm9y8NQeMDmqDMbtkp7clROyzAFJVHcHPYYqn1w3KgNx5W5C5RoE4mTP587sKtn3srJAJm4Q30gwb0ZAWnfX3Zzr1ayR4uxanfK20CgJFMCKm453GTq1461dr8WFIbmNnTE6ozmAmJE%2B5eaTcbwcZxhrtnWXwc%2B%2FjkR2vl%2B%2B%2B%2F%2BVPNlrhdPwrPAvSux8OttNTn%2F%2FJ3M6MaNaJsB2ca0q11PK4%2BUpe53XaJOElESYjnSgRW0u0xUhwUNj8hcxgfTh7UKrKuA4DAOMd%2BFJ4hR32YD2NdWFULnLIyzs0rzJg9qQnlt2Gf6dV35cdwMDWeF9F8c%2Bdm34mMqBVdezTmommzqNglGZsshB3dJAUfgJLyBnH8%2F0ffFm15i8T6uFHIFT1wVATLKBWLgIBe3ntRkQ5ahRn3j3rXJHmKeb1XNbYp9ofaudiIXot%2FfxMshdPrq%2F7ptcC3eOfMerGoHG30nnwR04LSE1wgMV6fl5Dp7gjPmsfWUM9Vv4DRANwgRcIhYeoW1Ior11p8Ut0%2FQ4ibLyMk%2FVAoLJvUx104bnSp6IlX0B2gLIIm9dfcZLmf8bvGlrVcv0vCBXc50eBITwugSNPH3Ok09sVpGw61BSdoQRvEGgfFlc5w%3D%3D&nvMid=88259004754&catId=50007254",
]
     

# '정지' 버튼
if st.button('정지'):
    st.session_state.stop = True
    st.write("플레이스 방문이 중단되었습니다.")
    
    # 열려 있는 창 닫기
    js_code2 = """
    <script type="text/javascript">
        if (typeof(window.new_window) !== 'undefined' && !window.new_window.closed) {
            window.new_window.close();
        }
    </script>
    """
    st.components.v1.html(js_code2)

# '플레이스 방문 시작' 버튼
if st.button('플레이스 방문'):
    st.session_state.stop = False  # 중단 상태 초기화
    for i in range(0,10000):    
        for site_url in urls:
            if st.session_state.stop:
                st.write("플레이스 방문이 중단되었습니다.")
                break

            # 같은 창에 새로운 URL 열기
            js_code1 = f"""
            <script type="text/javascript">
                if (typeof(window.new_window) === 'undefined' || window.new_window.closed) {{
                    window.new_window = window.open("{site_url}", "_blank");
                }} else {{
                    window.new_window.close();
                    window.new_window.location.href = "{site_url}";
                }}
            </script>
            """
            st.components.v1.html(js_code1)
            random_delay()