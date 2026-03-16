import streamlit as st
import pandas as pd
import google.generativeai as genai

st.title("📈 محلل المبيعات الذكي")

# 1. إعداد المفتاح
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("يرجى إضافة GOOGLE_API_KEY في إعدادات الـ Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. كود ذكي لاختيار النموذج المتاح تلقائياً
def get_best_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return genai.GenerativeModel(m.name)
    return None

model = get_best_model()

uploaded_file = st.file_uploader("📤 ارفع ملف CSV", type="csv")

if uploaded_file and model:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
    
    if st.button("تحليل الأسباب"):
        try:
            losses = df[df['profit'] < 0].to_string()
            response = model.generate_content(f"حلل أسباب خسارة المنتجات: {losses}")
            st.write("### 🧠 التحليل:")
            st.write(response.text)
        except Exception as e:
            st.error(f"خطأ: {e}")
elif not model:
    st.error("لم يتم العثور على نموذج يدعم generateContent في حسابك.")
