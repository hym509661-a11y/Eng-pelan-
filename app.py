import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from fpdf import FPDF

# --- إعدادات التطبيق ---
st.set_page_config(page_title="المصمم الإنشائي الاحترافي", layout="wide")

# دالة معالجة النص العربي للـ PDF
def fix_ar(text):
    return text[::-1]

# دالة توليد PDF مستقرة
def generate_civil_pdf(title, data_dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt=title, ln=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for k, v in data_dict.items():
        line = f"{v} : {fix_ar(k)}"
        pdf.multi_cell(180, 10, txt=line, align='R')
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- القائمة الجانبية للمعطيات العامة ---
with st.sidebar:
    st.header("⚙️ المعطيات العامة")
    fcu = st.number_input("إجهاد الخرسانة fcu (MPa)", value=25)
    fy = st.number_input("إجهاد الحديد fy (MPa)", value=400)
    st.divider()
    st.info("قم بتغيير الأبعاد والأقطار من داخل كل قسم.")

menu = ["الجوائز (Beams)", "البلاطات الهوردي (Ribbed)", "البلاطات المصمتة (Solid)", "الأساسات (Footings)", "الأعمدة (Columns)"]
choice = st.selectbox("🎯 اختر العنصر المطلوب:", menu)

# ---------------------------------------------------------
# 1. الجوائز (Beams) - مرونة كاملة في الأبعاد والأقطار
# ---------------------------------------------------------
if choice == "الجوائز (Beams)":
    st.header("🔗 تفاصيل تصميم الجوائز")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        L = st.number_input("الطول L (m)", value=5.0)
        b = st.number_input("العرض b (cm)", value=25)
    with col2:
        h = st.number_input("الارتفاع h (cm)", value=60)
        wu = st.number_input("الحمولة wu (t/m)", value=3.5)
    with col3:
        bar_size = st.selectbox("قطر الحديد الرئيسي", [12, 14, 16, 18, 20, 25], index=2)
        stirrup_size = st.selectbox("قطر الكانات", [8, 10, 12], index=0)

    if st.button("تحديث الرسم والحسابات"):
        Mu = (wu * L**2) / 8
        As_req = (Mu * 10**5) / (0.87 * fy * (h-5))
        bar_area = (math.pi * (bar_size/10)**2) / 4
        n_bars = math.ceil(As_req / bar_area)
        
        # --- الرسم التوضيحي الذي أعجبك ---
        fig, ax = plt.subplots(figsize=(10, 3))
        # رسم جسم الجائز
        ax.plot([0, L], [0, 0], color='lightgrey', lw=40, alpha=0.3)
        # رسم الحديد السفلي (أحمر)
        ax.plot([0.05, L-0.05], [-0.15, -0.15], 'red', lw=4, label=f"Main: {n_bars} T{bar_size}")
        # رسم الحديد العلوي (أخضر)
        ax.plot([0, L], [0.15, 0.15], 'green', lw=2, label="Hangers: 2 T12")
        # رسم الكانات (توزيع)
        for x in np.linspace(0.1, L-0.1, 18):
            ax.plot([x, x], [-0.22, 0.22], 'black', lw=1.2)
        
        ax.set_ylim(-0.7, 0.7)
        ax.axis('off')
        ax.legend(loc='lower center', ncol=3)
        st.pyplot(fig)
        
        

        # --- جداول التفاصيل و BBS ---
        st.subheader("📊 جدول تفريد الحديد (BBS)")
        st.table({
            "العنصر": ["الحديد السفلي الرئيسي", "حديد التعليق العلوي", "الكانات (Stirrups)"],
            "القطر": [f"T{bar_size}", "T12", f"T{stirrup_size}"],
            "العدد": [n_bars, 2, f"{int(L/0.15)}/m"],
            "الطول (m)": [L+0.4, L, 2*(b+h-10)/100 + 0.1]
        })
        
        res_data = {"المجاز": f"{L} m", "العزم": f"{Mu:.2f} t.m", "التسليح": f"{n_bars} T{bar_size}"}
        pdf_bytes = generate_civil_pdf("Beam Design Report", res_data)
        st.download_button("📥 تحميل المذكرة الحسابية", pdf_bytes, "Beam_Report.pdf")

# ---------------------------------------------------------
# 2. البلاطات الهوردي (Ribbed)
# ---------------------------------------------------------
elif choice == "البلاطات الهوردي (Ribbed)":
    st.header("🧱 تصميم الأعصاب")
    col1, col2 = st.columns(2)
    with col1:
        L_r = st.number_input("طول العصب (m)", value=5.0)
        h_r = st.number_input("سمك البلاطة (cm)", value=30)
    with col2:
        r_bar = st.selectbox("قطر حديد العصب", [12, 14, 16], index=1)
        wu_r = st.number_input("الحمولة (t/m2)", value=0.8)

    if st.button("عرض تفاصيل العصب"):
        Mu_r = (wu_r * 0.5 * L_r**2) / 8
        st.metric("العزم على العصب الواحد", f"{Mu_r:.2f} t.m")
        
        
        
        st.table({
            "توصيف العصب": ["تسليح رئيسي", "حديد حراري (شبكة)", "عرض العصب"],
            "القيمة": [f"2 T{r_bar}", "T8 @ 20cm", "12 cm"]
        })
        
        pdf_r = generate_civil_pdf("Rib Report", {"العصب": f"{L_r} m", "الحديد": f"2T{r_bar}"})
        st.download_button("📥 تحميل المذكرة", pdf_r, "Rib_Report.pdf")

# ---------------------------------------------------------
# 3. الأساسات (Footings)
# ---------------------------------------------------------
elif choice == "الأساسات (Footings)":
    st.header("📐 تصميم الأساس المنفرد")
    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input("حمل العمود (Ton)", value=120.0)
        q_soil = st.number_input("تحمل التربة (kg/cm2)", value=2.0)
    with col2:
        f_bar = st.selectbox("قطر حديد القاعدة", [12, 14, 16, 18], index=1)
        f_thick = st.number_input("سمك القاعدة (cm)", value=60)

    if st.button("تصميم القاعدة"):
        area = (P * 1.1) / (q_soil * 10)
        side = math.sqrt(area)
        
        # رسم توضيحي للقاعدة
        fig2, ax2 = plt.subplots(figsize=(5, 5))
        ax2.add_patch(plt.Rectangle((0, 0), side, side, color='lightgrey', alpha=0.5))
        ax2.plot([0.1, side-0.1], [0.5, 0.5], 'r', lw=2)
        ax2.plot([0.5, 0.5], [0.1, side-0.1], 'r', lw=2)
        ax2.set_title(f"Plan: {side:.2f} x {side:.2f} m")
        ax2.axis('off')
        st.pyplot(fig2)
        
        
        
        st.table({
            "العنصر": ["الأبعاد", "التسليح (فرش/غطاء)", "السمك"],
            "التفاصيل": [f"{side:.2f} x {side:.2f} m", f"T{f_bar} @ 15cm", f"{f_thick} cm"]
        })
        
        pdf_f = generate_civil_pdf("Footing Report", {"الحمل": f"{P} T", "الأبعاد": f"{side:.2f} m"})
        st.download_button("📥 تحميل المذكرة", pdf_f, "Footing_Report.pdf")

# ---------------------------------------------------------
# 4. الأعمدة (Columns)
# ---------------------------------------------------------
elif choice == "الأعمدة (Columns)":
    st.header("🏢 تصميم العمود")
    col1, col2 = st.columns(2)
    with col1:
        Pu = st.number_input("الحمل Pu (Ton)", value=150.0)
        c_width = st.number_input("عرض العمود (cm)", value=30)
    with col2:
        c_depth = st.number_input("عمق العمود (cm)", value=60)
        c_bar = st.selectbox("قطر الحديد الرئيسي", [14, 16, 18, 20], index=1)

    if st.button("تحليل العمود"):
        
        st.table({
            "المقطع": [f"{c_width} x {c_depth} cm"],
            "التسليح المقترح": [f"8 T{c_bar}"],
            "الكانات": ["T8 @ 15cm"]
        })
        pdf_c = generate_civil_pdf("Column Report", {"الحمل": f"{Pu} T", "المقطع": f"{c_width}x{c_depth}"})
        st.download_button("📥 تحميل المذكرة", pdf_c, "Column_Report.pdf")
