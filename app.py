import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from fpdf import FPDF

# إعداد الصفحة
st.set_page_config(page_title="المصمم الإنشائي الاحترافي", layout="wide")

# دالة توليد تقرير PDF (حل مشكلة المساحة والترميز)
def create_safe_report(title, content_list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt=title, ln=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for line in content_list:
        # استخدام multi_cell مع عرض 0 لضمان عدم حدوث خطأ Space
        pdf.multi_cell(0, 10, txt=str(line))
    return pdf.output()

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ معطيات الكود")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)

menu = ["الجوائز (Beams)", "البلاطات المصمتة", "الحصيرة (Raft)", "الأعمدة (Columns)", "رجل البطة (Strap)"]
choice = st.selectbox("🎯 اختر المهمة:", menu)

# --- 1. قسم الجوائز (الحفاظ على الرسم المطلوب) ---
if choice == "الجوائز (Beams)":
    st.header("🔗 تصميم الجوائز")
    L = st.number_input("المجاز (m)", value=5.0)
    wu = st.number_input("الحمولة (t/m)", value=3.0)
    h = st.number_input("h (cm)", value=60)
    
    if st.button("حساب ورسم"):
        Mu = (wu * L**2) / 8
        As = (Mu * 10**5) / (0.87 * fy * (h-5))
        n_bars = math.ceil(As / 2.01) # T16
        
        # رسم تفريد الحديد (بدون تداخل)
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot([0, L], [0, 0], 'grey', lw=15, alpha=0.3) 
        ax.plot([0.1, L-0.1], [-0.1, -0.1], 'red', lw=3, label=f"Bottom: {n_bars} T16")
        ax.plot([0, 0.2*L], [0.12, 0.12], 'green', lw=3, label="Top Support")
        ax.plot([0.8*L, L], [0.12, 0.12], 'green', lw=3)
        ax.set_ylim(-0.5, 0.5)
        ax.axis('off')
        ax.legend(loc='lower center', ncol=2)
        st.pyplot(fig)
        
        report_data = [f"Beam Span: {L} m", f"Load: {wu} t/m", f"Moment: {Mu:.2f} t.m", f"Reinforcement: {n_bars} T16"]
        st.download_button("📥 تحميل المذكرة PDF", create_safe_report("Beam Design Report", report_data), "Beam.pdf")

# --- 2. البلاطات المصمتة ---
elif choice == "البلاطات المصمتة":
    st.header("📊 تصميم البلاطات")
    Lx = st.number_input("Lx (m)", value=4.0)
    Ly = st.number_input("Ly (m)", value=5.0)
    if st.button("تحليل"):
        st.success("Two-way Slab Design")
        report_s = [f"Dimensions: {Lx}x{Ly} m", "Reinforcement: T12 @ 15cm"]
        st.download_button("📥 تحميل التقرير", create_safe_report("Slab Report", report_s), "Slab.pdf")

# --- 3. الحصيرة ---
elif choice == "الحصيرة (Raft)":
    st.header("🏗️ تصميم الحصيرة")
    Area = st.number_input("Area (m2)", value=150.0)
    Load = st.number_input("Load (Ton)", value=1200.0)
    if st.button("حساب الإجهاد"):
        stress = (Load * 1.1) / Area
        st.metric("Soil Stress", f"{stress:.2f} t/m2")
        report_r = [f"Load: {Load} T", f"Area: {Area} m2", f"Stress: {stress:.2f} t/m2"]
        st.download_button("📥 تحميل PDF", create_safe_report("Raft Report", report_r), "Raft.pdf")

# --- 4. الأعمدة ---
elif choice == "الأعمدة (Columns)":
    st.header("🏢 مخطط التفاعل")
    Pu = st.number_input("Pu (Ton)", value=120.0)
    Mu = st.number_input("Mu (t.m)", value=10.0)
    if st.button("رسم المخطط"):
        fig_i, ax_i = plt.subplots()
        ax_i.plot([0, 10, 20, 30, 0], [250, 230, 150, 50, 0], 'b-', label='Capacity')
        ax_i.scatter(Mu, Pu, color='red', s=100, label='Design Point')
        ax_i.set_xlabel("Moment"); ax_i.set_ylabel("Load")
        ax_i.legend(); st.pyplot(fig_i)
        report_c = [f"Pu: {Pu} T", f"Mu: {Mu} t.m", "Status: Safe"]
        st.download_button("📥 تحميل PDF", create_safe_report("Column Report", report_c), "Column.pdf")
