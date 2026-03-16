import streamlit as st
import pandas as pd
import io
import google.generativeai as genai

st.set_page_config(page_title="محلل المبيعات", page_icon="📈")
st.title("📈 نظام تحليل المبيعات الذكي")

# التحقق من وجود المفتاح في الـ Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("مفتاح الـ API غير موجود في إعدادات الـ Secrets. يرجى إضافته.")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# نستخدم gemini-1.5-flash كنموذج أساسي
model = genai.GenerativeModel('gemini-1.5-flash')

tab1, tab2 = st.tabs(["📤 رفع ملف", "📝 لصق بيانات"])
df = None

with tab1:
    uploaded_file = st.file_uploader("اختر ملف CSV", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

with tab2:
    data_input = st.text_area("البيانات (الاسم,المبيعات,الربح):", "Laptop,5000,1000\nMouse,150,-20")
    if st.button("تجهيز البيانات"):
        df = pd.read_csv(io.StringIO(data_input), names=['product', 'sales', 'profit'], skipinitialspace=True)

if df is not None:
    st.write("### البيانات:")
    st.dataframe(df)
    
    if st.button("تحليل الأسباب الجذرية"):
        losses = df[df['profit'] < 0]
        if losses.empty:
            st.success("لا توجد خسائر.")
        else:
            try:
                prompt = f"حلل أسباب خسارة المنتجات: {losses.to_string()}، وقدم نصائح."
                response = model.generate_content(prompt)
                st.write("### 🧠 التحليل:")
                st.write(response.text)
            except Exception as e:
                st.error(f"خطأ في الاتصال بالذكاء الاصطناعي: {e}")
