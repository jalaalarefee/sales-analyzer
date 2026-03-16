import streamlit as st
import pandas as pd
import google.generativeai as genai

st.title("📈 نظام تحليل المبيعات الذكي")

# قراءة المفتاح من الـ Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("لم يتم العثور على المفتاح في إعدادات Secrets!")
    st.stop()

uploaded_file = st.file_uploader("📥 ارفع ملف CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### البيانات:")
    st.dataframe(df)
    
    if st.button("تحليل الأسباب"):
        losses = df[df['profit'] < 0].to_string()
        response = model.generate_content(f"حلل أسباب خسارة المنتجات التالية: {losses}")
        st.write("### 🧠 التحليل:")
        st.write(response.text)
