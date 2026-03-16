import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.express as px

# 1. إعداد واجهة الصفحة
st.set_page_config(page_title="نظام تحليل الأداء المالي", layout="wide")
st.title("⚖️ نظام التحليل والمقارنة الذكي للمتاجر")

# 2. إعداد الاتصال
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("يرجى إضافة GOOGLE_API_KEY في إعدادات الـ Secrets.")
    st.stop()

# 3. واجهة رفع الملفات
st.sidebar.header("إعدادات البيانات")
col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("📥 ارفع ملف الشهر الأول (CSV)", type="csv")
with col2:
    file2 = st.file_uploader("📥 ارفع ملف الشهر الثاني (CSV)", type="csv")

# 4. منطق التحليل الذكي (يتحسس الملفات المرفوعة)
def analyze_data(data_str, prompt_text):
    with st.spinner("جاري التحليل الاستراتيجي..."):
        prompt = f"{prompt_text}\n\nالبيانات:\n{data_str}"
        response = model.generate_content(prompt)
        st.markdown("---")
        st.subheader("🧠 نتيجة التحليل الاستراتيجي")
        st.write(response.text)
        st.download_button("📥 تحميل التحليل كملف نصي", response.text, file_name="report.txt")

# الحالة (أ): مقارنة ملفين
if file1 and file2:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df1['period'] = 'الشهر الأول'
    df2['period'] = 'الشهر الثاني'
    combined_df = pd.concat([df1, df2])
    
    st.subheader("📊 مقارنة الأداء البصري")
    
    fig = px.bar(combined_df, x='product', y='profit', color='period', barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("🚀 ابدأ التحليل المقارن"):
        analyze_data(combined_df.to_string(), "قارن بين أداء الشهرين المرفقين، حدد التحسن والتراجع، وقدم 3 توصيات.")

# الحالة (ب): تحليل ملف واحد فقط
elif file1 or file2:
    target_file = file1 if file1 else file2
    df = pd.read_csv(target_file)
    st.subheader("📋 بيانات المتجر")
    st.dataframe(df)
    
    
    if st.button("🚀 ابدأ التحليل العام"):
        analyze_data(df.to_string(), "حلل أداء هذا المتجر، حدد المنتجات الأكثر ربحية وخسارة، وقدم توصيات لتحسين الأرباح.")

else:
    st.info("يرجى رفع ملف واحد للتحليل العام، أو ملفين للمقارنة بينهما.")

with st.sidebar:
    st.write("---")
    st.success("النظام جاهز للعمل")
