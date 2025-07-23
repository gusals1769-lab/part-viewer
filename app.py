import os
import base64
import streamlit as st
import pandas as pd

# 페이지 제목 및 레이아웃 설정
st.set_page_config(page_title="품목코드로 도면 조회", layout="wide")
st.title("📐 품목코드로 도면 조회")

# 1) 엑셀에서 '품목코드' 컬럼만 읽어서 집합으로 저장
df = pd.read_excel("품목코드.xlsx", usecols=["품목코드"])
df["품목코드"] = df["품목코드"].astype(str).str.strip().str.upper()
codes = set(df["품목코드"])

# 2) PDF를 base64로 읽어서 브라우저에서 차단 덜 받는 방식(object)으로 띄우는 함수
def show_pdf(path, filename):
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")

    html = f"""
    <object data="data:application/pdf;base64,{b64}" type="application/pdf"
            width="100%" height="800px">
        <p>PDF 미리보기가 차단되었습니다.
           <a href="data:application/pdf;base64,{b64}" download="{filename}">다운로드</a>하거나
           <a href="data:application/pdf;base64,{b64}" target="_blank">새 탭에서 열기</a>를 눌러주세요.</p>
    </object>
    """
    st.components.v1.html(html, height=820, scrolling=True)

    # (선택) 다운로드 버튼도 하나 더 제공
    st.download_button("PDF 다운로드", data, file_name=filename, mime="application/pdf")

# 3) 사용자 입력 UI
code_input = st.text_input("품목코드 입력").strip().upper()
if st.button("조회"):
    if code_input in codes:
        pdf_path = os.path.join("drawings", f"{code_input}.pdf")
        if os.path.exists(pdf_path):
            show_pdf(pdf_path, f"{code_input}.pdf")
        else:
            st.error("❌ 해당 도면 파일이 존재하지 않습니다.")
    else:
        st.error("❌ 해당 품목코드를 찾을 수 없습니다.")
