import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.express as px

# 1. إعداد واجهة الصفحة
st.set_page_config(page_title="نظام تحليل الأداء المالي", layout="wide")
st.title("⚖️ نظام المقارنة الذكي للأداء المالي")

# 2. إعداد الاتصال بالذكاء الاصطناعي
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("يرجى التأكد من إضافة GOOGLE_API_KEY في إعدادات الـ Secrets.")
    st.stop()

# 3. واجهة رفع الملفات
st.sidebar.header("إعدادات المقارنة")
col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("📥 ارفع ملف الشهر الأول (CSV)", type="csv")
with col2:
    file2 = st.file_uploader("📥 ارفع ملف الشهر الثاني (CSV)", type="csv")

# 4. معالجة البيانات والمقارنة
if file1 and file2:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # إضافة عمود الفترة للتمييز عند الدمج
    df1['period'] = 'الشهر الأول'
    df2['period'] = 'الشهر الثاني'
    combined_df = pd.concat([df1, df2])
    
    st.subheader("📊 مقارنة الأداء البصري")
    
    fig = px.bar(combined_df, x='product', y='profit', color='period', 
                 barmode='group', title="مقارنة أرباح المنتجات بين فترتين")
    st.plotly_chart(fig, use_container_width=True)
    
    # 5. التحليل الذكي الشامل (عام + مقارن)
    if st.button("🚀 ابدأ التحليل الكامل (عام + مقارن)"):
        with st.spinner("جاري التحليل الاستراتيجي للبيانات..."):
            prompt = f"""
            أنت خبير مالي وذكاء أعمال. لديك بيانات مبيعات لشهرين:
            {combined_df.to_string()}
            
            المطلوب منك القيام بـ 3 مهام دقيقة:
            1. تحليل عام لكل شهر على حدة (نقاط القوة والضعف في كل شهر).
            2. مقارنة أداء الشهرين (ما الذي تحسن؟ وما الذي تراجع؟ ولماذا؟).
            3. تقديم 3 توصيات استراتيجية للمستقبل بناءً على اتجاه البيانات بين الشهرين.
            4. تقييم شامل لحالة المتجر.
            """
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.subheader("🧠 نتيجة التحليل الاستراتيجي المقارن")
                st.write(response.text)
                
                # زر تحميل التقرير
                st.download_button("📥 تحميل التحليل كملف نصي", response.text, file_name="comparison_report.txt")
            except Exception as e:
                st.error(f"حدث خطأ أثناء التحليل: {e}")

elif file1 or file2:
    st.info("يرجى رفع ملفين للمقارنة بينهما.")

# 6. قسم التذييل
with st.sidebar:
    st.write("---")
    st.success("النظام جاهز للعمل")
    st.info("ملاحظة: تأكد أن ملفات الـ CSV تحتوي على أعمدة: product, sales, profit")
