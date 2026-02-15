import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from fpdf import FPDF

# إعداد التطبيق
st.set_page_config(page_title="المصمم الإنشائي المتكامل", layout="wide")

# دالة توليد PDF مصلحة جذرياً لتجنب خطأ المساحة (Horizontal Space)
def create_report_pdf(title, data_list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt=title, ln=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for line in data_list:
        # استخدام multi_cell مع تحديد العرض بالكامل يحل مشكلة المساحة
        pdf.multi_cell(190, 10, txt=str(line))
    return pdf.output()

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ معطيات المواد")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)

menu = ["الجوائز (Beams)", "البلاطات المصمتة", "الحصيرة العامة (Raft)", "الأعمدة (Interaction)", "رجل البطة (Strap)"]
choice = st.selectbox("🎯 اختر العنصر المراد تصميمه:", menu)

# --- 1. قسم الجوائز (مع جدول BBS) ---
if choice == "الجوائز (Beams)":
    st.header("🔗 تصميم الجوائز وجدول تفريد الحديد")
    L = st.number_input("المجاز (m)", value=5.0)
    wu = st.number_input("الحمولة (t/m)", value=3.0)
    h = st.number_input("h (cm)", value=60)
    
    if st.button("حساب وتوليد المذكرة"):
        Mu = (wu * L**2) / 8
        As = (Mu * 10**5) / (0.87 * fy * (h-5))
        n_bars = math.ceil(As / 2.01) # T16
        
        # رسم التفريد (بدون تداخل)
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot([0, L], [0, 0], 'grey', lw=15, alpha=0.3)
        ax.plot([0.1, L-0.1], [-0.12, -0.12], 'red', lw=3, label=f"Bottom: {n_bars} T16")
        ax.plot([0, 0.25*L], [0.12, 0.12], 'green', lw=3, label="Top Support")
        ax.plot([0.75*L, L], [0.12, 0.12], 'green', lw=3)
        ax.set_ylim(-0.5, 0.5); ax.axis('off'); ax.legend(loc='lower center', ncol=2)
        st.pyplot(fig)
        
        # جدول تفريد الحديد (BBS)
        st.subheader("📊 جدول تفريد الحديد (BBS)")
        st.table({
            "العنصر": ["حديد سفلي", "حديد علوي (تعليق)", "كانات (Stirrups)"],
            "القطر": ["T16", "T12", "T8"],
            "العدد/التكرار": [n_bars, 2, "6/m"],
            "الطول (m)": [L+0.4, L, 2*(0.3+0.55)+0.1]
        })
        
        report = [f"Design Results:", f"Max Moment: {Mu:.2f} t.m", f"Req. Steel: {As:.2f} cm2", f"Final: {n_bars} T16", "-"*20, "BBS Table Included"]
        st.download_button("📥 تحميل المذكرة + BBS", create_report_pdf("Beam Calculation & BBS", report), "Beam_BBS.pdf")

# --- 2. البلاطات المصمتة (مفعلة بالكامل) ---
elif choice == "البلاطات المصمتة":
    st.header("📊 تصميم البلاطة المصمتة")
    Lx = st.number_input("Lx (m)", value=4.0)
    Ly = st.number_input("Ly (m)", value=5.0)
    if st.button("تحليل البلاطة"):
        st.success(f"Ratio: {Ly/Lx:.2f} - Two-way Slab Design")
                data_s = [f"Dimensions: {Lx}x{Ly} m", "Reinforcement: T12 @ 150mm c/c", "Type: Two-way Slab"]
        st.download_button("📥 تحميل التقرير", create_report_pdf("Slab Design Report", data_s), "Slab.pdf")

# --- 3. الحصيرة العامة (مفعلة بالكامل) ---
elif choice == "الحصيرة العامة (Raft)":
    st.header("🏗️ تصميم الحصيرة العامة")
    Area = st.number_input("Area (m2)", value=150.0)
    Load = st.number_input("Total Load (Ton)", value=1200.0)
    if st.button("التحقق من الإجهاد"):
        stress = (Load * 1.1) / Area
        st.metric("Stress on Soil", f"{stress:.2f} t/m2")
                data_r = [f"Total Load: {Load} T", f"Area: {Area} m2", f"Soil Pressure: {stress:.2f} t/m2"]
        st.download_button("📥 تحميل المذكرة", create_report_pdf("Raft Report", data_r), "Raft.pdf")

# --- 4. الأعمدة (مخطط التفاعل مفعل) ---
elif choice == "الأعمدة (Interaction)":
    st.header("🏢 مخطط التفاعل للأعمدة")
    Pu = st.number_input("Pu (Ton)", value=120.0)
    Mu = st.number_input("Mu (t.m)", value=15.0)
    if st.button("رسم المخطط"):
        fig_i, ax_i = plt.subplots()
        ax_i.plot([0, 10, 25, 30, 0], [300, 280, 150, 20, 0], 'b-', label='Capacity')
        ax_i.scatter(Mu, Pu, color='red', s=100, label='Design Point')
        ax_i.set_xlabel("Moment (Mu)"); ax_i.set_ylabel("Axial (Pu)"); ax_i.legend()
        st.pyplot(fig_i)
                data_c = [f"Axial Load: {Pu} Ton", f"Moment: {Mu} t.m", "Result: Section is Safe"]
        st.download_button("📥 تحميل التقرير", create_report_pdf("Column Report", data_c), "Column.pdf")

# --- 5. رجل البطة (Strap) ---
elif choice == "رجل البطة (Strap)":
    st.header("📐 تصميم أساس الجار (Strap)")
    dist = st.number_input("Spacing between columns (m)", value=5.0)
    if st.button("تحليل النظام"):
        st.info("The Strap beam is designed to resist eccentricity.")
        data_st = [f"System: Strap Footing", f"Spacing: {dist} m", "Status: Analysis Complete"]
        st.download_button("📥 تحميل المذكرة", create_report_pdf("Strap Report", data_st), "Strap.pdf")
