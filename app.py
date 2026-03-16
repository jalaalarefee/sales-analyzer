import streamlit as st
import google.generativeai as genai

st.title("📈 محلل المبيعات الذكي")

# تأكد أن اسم المفتاح في Secrets مطابق تماماً لهذا
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # اختبار سريع للاتصال
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.success("تم الاتصال بالذكاء الاصطناعي بنجاح!")
    except Exception as e:
        st.error(f"خطأ في إعداد الاتصال: {e}")
else:
    st.error("مفتاح GOOGLE_API_KEY غير موجود في الـ Secrets. الرجاء إضافته.")
