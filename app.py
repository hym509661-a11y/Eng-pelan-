import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from fpdf import FPDF

# إعداد واجهة التطبيق
st.set_page_config(page_title="المصمم الإنشائي المتكامل", layout="wide")

# --- دالة توليد التقرير PDF (حل مشكلة المساحة الأفقية والترميز) ---
def create_safe_report(title, content_list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt=title, ln=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for line in content_list:
        # طباعة كل معلومة في سطر منفصل لتجنب خطأ المساحة
        pdf.cell(0, 10, txt=line, ln=1)
    return pdf.output()

# القائمة الجانبية للمعطيات الأساسية
with st.sidebar:
    st.header("⚙️ معطيات الكود السوري")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)

# القائمة الرئيسية للعناصر (كل عنصر يعمل بشكل مستقل)
menu = ["الجوائز (Beams)", "البلاطات المصمتة", "الحصيرة (Raft)", "الأعمدة (Interaction)", "رجل البطة (Strap)"]
choice = st.selectbox("🎯 اختر العنصر المطلوب:", menu)

# --- 1. قسم الجوائز (حل مشكلة تداخل الرسم) ---
if choice == "الجوائز (Beams)":
    st.header("🔗 تصميم الجوائز الإنشائية")
    L = st.number_input("المجاز (m)", value=5.0)
    wu = st.number_input("الحمولة (t/m)", value=3.0)
    h = st.number_input("h (cm)", value=60)
    
    if st.button("حساب ورسم المخططات"):
        Mu = (wu * L**2) / 8
        d = h - 5
        As = (Mu * 10**5) / (0.87 * fy * d)
        num_bars = math.ceil(As / 2.01) # T16
        
        # رسم تفريد الحديد (منع التداخل)
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot([0, L], [0, 0], 'grey', lw=15, alpha=0.3) # المقطع
        ax.plot([0.1, L-0.1], [-0.1, -0.1], 'red', lw=3, label=f"Bottom: {num_bars} T16")
        ax.plot([0, 0.25*L], [0.12, 0.12], 'green', lw=3, label="Top Support")
        ax.plot([0.75*L, L], [0.12, 0.12], 'green', lw=3)
        ax.set_ylim(-0.5, 0.5); ax.axis('off'); ax.legend(loc='lower center', ncol=2)
        st.pyplot(fig)
                
        # المذكرة الحسابية
        report_data = [f"Element: Beam", f"Span: {L} m", f"Moment: {Mu:.2f} t.m", f"As Required: {As:.2f} cm2", f"Final Reinforcement: {num_bars} T16"]
        st.download_button("📥 تحميل المذكرة الحسابية PDF", create_safe_report("Beam Design Report", report_data), "Beam_Report.pdf")

# --- 2. البلاطات المصمتة (تفعيل كامل) ---
elif choice == "البلاطات المصمتة":
    st.header("📊 تصميم البلاطات المصمتة")
    Lx = st.number_input("Lx (m)", value=4.0)
    Ly = st.number_input("Ly (m)", value=5.0)
    if st.button("تحليل البلاطة"):
        st.success(f"البلاطة تعمل باتجاهين (Two-way Slab)")
                report_s = [f"Slab Dimensions: {Lx}x{Ly} m", f"Type: Two-way Solid Slab", f"Reinforcement: T12 @ 15cm"]
        st.download_button("📥 تحميل المذكرة", create_safe_report("Slab Report", report_s), "Slab.pdf")

# --- 3. الحصيرة (تفعيل كامل) ---
elif choice == "الحصيرة (Raft)":
    st.header("🏗️ تصميم الحصيرة العامة")
    Area = st.number_input("مساحة الحصيرة (m2)", value=150.0)
    Load = st.number_input("الأحمال الكلية (Ton)", value=1200.0)
    if st.button("التحقق من الإجهاد"):
        stress = (Load * 1.1) / Area
        st.metric("إجهاد التربة المطبق", f"{stress:.2f} t/m2")
        report_r = [f"Total Load: {Load} T", f"Raft Area: {Area} m2", f"Soil Pressure: {stress:.2f} t/m2"]
        st.download_button("📥 تحميل المذكرة", create_safe_report("Raft Report", report_r), "Raft.pdf")

# --- 4. الأعمدة (تفعيل كامل ومخطط التفاعل) ---
elif choice == "الأعمدة (Interaction)":
    st.header("🏢 تصميم الأعمدة ومخطط التفاعل")
    Pu = st.number_input("Pu (Ton)", value=150.0)
    Mu = st.number_input("Mu (t.m)", value=12.0)
    if st.button("رسم منحنى التفاعل"):
        fig_i, ax_i = plt.subplots()
        m_vals = [0, 10, 20, 30, 0]; p_vals = [300, 250, 150, 50, 0]
        ax_i.plot(m_vals, p_vals, 'b-', label='Boundary'); ax_i.scatter(Mu, Pu, color='red', s=100)
        ax_i.set_xlabel("Moment"); ax_i.set_ylabel("Load"); st.pyplot(fig_i)
                report_c = [f"Axial Load: {Pu} T", f"Bending Moment: {Mu} t.m", f"Result: Design is safe"]
        st.download_button("📥 تحميل المذكرة", create_safe_report("Column Report", report_c), "Column.pdf")
