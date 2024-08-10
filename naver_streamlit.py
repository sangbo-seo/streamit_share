import streamlit as st
import requests

# Streamlit 애플리케이션 제목
st.title('웹사이트 접속 예제')


# 사용자로부터 URL 입력받기
url = st.text_input('열고 싶은 URL을 입력하세요:', 'https://www.example.com')

# 버튼 클릭 시 JavaScript로 새 창 열기
if st.button('새 창으로 열기'):
    js_code = f"""
    <script type="text/javascript">
        window.open("{url}");
    </script>
    """
    st.components.v1.html(js_code)


# 사용자로부터 URL 입력받기
url = st.text_input('접속할 URL을 입력하세요:', 'https://m.naver.com')

# 접속 버튼
if st.button('접속하기'):
    # URL 접속 시도
    try:
        response = requests.get(url)
        
        # 응답 성공 시, 상태 코드와 콘텐츠를 출력
        if response.status_code == 200:
            st.success(f"성공적으로 {url}에 접속했습니다.")
            st.write(f"응답 코드: {response.status_code}")
            st.write(response.text[:1000])  # 응답 내용의 일부를 출력
        else:
            st.error(f"{url}에 접속하는 데 실패했습니다. 상태 코드: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        # 예외 발생 시, 오류 메시지 출력
        st.error(f"에러 발생: {e}")

