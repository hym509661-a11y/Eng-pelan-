import streamlit as st
import pandas as pd
import ezdxf

# إعدادات الصفحة
st.set_page_config(page_title="Civil Linker: ETABS-SAFE-CAD", layout="wide")

st.title("🏗️ منصة الربط الهندسي المتكاملة")
st.write("دمج بيانات التصميم بين ETABS و SAFE والتصدير لـ AutoCAD")

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("إعدادات المشروع")
    project_name = st.text_input("اسم المشروع", "مشروع جديد")
    st.info(f"رقم التواصل المسجل: 0998449697") # إضافة الرقم حسب طلبك

# --- القسم الأول: استيراد البيانات من ETABS ---
st.header("1. استيراد بيانات ETABS")
uploaded_etabs = st.file_uploader("ارفع ملف Excel المصدر من ETABS (Base Reactions)", type=['xlsx'])

if uploaded_etabs:
    df_etabs = pd.read_excel(uploaded_etabs)
    st.success("تم تحميل بيانات ETABS بنجاح!")
    st.dataframe(df_etabs.head()) # عرض عينة من البيانات

---

# --- القسم الثاني: المعالجة لبرنامج SAFE ---
st.header("2. تجهيز البيانات لـ SAFE")
st.write("تعديل الأحمال وتنسيقها لتناسب استيراد ملفات F2K أو Excel في SAFE.")
if st.button("تجهيز ملف الـ SAFE"):
    # هنا تضع معادلات التصحيح أو تجميع الأحمال
    st.warning("جاري تحويل التنسيق... (يتم برمجته بناءً على نسخة SAFE لديك)")

---

# --- القسم الثالث: التصدير لـ AutoCAD ---
st.header("3. تصدير اللوحات (AutoCAD)")
if st.button("توليد ملف DXF"):
    doc = ezdxf.new()
    msp = doc.modelspace()
    
    # مثال: رسم جدول القواعد تلقائياً بناءً على البيانات
    msp.add_text("جدول أحمال القواعد", dxfattribs={'height': 0.5}).set_placement((0, 10))
    # إضافة ختم المشروع برقمك
    msp.add_text(f"Contact: 0998449697", dxfattribs={'height': 0.3}).set_placement((0, -2))
    
    doc.saveas("Civil_Design_Output.dxf")
    st.success("تم إنشاء ملف AutoCAD (DXF) بنجاح!")
    
    with open("Civil_Design_Output.dxf", "rb") as file:
        st.download_button("تحميل ملف الـ CAD", file, "Design.dxf")
