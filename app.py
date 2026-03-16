import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="محلل المبيعات الذكي", page_icon="📈")
st.title("📈 نظام تحليل المبيعات الذكي")
st.write("ارفع ملف المبيعات الخاص بك لاستخراج الأسباب الجذرية لانخفاض الربح.")

# إعداد مفتاح الذكاء الاصطناعي
api_key = "AIzaSyAwXpVjwawtxlNPiSN2zxUmOgQg9_p76LQ"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("اختر ملف المبيعات (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### بياناتك:")
    st.dataframe(df)
    
    if st.button("تحليل الأسباب الجذرية"):
        with st.spinner("جاري التحليل..."):
            losses = df[df['profit'] < 0]
            if losses.empty:
                st.success("تهانينا! لا توجد منتجات خاسرة.")
            else:
                prompt = f"حلل أسباب خسارة المنتجات التالية: {losses.to_string()}، وقدم نصائح عملية."
                response = model.generate_content(prompt)
                st.write("### 🧠 التحليل الذكي:")
                st.write(response.text)
