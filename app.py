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

# 2) PDF를 base64로 읽어서 iframe에 띄우는 함수
def show_pdf(path):
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    iframe = f"""
    <iframe
      src="data:application/pdf;base64,{b64}"
      width="100%"
      height="800px"
      type="application/pdf"
    ></iframe>
    """
    st.markdown(iframe, unsafe_allow_html=True)

# 3) 사용자 입력 UI
code_input = st.text_input("품목코드 입력").strip().upper()
if st.button("조회"):
    if code_input in codes:
        pdf_path = os.path.join("drawings", f"{code_input}.pdf")
        if os.path.exists(pdf_path):
            show_pdf(pdf_path)
        else:
            st.error("❌ 해당 도면 파일이 존재하지 않습니다.")
    else:
        st.error("❌ 해당 품목코드를 찾을 수 없습니다.")