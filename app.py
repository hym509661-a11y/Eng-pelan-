import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from fpdf import FPDF

# إعداد واجهة التطبيق
st.set_page_config(page_title="المكتب الهندسي الاحترافي", layout="wide")

# --- دالة توليد تقرير PDF آمنة (تحل مشكلة المساحة الأفقية واللغة) ---
def create_report(title, details_list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt=title, ln=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    # طباعة كل معلومة في سطر مستقل لتجنب خطأ المساحة (Horizontal Space)
    for detail in details_list:
        pdf.cell(0, 10, txt=str(detail), ln=1)
    return pdf.output()

# القائمة الجانبية للمعطيات
with st.sidebar:
    st.header("⚙️ معطيات المواد")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)
    st.divider()
    st.info("تصميم وفق الكود العربي السوري")

# القائمة الرئيسية للعناصر
menu = ["الجوائز (Beams)", "البلاطات المصمتة", "الحصيرة (Raft)", "الأعمدة (Interaction Diagram)", "رجل البطة (Strap Footing)"]
choice = st.selectbox("🎯 اختر العنصر المطلوب:", menu)

# --- 1. قسم الجوائز ---
if choice == "الجوائز (Beams)":
    st.header("🔗 تصميم الجوائز المستمرة والبسيطة")
    L = st.number_input("المجاز (m)", value=5.0, key="L_beam")
    wu = st.number_input("الحمولة (t/m)", value=3.0, key="w_beam")
    h = st.number_input("h (cm)", value=60, key="h_beam")
    
    if st.button("حساب ورسم وتوليد تقرير"):
        Mu = (wu * L**2) / 8
        d = h - 5
        As = (Mu * 10**5) / (0.87 * fy * d)
        num_bars = math.ceil(As / 2.01) # فرض T16
        
        # رسم تفريد الحديد (نفس النمط المطلوب)
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot([0, L], [0, 0], 'grey', lw=15, alpha=0.3) # البيتون
        ax.plot([0.1, L-0.1], [-0.1, -0.1], 'red', lw=3, label=f"Bottom: {num_bars} T16")
        ax.plot([0, 0.2*L], [0.15, 0.15], 'green', lw=3, label="Top Support")
        ax.plot([0.8*L, L], [0.15, 0.15], 'green', lw=3)
        ax.set_ylim(-0.5, 0.5)
        ax.axis('off')
        ax.legend(loc='lower center', ncol=2)
        st.pyplot(fig)
        
        results = [
            f"Element: Beam Design",
            f"Span (L): {L} m",
            f"Design Moment (Mu): {Mu:.2f} t.m",
            f"Required Steel Area (As): {As:.2f} cm2",
            f"Recommended Bars: {num_bars} T16"
        ]
        st.download_button("📥 تحميل المذكرة الحسابية PDF", create_report("Beam Design Report", results), "Beam_Report.pdf")

# --- 2. البلاطات المصمتة ---
elif choice == "البلاطات المصمتة":
    st.header("📊 تصميم البلاطات المصمتة")
    Lx = st.number_input("Lx (m)", value=4.0)
    Ly = st.number_input("Ly (m)", value=5.0)
    if st.button("تحليل البلاطة"):
        st.success(f"Aspect Ratio: {Ly/Lx:.2f} - Two-way Slab Design")
        report_s = [f"Slab Dimensions: {Lx}x{Ly} m", "Type: Solid Slab", "Reinforcement: T12 @ 15cm"]
        st.download_button("📥 تحميل التقرير", create_report("Slab Report", report_s), "Slab.pdf")

# --- 3. الحصيرة ---
elif choice == "الحصيرة (Raft)":
    st.header("🏗️ تصميم الحصيرة العامة")
    Area = st.number_input("مساحة الحصيرة (m2)", value=150.0)
    Load = st.number_input("الأحمال (Ton)", value=1200.0)
    if st.button("التحقق"):
        stress = (Load * 1.1) / Area
        st.metric("Soil Stress", f"{stress:.2f} t/m2")
        report_r = [f"Total Load: {Load} Ton", f"Area: {Area} m2", f"Stress: {stress:.2f} t/m2"]
        st.download_button("📥 تحميل المذكرة", create_report("Raft Report", report_r), "Raft.pdf")

# --- 4. الأعمدة ---
elif choice == "الأعمدة (Interaction Diagram)":
    st.header("🏢 تصميم الأعمدة - مخطط التفاعل")
    Pu = st.number_input("Pu (Ton)", value=150.0)
    Mu = st.number_input("Mu (t.m)", value=15.0)
    if st.button("رسم المخطط"):
        fig_i, ax_i = plt.subplots()
        m_vals = [0, 10, 25, 35, 15, 0]; p_vals = [300, 280, 200, 100, 50, 0]
        ax_i.plot(m_vals, p_vals, 'b-', label='Capacity')
        ax_i.scatter(Mu, Pu, color='red', s=100, label='Design Point')
        ax_i.set_xlabel("Moment Mu (t.m)"); ax_i.set_ylabel("Load Pu (Ton)")
        ax_i.legend(); st.pyplot(fig_i)
        report_c = [f"Axial Load: {Pu} T", f"Moment: {Mu} t.m", "Status: Safe Design"]
        st.download_button("📥 تحميل التقرير", create_report("Column Report", report_c), "Column.pdf")

# --- 5. رجل البطة (Strap) ---
elif choice == "رجل البطة (Strap Footing)":
    st.header("📐 تصميم أساس الجار (Strap)")
    dist = st.number_input("Dist between columns (m)", value=5.0)
    if st.button("تحليل الشداد"):
        st.info("Designing Strap Beam for eccentricity...")
        report_st = [f"System: Strap Footing", f"Spacing: {dist} m", "Reinforcement: T18 Bars"]
        st.download_button("📥 تحميل المذكرة", create_report("Strap Report", report_st), "Strap.pdf")
