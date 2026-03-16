import streamlit as st
import pandas as pd
import google.generativeai as genai

st.title("📈 نظام تحليل المبيعات الذكي")

# 1. إعداد الاتصال
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"خطأ في إعداد الاتصال: {e}")
        st.stop()
else:
    st.error("مفتاح GOOGLE_API_KEY غير موجود في الـ Secrets.")
    st.stop()

# 2. واجهة رفع الملف
uploaded_file = st.file_uploader("📤 ارفع ملف المبيعات (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### بياناتك:")
    st.dataframe(df)
    
    if st.button("تحليل الأسباب الجذرية"):
        with st.spinner("جاري التحليل..."):
            try:
                losses = df[df['profit'] < 0]
                if losses.empty:
                    st.success("تهانينا! لا توجد منتجات خاسرة.")
                else:
                    prompt = f"حلل أسباب الخسارة للمنتجات التالية: {losses.to_string()}، وقدم حلولاً عملية."
                    response = model.generate_content(prompt)
                    st.write("### 🧠 النتيجة:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"خطأ أثناء التحليل: {e}")
