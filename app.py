import streamlit as st
import pandas as pd
import io
import google.generativeai as genai

st.set_page_config(page_title="محلل المبيعات", page_icon="📈")
st.title("📈 نظام تحليل المبيعات الذكي")

api_key = "AIzaSyAwXpVjwawtxlNPiSN2zxUmOgQg9_p76LQ"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# إنشاء تبويبات (Tabs)
tab1, tab2 = st.tabs(["📤 رفع ملف", "📝 لصق بيانات"])

df = None

with tab1:
    uploaded_file = st.file_uploader("اختر ملف CSV", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

with tab2:
    data_input = st.text_area("الصق البيانات هنا (الاسم,المبيعات,الربح):", "Laptop,5000,1000\nMouse,150,-20")
    if st.button("تحميل البيانات الملصقة"):
        df = pd.read_csv(io.StringIO(data_input), names=['product', 'sales', 'profit'], skipinitialspace=True)

# عملية التحليل المشتركة
if df is not None:
    st.write("### بياناتك:")
    st.dataframe(df)
    
    if st.button("تحليل الأسباب الجذرية"):
        with st.spinner("جاري التحليل..."):
            losses = df[df['profit'] < 0]
            if losses.empty:
                st.success("لا توجد منتجات خاسرة!")
            else:
                prompt = f"حلل أسباب خسارة المنتجات التالية: {losses.to_string()}، وقدم نصائح عملية."
                response = model.generate_content(prompt)
                st.write("### 🧠 التحليل الذكي:")
                st.write(response.text)
