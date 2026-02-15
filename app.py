import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from fpdf import FPDF

# إعداد واجهة التطبيق
st.set_page_config(page_title="المصمم الإنشائي المتكامل", layout="wide")
st.title("🏗️ المكتب الهندسي الشامل (الكود السوري)")

# دالة توليد تقرير PDF احترافي (معدلة لتجنب أخطاء اللغة العربية)
def create_pdf(report_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Detailed Structural Design Report", ln=1, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=report_text)
    return pdf.output()

# القائمة الجانبية للمعطيات الأساسية
with st.sidebar:
    st.header("⚙️ معطيات المواد")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)

# فصل العناصر لضمان الدقة
menu = ["الجوائز البيتونية", "البلاطات المصمتة", "البلاطات الهوردي", "الأعمدة الشاملة", "الأساسات ورجل البطة"]
choice = st.selectbox("🎯 اختر العنصر المراد تصميمه بدقة:", menu)

# ---------------------------------------------------------
# 1. تصميم الجوائز (Beams)
# ---------------------------------------------------------
if choice == "الجوائز البيتونية":
    st.header("🔗 تصميم الجوائز (عزم + قص + تفريد)")
    c1, c2 = st.columns(2)
    with c1:
        L = st.number_input("طول الجائز L (m)", value=5.0)
        b = st.number_input("عرض الجائز b (cm)", value=30)
    with c2:
        h = st.number_input("ارتفاع الجائز h (cm)", value=60)
        wu = st.number_input("الحمولة التصميمية wu (t/m)", value=2.5)

    if st.button("تحليل وتصميم الجائز"):
        Mu = (wu * L**2) / 8
        Vu = (wu * L) / 2
        d = h - 3 # cover
        As = (Mu * 10**5) / (0.87 * fy * d)
        num_bars = math.ceil(As / (math.pi * 0.8**2)) # Default T16
        
        # الرسوم البيانية (عزم وقص وتفريد)
        x = np.linspace(0, L, 100)
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
        
        ax1.plot(x, (wu*x/2)*(L-x), 'b', lw=2)
        ax1.invert_yaxis()
        ax1.set_title(f"Moment Diagram (Max Mu = {Mu:.2f} t.m)")
        ax1.fill_between(x, (wu*x/2)*(L-x), color='blue', alpha=0.1)

        ax2.plot(x, wu*(L/2 - x), 'r', lw=2)
        ax2.set_title(f"Shear Diagram (Max Vu = {Vu:.2f} t)")
        
        ax3.plot([0, L], [0, 0], 'black', lw=10) # المقطع
        ax3.plot([0.05, L-0.05], [-0.15, -0.15], 'red', lw=3, label="Main Bottom") # سفلي
        ax3.plot([0, 0.2*L], [0.15, 0.15], 'green', lw=2, label="Top Support") # علوي
        ax3.plot([0.8*L, L], [0.15, 0.15], 'green', lw=2)
        ax3.set_title("Reinforcement: Bottom & Top Bars")
        ax3.legend()
        st.pyplot(fig)
        
        st.success(f"الحديد المطلوب: {As:.2f} cm² ({num_bars} T16)")

# ---------------------------------------------------------
# 2. تصميم الأعمدة (Columns)
# ---------------------------------------------------------
elif choice == "الأعمدة الشاملة":
    st.header("🏢 تصميم الأعمدة + مخطط التفاعل")
    c1, c2 = st.columns(2)
    with c1:
        Pu = st.number_input("الحمل Pu (Ton)", value=120.0)
        Mu_c = st.number_input("العزم Mu (t.m)", value=10.0)
    with c2:
        b_c = st.number_input("b (cm)", value=30)
        h_c = st.number_input("h (cm)", value=50)

    if st.button("رسم مخطط التفاعل"):
        fig_int, ax_int = plt.subplots()
        # منحنى افتراضي للمخطط
        m_curve = [0, 10, 20, 30, 15, 0]
        p_curve = [250, 230, 180, 80, 30, 0]
        ax_int.plot(m_curve, p_curve, 'b-', label='Capacity')
        ax_int.plot(Mu_c, Pu, 'ro', label='Design Point')
        ax_int.set_xlabel("Moment Mu")
        ax_int.set_ylabel("Load Pu")
        ax_int.legend()
        st.pyplot(fig_int)
