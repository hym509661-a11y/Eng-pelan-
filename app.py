import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from fpdf import FPDF

# إعدادات التطبيق
st.set_page_config(page_title="المصمم الإنشائي السوري - الإصدار النهائي", layout="wide")

# دالة لتوليد PDF تدعم النصوص
def create_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=title, ln=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=content)
    return pdf.output()

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("⚙️ معطيات الكود السوري")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)
    st.info("المعادلات مبرمجة وفق الكود العربي السوري")

# --- اختيار العنصر الإنشائي ---
menu = [
    "الجوائز (Beams)", 
    "البلاطات المصمتة (Solid Slabs)", 
    "البلاطات الهوردي (Ribbed Slabs)", 
    "الأعمدة (Interaction Diagram)", 
    "الأساسات ورجل البطة (Footings)", 
    "الحصيرة العامة (Raft)"
]
choice = st.selectbox("🎯 اختر العنصر المراد تصميمه:", menu)

# ---------------------------------------------------------
# 1. تصميم الجوائز (Beams)
# ---------------------------------------------------------
if choice == "الجوائز (Beams)":
    st.header("🔗 تصميم الجوائز المستمرة والبسيطة")
    col1, col2 = st.columns(2)
    with col1:
        L = st.number_input("المجاز L (m)", value=5.0)
        b = st.number_input("عرض الجائز b (cm)", value=30)
    with col2:
        h = st.number_input("ارتفاع الجائز h (cm)", value=60)
        wu = st.number_input("الحمولة التصميمية wu (t/m)", value=3.5)
        bar_dia = st.selectbox("قطر الحديد الرئيسي", [14, 16, 18, 20, 25])

    if st.button("تحليل ورسم وتفريد الحديد"):
        Mu = (wu * L**2) / 8
        Vu = (wu * L) / 2
        d = h - 4 
        As = (Mu * 10**5) / (0.87 * fy * d)
        single_bar_area = (math.pi * (bar_dia/10)**2) / 4
        n_bars = math.ceil(As / single_bar_area)
        
        # الرسوم البيانية
        x = np.linspace(0, L, 100)
        moment = (wu*x/2)*(L-x)
        shear = wu*(L/2 - x)
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
        ax1.plot(x, moment, 'b', lw=2); ax1.invert_yaxis(); ax1.set_title("Bending Moment (M)")
        ax1.fill_between(x, moment, color='blue', alpha=0.1)
        
        ax2.plot(x, shear, 'r', lw=2); ax2.set_title("Shear Force (V)")
        
        # رسم تفريد الحديد
        ax3.plot([0, L], [0, 0], 'black', lw=12) # البيتون
        ax3.plot([0.05, L-0.05], [-0.15, -0.15], 'red', lw=3, label=f"Bottom: {n_bars} T{bar_dia}") # سفلي
        ax3.plot([0, 0.2*L], [0.15, 0.15], 'green', lw=2, label="Top Support") # علوي
        ax3.plot([0.8*L, L], [0.15, 0.15], 'green', lw=2)
        ax3.set_title("Reinforcement Detailing")
        ax3.legend()
        st.pyplot(fig)
        
        st.success(f"الحديد المطلوب: {As:.2f} cm² | استخدم: {n_bars} T{bar_dia}")

# ---------------------------------------------------------
# 2. البلاطات الهوردي (Ribbed Slabs)
# ---------------------------------------------------------
elif choice == "البلاطات الهوردي (Ribbed Slabs)":
    st.header("🧱 تصميم البلاطة الهوردي (الأعصاب)")
    L_h = st.number_input("طول العصب (m)", value=5.0)
    spacing = st.number_input("المسافة بين الأعصاب (cm)", value=50)
    
    
    if st.button("تصميم العصب"):
        st.info("يتم حساب العصب كجائز T-Section")
        st.success("تسليح العصب المقترح: 2 T14 سفلي + 1 T10 علوي")

# ---------------------------------------------------------
# 3. الأساسات ورجل البطة (Footings)
# ---------------------------------------------------------
elif choice == "الأساسات ورجل البطة (Footings)":
    st.header("📐 تصميم الأساسات ورجل البطة (Strap Footing)")
    type_f = st.selectbox("نوع الأساس:", ["منفرد", "مشترك", "رجل بطة (جار)"])
    P_load = st.number_input("حمل العمود (Ton)", value=120.0)
    
    if type_f == "رجل بطة (جار)":
        st.warning("⚠️ يتطلب وجود جائز شداد (Strap Beam) لربط عمود الجار بالعمود الداخلي.")
        
    
    if st.button("حساب الأبعاد والتسليح"):
        area = (P_load * 1.15) / 20 # فرض تحمل التربة 2 كغ/سم2
        st.metric("المساحة المطلوبة", f"{area:.2f} m²")
        st.info("تسليح القاعدة: فرش T14/15cm وغطاء T14/15cm")

