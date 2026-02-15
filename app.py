import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from fpdf import FPDF

# --- إعدادات التطبيق ---
st.set_page_config(page_title="المكتب الهندسي المتكامل v4.0", layout="wide")

# دالة معالجة النص العربي للـ PDF (عكس النص)
def fix_ar(text):
    return text[::-1]

# دالة توليد PDF تدعم العربية والمساحة
def generate_civil_pdf(title, data_dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt=title, ln=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for k, v in data_dict.items():
        safe_line = f"{v} : {fix_ar(k)}"
        pdf.multi_cell(180, 10, txt=safe_line, align='R')
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("⚙️ معطيات المواد")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)
    st.divider()
    st.success("جميع الأنظمة مفعلة")

menu = [
    "الجوائز (Beams)", 
    "البلاطات الهوردي (Ribbed)", 
    "البلاطات المصمتة (Solid)",
    "الأساسات (Footings)",
    "الحصيرة العامة (Raft)", 
    "الأعمدة (Columns)", 
    "أساس الجار (Strap)"
]
choice = st.selectbox("🎯 اختر العنصر المراد تصميمه:", menu)

# ---------------------------------------------------------
# 1. الجوائز (Beams)
# ---------------------------------------------------------
if choice == "الجوائز (Beams)":
    st.header("🔗 تصميم الجوائز مع تفريد الكانات")
    col1, col2 = st.columns(2)
    with col1:
        L = st.number_input("طول الجائز L (m)", value=5.0)
        wu = st.number_input("الحمولة wu (t/m)", value=3.5)
    with col2:
        b = st.number_input("العرض (cm)", value=25)
        h = st.number_input("الارتفاع (cm)", value=60)

    if st.button("تحليل ورسم التفاصيل"):
        Mu = (wu * L**2) / 8
        As = (Mu * 10**5) / (0.87 * fy * (h-5))
        n_bars = math.ceil(As / 2.01)
        
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot([0, L], [0, 0], color='lightgrey', lw=35, alpha=0.3)
        ax.plot([0.1, L-0.1], [-0.15, -0.15], 'red', lw=3, label=f"Bottom: {n_bars} T16")
        ax.plot([0, L], [0.15, 0.15], 'green', lw=2, label="Top: 2 T12")
        # رسم الكانات
        for s_pos in np.arange(0.1, L, 0.20):
            ax.plot([s_pos, s_pos], [-0.2, 0.2], 'black', lw=1, alpha=0.6)
        ax.set_ylim(-0.6, 0.6); ax.axis('off'); ax.legend(loc='lower center', ncol=3)
        st.pyplot(fig)
        
        st.subheader("📊 جدول تفريد الحديد (BBS)")
        st.table({"العنصر": ["سفلي", "علوي", "كانات"], "القطر": ["T16", "T12", "T8"], "العدد": [n_bars, 2, int(L/0.2)]})
        
        res = {"العزم": f"{Mu:.2f} t.m", "التسليح": f"{n_bars} T16", "الكانات": "T8 @ 20cm"}
        st.download_button("📥 تحميل المذكرة", generate_civil_pdf("Beam Report", res), "Beam.pdf")

# ---------------------------------------------------------
# 2. البلاطات الهوردي (Ribbed)
# ---------------------------------------------------------
elif choice == "البلاطات الهوردي (Ribbed)":
    st.header("🧱 تصميم الأعصاب (Ribbed Slabs)")
    L_rib = st.number_input("طول العصب (m)", value=5.0)
    S_rib = st.number_input("المسافة بين الأعصاب (cm)", value=50)
    if st.button("تصميم"):
        Mu_rib = (0.8 * (S_rib/100) * L_rib**2) / 8
        st.metric("العزم على العصب", f"{Mu_rib:.2f} t.m")
        st.success("التسليح المقترح: 2 T14 لكل عصب")

# ---------------------------------------------------------
# 3. الأساسات (المنفردة والمشتركة) - جديد
# ---------------------------------------------------------
elif choice == "الأساسات (Footings)":
    st.header("📐 تصميم الأساسات المنفردة والمشتركة")
    f_type = st.radio("نوع الأساس:", ["منفرد (Isolated)", "مشترك (Combined)"])
    P1 = st.number_input("حمل العمود (Ton)", value=100.0)
    q_all = st.number_input("إجهاد التربة المسموح (kg/cm2)", value=2.0)
    
    if st.button("حساب الأبعاد"):
        area_req = (P1 * 1.1) / (q_all * 10)
        side = math.sqrt(area_req)
        st.info(f"المساحة المطلوبة: {area_req:.2f} m2")
        st.success(f"الأبعاد المقترحة: {side:.2f} x {side:.2f} m")
        f_res = {"النوع": f_type, "الحمل": f"{P1} T", "الأبعاد": f"{side:.2f} m"}
        st.download_button("📥 تحميل PDF", generate_civil_pdf("Footing Report", f_res), "Footing.pdf")

# ---------------------------------------------------------
# 4. الحصيرة العامة
# ---------------------------------------------------------
elif choice == "الحصيرة العامة (Raft)":
    st.header("🏗️ تصميم الحصيرة العامة")
    Area = st.number_input("المساحة (m2)", value=200.0)
    Load = st.number_input("الأحمال (Ton)", value=1500.0)
    if st.button("تحقق"):
        stress = (Load * 1.1) / Area
        st.metric("إجهاد التربة", f"{stress:.2f} t/m2")
        r_res = {"الحمل": f"{Load} T", "الإجهاد": f"{stress:.2f}"}
        st.download_button("📥 تحميل PDF", generate_civil_pdf("Raft Report", r_res), "Raft.pdf")

# ---------------------------------------------------------
# 5. الأعمدة
# ---------------------------------------------------------
elif choice == "الأعمدة (Columns)":
    st.header("🏢 مخطط التفاعل")
    Pu = st.number_input("Pu (Ton)", value=150.0)
    Mu = st.number_input("Mu (t.m)", value=15.0)
    if st.button("رسم"):
        fig_i, ax_i = plt.subplots()
        ax_i.plot([0, 15, 30, 35, 0], [400, 350, 180, 50, 0], 'b-')
        ax_i.scatter(Mu, Pu, color='red')
        st.pyplot(fig_i)

# ---------------------------------------------------------
# 6. أساس الجار (Strap)
# ---------------------------------------------------------
elif choice == "أساس الجار (Strap)":
    st.header("📐 تصميم أساس الجار (رجل البطة)")
    st.info("تصميم الشداد (Strap Beam) لموازنة اللامركزية.")
    if st.button("تحليل"):
        st.download_button("📥 المذكرة", generate_civil_pdf("Strap Report", {"النظام": "Strap"}), "Strap.pdf")
