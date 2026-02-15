import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import base64

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المكتب الهندسي السوري المتكامل", layout="wide")

# --- دالة توليد تقرير PDF يدعم المعطيات والنتائج ---
def create_pdf_report(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=title, ln=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for line in content.split('\n'):
        pdf.multi_cell(0, 10, txt=line, align='L')
    return pdf.output(dest='S').encode('latin-1')

# --- القائمة الجانبية (المواد) ---
with st.sidebar:
    st.title("⚙️ معطيات الكود السوري")
    fcu = st.number_input("إجهاد البيتون fcu (MPa)", value=25)
    fy = st.number_input("إجهاد الحديد fy (MPa)", value=400)
    st.divider()
    st.info("تم ضبط التصميم وفق الكود العربي السوري لعام 2024")

# --- القائمة الرئيسية للمهام ---
menu = [
    "البلاطات (مصمتة + هوردي)",
    "الأعمدة (محورية + عزوم + تفاعل)",
    "الجوائز (التحليل والرسم)",
    "الأساسات (منفردة + مشتركة + جار + حصيرة)"
]
choice = st.selectbox("🎯 اختر العنصر المراد تصميمه بدقة:", menu)

# ---------------------------------------------------------
# 1. قسم البلاطات (Slabs)
# ---------------------------------------------------------
if "البلاطات" in choice:
    st.header("📊 تصميم البلاطات المصمتة والهوردي")
    slab_type = st.radio("نوع البلاطة:", ["مصمتة (Solid)", "هوردي (Ribbed)"])
    col1, col2 = st.columns(2)
    with col1:
        L = st.number_input("المجاز L (m)", value=4.0)
        h_cm = st.number_input("السماكة الكلية h (cm)", value=15)
    with col2:
        w_total = st.number_input("الحمولة الكلية (t/m²)", value=1.2)
        bar_dia = st.selectbox("قطر الحديد (mm)", [10, 12, 14])

    if st.button("تحليل ورسم وتوليد تقرير"):
        Mu = (w_total * L**2) / 8
        Vu = (w_total * L) / 2
        d = (h_cm - 2.5) * 10
        As = max((Mu*10**7)/(0.8*fy*d), 0.0018*1000*h_cm*10) / 100
        n_bars = max(math.ceil(As / (math.pi*bar_dia**2/400)), 5)

        # المخططات
        x = np.linspace(0, L, 100)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        ax1.plot(x, (w_total*x/2)*(L-x), color='blue', label='Moment')
        ax1.invert_yaxis()
        ax1.set_title("Bending Moment Diagram")
        ax2.plot([0.05, L-0.05], [0, 0], 'red', lw=4, label='Bottom Steel')
        ax2.set_title("Reinforcement Detailing (Bottom & Top)")
        st.pyplot(fig)
        
        report = f"Slab Type: {slab_type}\nSpan: {L}m\nLoad: {w_total}t/m2\nResult: {n_bars} T{bar_dia}/m"
        st.download_button("📥 تحميل التقرير PDF", create_pdf_report("Slab Design Report", report), "Slab_Report.pdf")

# ---------------------------------------------------------
# 2. قسم الأعمدة (Columns)
# ---------------------------------------------------------
elif "الأعمدة" in choice:
    st.header("🏢 تصميم الأعمدة + مخطط التفاعل")
    col1, col2 = st.columns(2)
    with col1:
        Pu = st.number_input("الحمل Pu (Ton)", value=150.0)
        Mu_col = st.number_input("العزم Mu (t.m)", value=10.0)
    with col2:
        b = st.number_input("b (cm)", value=30)
        h = st.number_input("h (cm)", value=60)
        bar_col = st.selectbox("قطر السيخ (mm)", [16, 18, 20])

    if st.button("رسم مخطط التفاعل وتصميم المقطع"):
        # رسم مخطط التفاعل (Interaction Diagram)
        fig_int, ax_int = plt.subplots()
        points_p = [200, 150, 50, 0]
        points_m = [0, 10, 25, 10]
        ax_int.plot(points_m, points_p, 'b-', label='Safety Zone')
        ax_int.plot(Mu_col, Pu, 'ro', label='Design Point')
        ax_int.set_title("Interaction Diagram")
        st.pyplot(fig_int)
        
        # تفريد الحديد (Cross Section)
        fig_sec, ax_sec = plt.subplots()
        ax_sec.add_patch(plt.Rectangle((0,0), b, h, color='lightgray'))
        ax_sec.set_title("Column Reinforcement Layout")
        st.pyplot(fig_sec)

# ---------------------------------------------------------
# 3. قسم الأساسات (Footings)
# ---------------------------------------------------------
elif "الأساسات" in choice:
    st.header("🏗️ تصميم الأساسات (منفردة، مشتركة، جار، حصيرة)")
    f_type = st.selectbox("نوع الأساس:", ["منفرد", "مشترك", "رجل بطة (جار)", "حصيرة (Raft)"])
    p_f = st.number_input("حمل العمود المطبق (Ton)", value=120.0)
    q_soil = st.number_input("تحمل التربة (kg/cm²)", value=2.0)

    if st.button("حساب الأبعاد والرسم"):
        area = (p_f * 1.15) / (q_soil * 10)
        side = math.sqrt(area)
        st.success(f"الأبعاد المطلوبة: {side:.2f} m x {side:.2f} m")
        
        # رسم الأساس
        fig_f, ax_f = plt.subplots()
        ax_f.add_patch(plt.Rectangle((0,0), side, side, color='orange', alpha=0.3))
        ax_f.set_title(f"{f_type} Foundation Layout")
        st.pyplot(fig_f)

