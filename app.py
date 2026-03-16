import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_title("📈 نظام تحليل المبيعات الذكي")

# 1. التحقق من وجود المفتاح في الـ Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("خطأ: يرجى إضافة GOOGLE_API_KEY في إعدادات Secrets.")
    st.stop()

# 2. إعداد الاتصال
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. استخدام نموذج gemini-pro (الأكثر استقراراً)
model = genai.GenerativeModel('gemini-pro')

uploaded_file = st.file_uploader("ارفع ملف CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(df)
    
    if st.button("تحليل"):
        try:
            losses = df[df['profit'] < 0].to_string()
            response = model.generate_content(f"حلل أسباب الخسارة التالية: {losses}")
            st.write(response.text)
        except Exception as e:
            st.error(f"خطأ: {e}")
