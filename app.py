import streamlit as st
import pandas as pd
import google.generativeai as genai

st.title("📈 نظام تحليل المبيعات الذكي")

# 1. إعداد المفتاح
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("يرجى إضافة GOOGLE_API_KEY في إعدادات الـ Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. تعريف النموذج باستخدام الاسم الأكثر توافقاً (gemini-pro)
# هذا النموذج هو الأقل عرضة لخطأ 404 في النسخ المجانية
model = genai.GenerativeModel('gemini-pro')

uploaded_file = st.file_uploader("📤 ارفع ملف CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### بياناتك:")
    st.dataframe(df)
    
    if st.button("تحليل الأسباب"):
        with st.spinner("جاري المعالجة..."):
            try:
                # تصفية الخسائر
                losses = df[df['profit'] < 0]
                if losses.empty:
                    st.success("لا توجد خسائر.")
                else:
                    prompt = f"حلل أسباب خسارة المنتجات التالية وقدم نصائح: {losses.to_string()}"
                    response = model.generate_content(prompt)
                    st.write("### 🧠 التحليل:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"خطأ: {e}")
