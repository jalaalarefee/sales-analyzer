import streamlit as st
import google.generativeai as genai

st.title("🔍 فحص النماذج المتاحة")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    if st.button("عرض قائمة النماذج المتاحة"):
        try:
            models = genai.list_models()
            for m in models:
                st.write(f"النموذج: {m.name} - (يدعم: {m.supported_generation_methods})")
        except Exception as e:
            st.error(f"خطأ في الاتصال: {e}")
else:
    st.error("مفتاح GOOGLE_API_KEY غير موجود في الـ Secrets")
