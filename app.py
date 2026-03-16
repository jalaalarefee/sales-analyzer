import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="محلل المبيعات", page_icon="📈")
st.title("📈 نظام تحليل المبيعات الذكي")

# تأكد من وضع GOOGLE_API_KEY في إعدادات الـ Secrets
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# نستخدم نموذج gemini-1.0-pro لضمان التوافق التام
model = genai.GenerativeModel('gemini-1.0-pro')

uploaded_file = st.file_uploader("📤 ارفع ملف المبيعات (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### بياناتك:")
    st.dataframe(df)
    
    if st.button("تحليل الأسباب الجذرية"):
        with st.spinner("جاري التحليل..."):
            losses = df[df['profit'] < 0]
            if losses.empty:
                st.success("لا توجد خسائر.")
            else:
                prompt = f"حلل أسباب خسارة المنتجات التالية: {losses.to_string()}، وقدم نصائح عملية."
                response = model.generate_content(prompt)
                st.write("### 🧠 التحليل:")
                st.write(response.text)
