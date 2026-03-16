import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.express as px

# 1. إعداد واجهة الصفحة
st.set_page_config(page_title="نظام تحليل الأداء المالي", layout="wide")
st.title("⚖️ نظام التحليل والمقارنة الذكي للمتاجر")

# 2. إعداد الاتصال واختيار النموذج تلقائياً
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # كود ذكي لاختيار النموذج المتاح
        def get_model():
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    return genai.GenerativeModel(m.name)
            return None
        
        model = get_model()
        if not model:
            st.error("لم يتم العثور على نموذج متاح يدعم التحليل.")
            st.stop()
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
        st.stop()
else:
    st.error("يرجى إضافة GOOGLE_API_KEY في إعدادات الـ Secrets.")
    st.stop()

# 3. واجهة رفع الملفات
col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("📥 ارفع ملف الشهر الأول (CSV)", type="csv")
with col2:
    file2 = st.file_uploader("📥 ارفع ملف الشهر الثاني (CSV)", type="csv")

# دالة التحليل الموحدة
def analyze(data_str, prompt_text):
    with st.spinner("جاري التحليل الاستراتيجي..."):
        full_prompt = f"{prompt_text}\n\nالبيانات:\n{data_str}"
        response = model.generate_content(full_prompt)
        st.markdown("---")
        st.subheader("🧠 نتيجة التحليل الاستراتيجي")
        st.write(response.text)
        st.download_button("📥 تحميل التقرير", response.text, file_name="analysis.txt")

# 4. منطق المقارنة أو التحليل العام
if file1 and file2:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df1['period'] = 'الشهر الأول'
    df2['period'] = 'الشهر الثاني'
    combined_df = pd.concat([df1, df2])
    
    st.subheader("📊 مقارنة الأداء")
    
    fig = px.bar(combined_df, x='product', y='profit', color='period', barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("🚀 ابدأ التحليل المقارن"):
        analyze(combined_df.to_string(), "قارن بين أداء الشهرين، حدد التحسن والتراجع، وقدم توصيات.")

elif file1 or file2:
    target_file = file1 if file1 else file2
    df = pd.read_csv(target_file)
    st.subheader("📋 بيانات المتجر")
    st.dataframe(df)
    
    if st.button("🚀 ابدأ التحليل العام"):
        analyze(df.to_string(), "حلل أداء المتجر، حدد المنتجات الأكثر ربحية وخسارة، وقدم توصيات للتحسين.")
