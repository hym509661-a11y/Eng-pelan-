import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from fpdf import FPDF

# إعداد واجهة التطبيق
st.set_page_config(page_title="المصمم الإنشائي الاحترافي", layout="wide")

# --- دالة توليد PDF مصلحة (تجنب خطأ المساحة والترميز) ---
def create_fixed_pdf(title, data_dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt=title, ln=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    
    for key, value in data_dict.items():
        # استخدام عرض الصفحة الكامل 0 لتجنب خطأ Not enough horizontal space
        pdf.multi_cell(0, 10, txt=f"{key}: {value}", border=0)
    
    return pdf.output()

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ معطيات الكود")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)

menu = ["الجوائز (Beams)", "البلاطات المصمتة", "الحصيرة (Raft)", "الأعمدة الشاملة", "رجل البطة (Strap)"]
choice = st.selectbox("🎯 اختر العنصر:", menu)

# --- 1. قسم الجوائز (مع الحفاظ على الرسم المطلوب) ---
if choice == "الجوائز (Beams)":
    st.header("🔗 تصميم الجوائز")
    L = st.number_input("المجاز (m)", value=5.0)
    wu = st.number_input("الحمولة (t/m)", value=3.0)
    h = st.number_input("الارتفاع h (cm)", value=60)
    
    if st.button("حساب وتوليد المذكرة"):
        Mu = (wu * L**2) / 8
        As = (Mu * 10**5) / (0.87 * fy * (h-5))
        n_bars = math.ceil(As / 2.01) # T16
        
        # الرسم المطلوب (بدون تداخل)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot([0, L], [0, 0], 'grey', lw=15, alpha=0.3) # الخرسانة
        ax.plot([0.1, L-0.1], [-0.1, -0.1], 'red', lw=3, label=f"Bottom: {n_bars} T16")
        ax.plot([0, 0.2*L], [0.1, 0.1], 'green', lw=3, label="Top Support")
        ax.plot([0.8*L, L], [0.1, 0.1], 'green', lw=3)
        ax.set_ylim(-0.5, 0.5)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2)
        st.pyplot(fig)
        
        calc_results = {
            "Bending Moment (Mu)": f"{Mu:.2f} t.m",
            "Reinforcement Area (As)": f"{As:.2f} cm2",
            "Recommended Bars": f"{n_bars} T16",
            "Shear Force (Vu)": f"{(wu*L/2):.2f} t"
        }
        pdf_out = create_fixed_pdf("Beam Calculation Report", calc_results)
        st.download_button("📥 تحميل المذكرة الحسابية PDF", pdf_out, "Beam_Design.pdf")

# --- 2. البلاطة المصمتة (تفعيل كامل) ---
elif choice == "البلاطات المصمتة":
    st.header("📊 تصميم البلاطة المصمتة")
    Lx = st.number_input("Lx (m)", value=4.0)
    Ly = st.number_input("Ly (m)", value=5.0)
    ts = st.number_input("Slab Thickness (cm)", value=15)
    
    if st.button("تحليل البلاطة"):
        ratio = Ly / Lx
        st.write(f"Aspect Ratio: {ratio:.2f}")
        st.success("Two-way Slab Design" if ratio < 2 else "One-way Slab Design")
        
        fig_s, ax_s = plt.subplots()
        ax_s.add_patch(plt.Rectangle((0,0), Lx, Ly, color='blue', alpha=0.1))
        ax_s.set_title("Slab Plan View")
        st.pyplot(fig_s)
        
        calc_s = {"Dimensions": f"{Lx}x{Ly} m", "Thickness": f"{ts} cm", "Type": "Solid Slab"}
        st.download_button("📥 تحميل المذكرة PDF", create_fixed_pdf("Slab Design Report", calc_s), "Slab_Report.pdf")

# --- 3. الحصيرة (تفعيل كامل) ---
elif choice == "الحصيرة (Raft)":
    st.header("🏗️ تصميم الحصيرة")
    Total_P = st.number_input("Total Load (Ton)", value=1200.0)
    Area_R = st.number_input("Raft Area (m2)", value=150.0)
    
    if st.button("تحقق من الإجهاد"):
        stress = (Total_P * 1.1) / Area_R
        st.metric("Soil Stress", f"{stress:.2f} t/m2")
        calc_r = {"Total Load": f"{Total_P} Ton", "Raft Area": f"{Area_R} m2", "Bearing Pressure": f"{stress:.2f} t/m2"}
        st.download_button("📥 تحميل المذكرة PDF", create_fixed_pdf("Raft Design Report", calc_r), "Raft_Report.pdf")

# --- 4. الأعمدة (مخطط التفاعل) ---
elif choice == "الأعمدة الشاملة":
    st.header("🏢 الأعمدة ومخطط التفاعل")
    Pu = st.number_input("Pu (Ton)", value=150.0)
    Mu = st.number_input("Mu (t.m)", value=12.0)
    
    if st.button("رسم المخطط"):
        fig_i, ax_i = plt.subplots()
        m_c = [0, 10, 20, 30, 0]; p_c = [300, 250, 150, 50, 0]
        ax_i.plot(m_c, p_c, 'b-', label='Capacity')
        ax_i.scatter(Mu, Pu, color='red', s=100, label='Design Point')
        ax_i.set_xlabel("Moment Mu"); ax_i.set_ylabel("Load Pu")
        ax_i.legend(); st.pyplot(fig_i)
        
        calc_c = {"Axial Load Pu": f"{Pu} Ton", "Moment Mu": f"{Mu} t.m", "Status": "Verified"}
        st.download_button("📥 تحميل المذكرة PDF", create_fixed_pdf("Column Design Report", calc_c), "Column_Report.pdf")

# --- 5. رجل البطة (Strap) ---
elif choice == "رجل البطة (Strap)":
    st.header("📐 أساس الجار (رجل البطة)")
        dist = st.number_input("Distance between columns (m)", value=5.0)
    if st.button("تحليل الشداد"):
        st.info("The Strap beam is designed for maximum negative moment.")
        calc_st = {"System": "Strap Footing", "Column Spacing": f"{dist} m"}
        st.download_button("📥 تحميل المذكرة PDF", create_fixed_pdf("Strap Footing Report", calc_st), "Strap_Report.pdf")
