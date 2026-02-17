import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="Civil Linker", layout="wide")

# العنوان الرئيسي
st.title("🏗️ منصة الربط الهندسي (ETABS - SAFE - CAD)")
st.write("أداة هندسية لدمج البيانات وتسهيل التصميم")

# --- القائمة الجانبية ---
st.sidebar.header("إعدادات المشروع")
project_name = st.sidebar.text_input("اسم المشروع", "مشروع جديد")
st.sidebar.info("للتواصل والدعم الفني: 0998449697")

# --- القسم الأول: ETABS ---
st.header("1. بيانات ETABS")
uploaded_etabs = st.file_uploader("ارفع ملف اكسل من ETABS", type=['xlsx'])

if uploaded_etabs:
    try:
        df = pd.read_excel(uploaded_etabs)
        st.success("تم رفع البيانات بنجاح")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"حدث خطأ أثناء القراءة: {e}")

# فاصل بصري
st.markdown("---")

# --- القسم الثاني: SAFE ---
st.header("2. التجهيز لبرنامج SAFE")
if st.button("تحويل البيانات لصيغة SAFE"):
    st.info("هذه الميزة ستقوم بتحويل جداول الاحمال إلى تنسيق F2K قريباً.")

# فاصل بصري
st.markdown("---")

# --- القسم الثالث: AutoCAD ---
st.header("3. تصدير AutoCAD")
if st.button("توليد ملف الرسم (DXF)"):
    st.warning("يتم الآن بناء محرك الرسم التلقائي...")
    # هنا سيتم إضافة كود مكتبة ezdxf لاحقاً
