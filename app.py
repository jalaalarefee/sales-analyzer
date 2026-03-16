import streamlit as st
import pandas as pd
import io
import google.generativeai as genai

# إعداد واجهة التطبيق
st.set_page_config(page_title="محلل المبيعات الذكي", page_icon="📈")
st.title("📈 نظام تحليل المبيعات الذكي")

# قراءة المفتاح من الخزنة الآمنة (Secrets)
# تأكد أنك وضعت GOOGLE_API_KEY في إعدادات الـ Secrets في موقع Streamlit
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# إعداد النموذج
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# إنشاء تبويبات (Tabs)
tab1, tab2 = st.tabs(["📤 رفع ملف CSV", "📝 لصق بيانات يدوياً"])

df = None

with tab1:
    uploaded_file = st.file_uploader("اختر ملف CSV", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

with tab2:
    data_input = st.text_area("الصق البيانات هنا (الاسم,المبيعات,الربح):", "Laptop,5000,1000\nMouse,150,-20")
    if st.button("تحميل البيانات الملصقة"):
        # تحويل النص المدخل إلى جدول
        data_io = io.StringIO(data_input.strip())
        df = pd.read_csv(data_io, names=['product', 'sales', 'profit'], skipinitialspace=True)

# عملية التحليل المشتركة
if df is not None:
    st.write("### بياناتك:")
    st.dataframe(df)
    
    if st.button("تحليل الأسباب الجذرية"):
        with st.spinner("جاري التحليل بواسطة الذكاء الاصطناعي..."):
            losses = df[df['profit'] < 0]
            if losses.empty:
                st.success("تهانينا! لا توجد منتجات خاسرة في بياناتك.")
            else:
                prompt = f"حلل أسباب خسارة المنتجات التالية: {losses.to_string()}، وقدم نصائح عملية لتحسين الأرباح."
                response = model.generate_content(prompt)
                st.write("### 🧠 التحليل الذكي:")
                st.write(response.text)
