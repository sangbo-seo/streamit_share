import streamlit as st
from urllib.parse import quote, unquote
import random
import time
from PIL import Image
import requests
import urllib.request
import json
from datetime import datetime



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
    for i in range(0, min(5, len(json_object['items']))):  # 상위 5개의 결과만 표시
        title = json_object['items'][i]['title'].replace('<b>', "").replace('</b>', "")
        mallName = json_object['items'][i]['link']
        bloggerID = json_object['items'][i]['bloggerlink'].replace('blog.naver.com/', "")
        results.append({
            "Title": title,
            "Blogger ID": bloggerID,
            "Link": mallName
        })
    
    return results

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



#--------------------------
# 제목 설정
st.title("한글 글자수 세기 by 철인29호")

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



# Streamlit 앱 제목
st.title("플레이스 순서대로 방문[Bros]")


# 초기 상태 설정
if 'stop' not in st.session_state:
    st.session_state.stop = False


# 사용자로부터 URL 입력받기
urls1 =[
    "https://m.blog.naver.com/dongnebros/223551645464",
    "https://m.blog.naver.com/dongnebros/223550514404",
    "https://m.blog.naver.com/dongnebros/223543231597",
    "https://m.blog.naver.com/dongnebros/223529949998",
    "https://m.blog.naver.com/dongnebros/223528378911",
]
     

# '정지' 버튼
if st.button('정지1'):
    st.session_state.stop = True
    st.write("플레이스 방문이 중단되었습니다.")
    
    # 열려 있는 창 닫기
    js_code4 = """
    <script type="text/javascript">
        if (typeof(window.new_window) !== 'undefined' && !window.new_window.closed) {
            window.new_window.close();
        }
    </script>
    """
    st.components.v1.html(js_code4)

# '플레이스 방문 시작' 버튼
if st.button('플레이스 방문1'):
    st.session_state.stop = False  # 중단 상태 초기화
    for i in range(0,10000):
        for site_url in urls1:
            if st.session_state.stop:
                st.write("사이트 방문이 중단되었습니다.")
                break

            # 같은 창에 새로운 URL 열기
            js_code3 = f"""
            <script type="text/javascript">
                if (typeof(window.new_window) === 'undefined' || window.new_window.closed) {{
                    window.new_window = window.open("{site_url}", "_blank");
                }} else {{
                    window.new_window.location.href = "{site_url}";
                }}
            </script>
            """
            st.components.v1.html(js_code3)
            random_delay()
    


