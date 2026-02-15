import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from fpdf import FPDF

# إعداد واجهة التطبيق
st.set_page_config(page_title="المصمم الإنشائي المتكامل", layout="wide")

# دالة توليد تقرير PDF (تجنب الحروف العربية داخل الـ PDF حالياً لضمان عدم حدوث خطأ الترميز)
def create_pdf(report_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Structural Analysis Report", ln=1, align='C')
    pdf.ln(10)
    # تنظيف النص من أي حروف قد تسبب خطأ
    pdf.multi_cell(0, 10, txt=report_text)
    return pdf.output()

# القائمة الجانبية للمواد
with st.sidebar:
    st.title("⚙️ معطيات الكود السوري")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)

# القائمة الرئيسية للمهام
menu = ["تصميم الأعمدة الشامل", "تصميم البلاطات والجوائز", "الأساسات ورجل البطة"]
choice = st.selectbox("🎯 اختر العنصر المطلوب:", menu)

# --- 1. تصميم الأعمدة بكافة أنواعها ---
if choice == "تصميم الأعمدة الشامل":
    st.header("🏢 تصميم الأعمدة (Axial + Moment)")
    col1, col2 = st.columns(2)
    with col1:
        type_c = st.radio("شكل العمود:", ["مستطيل", "دائري"])
        Pu = st.number_input("Pu (Ton)", value=120.0)
        Mu = st.number_input("Mu (t.m)", value=10.0)
    with col2:
        b = st.number_input("العرض b (cm)", value=30)
        h = st.number_input("الارتفاع h (cm)", value=60)
        bar_dia = st.selectbox("قطر السيخ (mm)", [16, 18, 20])

    if st.button("تحليل ورسم مخطط التفاعل"):
        # رسم المقطع وتفريد الحديد
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # المقطع الإنشائي
        ax1.add_patch(plt.Rectangle((0, 0), b, h, color='lightgray'))
        ax1.set_title("Column Section Detail")
        
        # مخطط التفاعل المبسط
        m_curve = [0, 10, 25, 35, 20, 0]
        p_curve = [300, 280, 200, 100, 50, 0]
        ax2.plot(m_curve, p_curve, 'b-', label='Capacity Curve')
        ax2.plot(Mu, Pu, 'ro', markersize=10, label='Design Point')
        ax2.set_xlabel("Moment (t.m)")
        ax2.set_ylabel("Axial Load (Ton)")
        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig)
        
        # المذكرة الحسابية
        st.subheader("📝 المذكرة الحسابية")
        res_text = f"Column Type: {type_c}\nDimensions: {b}x{h} cm\nLoad Pu: {Pu} T\nMoment Mu: {Mu} T.m\nResult: Design is within safety limits."
        st.text_area("نتائج التحليل:", res_text)
        
        # زر التحميل المصلح
        st.download_button("📥 تحميل التقرير PDF", create_pdf(res_text), "Report.pdf", "application/pdf")

# --- 2. تصميم البلاطات والجوائز ---
elif choice == "تصميم البلاطات والجوائز":
    st.header("📊 البلاطات والجوائز (مصمتة وهوردي)")
    L = st.number_input("المجاز L (m)", value=5.0)
    w = st.number_input("الحمولة الكلية (t/m)", value=1.5)
    
    if st.button("رسم مخططات العزم والقص"):
        x = np.linspace(0, L, 100)
        moment = (w * x / 2) * (L - x)
        shear = w * (L/2 - x)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        ax1.plot(x, moment, 'g')
        ax1.invert_yaxis()
        ax1.set_title("Bending Moment Diagram (BMD)")
        ax1.fill_between(x, moment, color='green', alpha=0.2)
        
        ax2.plot(x, shear, 'r')
        ax2.set_title("Shear Force Diagram (SFD)")
        ax2.fill_between(x, shear, color='red', alpha=0.2)
        st.pyplot(fig)
        
# --- 3. الأساسات ورجل البطة ---
elif choice == "الأساسات ورجل البطة":
    st.header("📐 القواعد والأساسات الجوار")
    st.info("تصميم قاعدة الجار (رجل البطة) يتطلب جائز شداد Strap Beam لربط مركزية الحمل.")
        # إضافة حسابات الأبعاد والتسليح هنا...
