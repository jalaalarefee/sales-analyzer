import streamlit as st
import pandas as pd
import google.generativeai as genai

# عنوان التطبيق
st.title("📈 نظام تحليل المبيعات الذكي")

# التحقق من وجود المفتاح في الـ Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("خطأ: يرجى إضافة GOOGLE_API_KEY في إعدادات الـ Secrets.")
    st.stop()

# إعداد الاتصال
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # استخدام النموذج الأكثر استقراراً وتوافقاً حالياً
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"خطأ في إعداد الاتصال: {e}")
    st.stop()

# رفع الملف
uploaded_file = st.file_uploader("📤 ارفع ملف المبيعات (CSV)", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("### بياناتك:")
        st.dataframe(df)
        
        if st.button("تحليل الأسباب الجذرية"):
            with st.spinner("جاري التواصل مع الذكاء الاصطناعي..."):
                # تصفية المنتجات التي تحقق خسارة (profit أقل من 0)
                losses = df[df['profit'] < 0]
                
                if losses.empty:
                    st.success("تهانينا! لا توجد منتجات خاسرة في بياناتك.")
                else:
                    prompt = f"حلل أسباب خسارة المنتجات التالية بناءً على المبيعات والربح: {losses.to_string()}، وقدم نصائح عملية لتحسين الأداء."
                    response = model.generate_content(prompt)
                    st.write("### 🧠 التحليل الذكي:")
                    st.write(response.text)
    except Exception as e:
        st.error(f"حدث خطأ أثناء معالجة الملف أو التحليل: {e}")
