import streamlit as st
from urllib.parse import quote, unquote




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



