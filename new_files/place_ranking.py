
import streamlit as st

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