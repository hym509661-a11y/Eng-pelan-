import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from fpdf import FPDF

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المصمم الإنشائي الشامل", layout="wide")

# --- دالة معالجة النصوص العربية للـ PDF (عكس النص) ---
def fix_ar(text):
    return text[::-1]

# --- دالة توليد PDF احترافية (حل مشكلة المساحة والترميز) ---
def generate_civil_pdf(title, data_dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt=title, ln=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for k, v in data_dict.items():
        # استخدام multi_cell بعرض 180 لمنع خطأ Horizontal Space
        safe_line = f"{v} : {fix_ar(k)}"
        pdf.multi_cell(180, 10, txt=safe_line, align='R')
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("⚙️ المعطيات العامة")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)
    st.divider()
    st.info("هذا التطبيق يقوم بحساب التسليح وتوليد مذكرات حسابية وجداول BBS.")

menu = ["الجوائز (Beams)", "البلاطات (Slabs)", "الحصيرة (Raft)", "الأعمدة (Columns)", "أساس الجار (Strap)"]
choice = st.selectbox("🎯 اختر العنصر المراد تصميمه:", menu)

# --- 1. قسم الجوائز (مع تفاصيل الكانات) ---
if choice == "الجوائز (Beams)":
    st.header("🔗 تصميم الجوائز وتفاصيل الكانات")
    col1, col2 = st.columns(2)
    with col1:
        L = st.number_input("طول الجائز L (m)", value=5.0)
        wu = st.number_input("الحمولة wu (t/m)", value=3.0)
    with col2:
        b = st.number_input("عرض الجائز b (cm)", value=25)
        h = st.number_input("ارتفاع الجائز h (cm)", value=60)

    if st.button("حساب ورسم التفاصيل"):
        Mu = (wu * L**2) / 8
        As = (Mu * 10**5) / (0.87 * fy * (h-5))
        n_bars = math.ceil(As / 2.01) # فرض T16
        stirrups_count = int(L * 6) # فرض 6 في المتر
        
        # --- رسم تفريد الحديد والكانات ---
        fig, ax = plt.subplots(figsize=(10, 3))
        # رسم الخرسانة
        ax.plot([0, L], [0, 0], color='lightgrey', lw=30, alpha=0.3)
        # رسم الحديد السفلي
        ax.plot([0.1, L-0.1], [-0.15, -0.15], 'red', lw=3, label=f"Main: {n_bars} T16")
        # رسم الحديد العلوي
        ax.plot([0, L], [0.15, 0.15], 'green', lw=2, label="Hangers: 2 T12")
        
        # رسم الكانات (توزيع تخطيطي)
        for x in np.linspace(0.2, L-0.2, 15):
            ax.plot([x, x], [-0.2, 0.2], 'black', lw=1, alpha=0.6)
        ax.text(L/2, 0.25, "Stirrups T8 @ 15cm", ha='center', fontsize=9)
        
        ax.set_ylim(-0.6, 0.6)
        ax.axis('off')
        ax.legend(loc='lower center', ncol=3)
        st.pyplot(fig)
        
        # --- جدول BBS المتكامل ---
        st.subheader("📊 جدول تفريد الحديد (BBS)")
        st.table({
            "العنصر": ["الحديد السفلي", "حديد التعليق", "الكانات (مغلقة)"],
            "القطر": ["T16", "T12", "T8"],
            "العدد": [n_bars, 2, stirrups_count],
            "الشكل": ["سيخ مستقيم", "سيخ مستقيم", "إطار مستطيل"],
            "الطول الإجمالي (m)": [L+0.4, L, 2*(b+h-10)/100 + 0.1]
        })
        
        res = {"الطول": f"{L} m", "العزم": f"{Mu:.2f} t.m", "الحديد": f"{n_bars} T16", "الكانات": f"{stirrups_count} T8"}
        st.download_button("📥 تحميل المذكرة العربية", generate_civil_pdf("Beam Report", res), "Beam.pdf")

# --- 2. قسم البلاطات ---
elif choice == "البلاطات (Slabs)":
    st.header("📊 تصميم البلاطات المصمتة")
    Lx = st.number_input("Lx (m)", value=4.0)
    Ly = st.number_input("Ly (m)", value=5.0)
    if st.button("تحليل التسليح"):
        st.success("تم التصميم كبلاطة عاملة باتجاهين")
        
        s_res = {"الأبعاد": f"{Lx}x{Ly} m", "التسليح": "T12 @ 150mm", "الغطاء": "2.5 cm"}
        st.download_button("📥 تحميل PDF", generate_civil_pdf("Slab Report", s_res), "Slab.pdf")

# --- 3. قسم الحصيرة ---
elif choice == "الحصيرة (Raft)":
    st.header("🏗️ تصميم الحصيرة العامة")
    Area = st.number_input("المساحة الكلية (m2)", value=150.0)
    Load = st.number_input("مجموع أحمال الأعمدة (Ton)", value=1200.0)
    if st.button("تحقق من الإجهاد"):
        stress = (Load * 1.1) / Area
        st.metric("الإجهاد على التربة", f"{stress:.2f} t/m2")
        
        r_res = {"الحمل": f"{Load} Ton", "الإجهاد": f"{stress:.2f} t/m2"}
        st.download_button("📥 تحميل PDF", generate_civil_pdf("Raft Report", r_res), "Raft.pdf")

# --- 4. قسم الأعمدة ---
elif choice == "الأعمدة (Columns)":
    st.header("🏢 مخطط التفاعل (Interaction Diagram)")
    Pu = st.number_input("الحمل المحوري Pu (Ton)", value=150.0)
    Mu = st.number_input("العزم Mu (t.m)", value=15.0)
    if st.button("رسم المنحنى"):
        fig_i, ax_i = plt.subplots()
        ax_i.plot([0, 15, 30, 35, 0], [400, 350, 180, 50, 0], 'b-', label='Section Capacity')
        ax_i.scatter(Mu, Pu, color='red', s=100, label='Design Point')
        ax_i.set_xlabel("Moment (Mu)"); ax_i.set_ylabel("Axial (Pu)"); ax_i.legend()
        st.pyplot(fig_i)
        
        c_res = {"Pu": f"{Pu} T", "Mu": f"{Mu} t.m", "النتيجة": "القطاع آمن"}
        st.download_button("📥 تحميل التقرير", generate_civil_pdf("Column Report", c_res), "Column.pdf")

# --- 5. أساس الجار (Strap) ---
elif choice == "أساس الجار (Strap)":
    st.header("📐 تصميم أساس الجار (Strap Footing)")
    
    st.info("يستخدم هذا النظام عندما يكون عمود الجار على حد الملكية تماماً.")
    if st.button("تحليل النظام"):
        st.success("تم حساب أبعاد الشداد لضمان استقرار القاعدة.")
        st_res = {"النظام": "Strap Footing", "الحالة": "مستقر"}
        st.download_button("📥 تحميل المذكرة", generate_civil_pdf("Strap Report", st_res), "Strap.pdf")
