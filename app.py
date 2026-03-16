import streamlit as st
import pandas as pd
import io
import google.generativeai as genai

st.set_page_config(page_title="محلل المبيعات", page_icon="📈")
st.title("📈 نظام تحليل المبيعات الذكي")

api_key = "AIzaSyAwXpVjwawtxlNPiSN2zxUmOgQg9_p76LQ"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# خيار اللصق النصي بدلاً من الملف
data_input = st.text_area("أو الصق البيانات هنا (المنتج, المبيعات, الربح):", 
                         "Laptop,5000,1000\nMouse,150,-20\nKeyboard,300,50\nPrinter,800,-50")

if st.button("تحليل الأسباب الجذرية"):
    try:
        # تحويل النص إلى جدول
        data_io = io.StringIO(data_input)
        df = pd.read_csv(data_io, names=['product', 'sales', 'profit'], header=None)
        
        st.write("### بياناتك:")
        st.dataframe(df)
        
        losses = df[df['profit'] < 0]
        if losses.empty:
            st.success("لا توجد خسائر!")
        else:
            prompt = f"حلل أسباب خسارة المنتجات التالية: {losses.to_string()}، وقدم نصائح عملية."
            response = model.generate_content(prompt)
            st.write("### 🧠 التحليل الذكي:")
            st.write(response.text)
    except Exception as e:
        st.error(f"خطأ في قراءة البيانات: تأكد من التنسيق (منتج,مبيعات,ربح). الخطأ: {e}")

