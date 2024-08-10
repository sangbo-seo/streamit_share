import streamlit as st


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