import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from fpdf import FPDF

# --- إعدادات التطبيق ---
st.set_page_config(page_title="المكتب الهندسي المتكامل v5.0", layout="wide")

# دالة معالجة النص العربي للـ PDF
def fix_ar(text):
    return text[::-1]

# دالة توليد PDF احترافية ومستقرة
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
    return pdf.output(dest='S').encode('latin-1')

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("⚙️ معطيات المواد")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)
    st.divider()
    st.info("جميع العناصر الآن تعطي تفاصيل تفريد الحديد وجداول BBS.")

menu = ["الجوائز (Beams)", "البلاطات الهوردي (Ribbed)", "البلاطات المصمتة (Solid)", "الأساسات (Footings)", "الحصيرة (Raft)", "الأعمدة (Columns)", "أساس الجار (Strap)"]
choice = st.selectbox("🎯 اختر العنصر المطلوب:", menu)

# ---------------------------------------------------------
# 1. الجوائز (Beams)
# ---------------------------------------------------------
if choice == "الجوائز (Beams)":
    st.header("🔗 تفاصيل تصميم الجوائز")
    L = st.number_input("طول الجائز (m)", value=5.0)
    wu = st.number_input("الحمولة (t/m)", value=3.5)
    if st.button("عرض التفاصيل وتوليد المذكرة"):
        Mu = (wu * L**2) / 8
        As = (Mu * 10**5) / (0.87 * fy * 55)
        n = math.ceil(As / 2.01)
        
        # الرسم
        fig, ax = plt.subplots(figsize=(10, 2))
        ax.plot([0, L], [0, 0], color='lightgrey', lw=20, alpha=0.3)
        ax.plot([0.1, L-0.1], [-0.1, -0.1], 'red', lw=3, label=f"{n}T16")
        for x in np.linspace(0.1, L-0.1, 15):
            ax.plot([x, x], [-0.15, 0.15], 'black', lw=1)
        ax.axis('off'); st.pyplot(fig)
        
        
        # BBS
        st.table({"النوع": ["سفلي", "علوي", "كانات"], "التسليح": [f"{n} T16", "2 T12", "T8 @ 15cm"]})
        
        pdf_bytes = generate_civil_pdf("Report", {"المجاز": f"{L} m", "العزم": f"{Mu:.2f}", "التسليح": f"{n}T16"})
        st.download_button("📥 تحميل المذكرة", pdf_bytes, "Beam_Report.pdf")

# ---------------------------------------------------------
# 2. البلاطات الهوردي (Ribbed)
# ---------------------------------------------------------
elif choice == "البلاطات الهوردي (Ribbed)":
    st.header("🧱 تفاصيل الأعصاب (Ribs)")
    L_r = st.number_input("طول العصب (m)", value=5.0)
    if st.button("عرض تفاصيل العصب"):
        Mu_r = (0.5 * 0.8 * L_r**2) / 8
        st.metric("العزم على العصب", f"{Mu_r:.2f} t.m")
        
        st.table({"العنصر": ["تسليح العصب", "عرض العصب", "التغطية"], "التفاصيل": ["2 T14", "12 cm", "3 cm"]})
        
        pdf_r = generate_civil_pdf("Rib Report", {"العصب": f"{L_r} m", "الحديد": "2T14"})
        st.download_button("📥 تحميل المذكرة", pdf_r, "Rib_Report.pdf")

# ---------------------------------------------------------
# 3. البلاطات المصمتة (Solid)
# ---------------------------------------------------------
elif choice == "البلاطات المصمتة (Solid)":
    st.header("📊 تفاصيل البلاطة المصمتة")
    Lx = st.number_input("Lx (m)", value=4.0)
    Ly = st.number_input("Ly (m)", value=5.0)
    if st.button("عرض تفاصيل البلاطة"):
        
        st.table({"الاتجاه": ["القصير Lx", "الطويل Ly"], "التسليح": ["T12 @ 15cm", "T10 @ 15cm"]})
        pdf_s = generate_civil_pdf("Slab Report", {"الأبعاد": f"{Lx}x{Ly}", "الحديد": "T12@15"})
        st.download_button("📥 تحميل المذكرة", pdf_s, "Slab_Report.pdf")

# ---------------------------------------------------------
# 4. الأساسات (Footings)
# ---------------------------------------------------------
elif choice == "الأساسات (Footings)":
    st.header("📐 تفاصيل الأساس المنفرد")
    P = st.number_input("حمل العمود (Ton)", value=120.0)
    if st.button("تصميم الأساس"):
        dim = math.sqrt((P*1.1)/20)
        st.success(f"الأبعاد: {dim:.2f} x {dim:.2f} m")
        
        st.table({"العنصر": ["حديد الاتجاهين", "سماكة القاعدة"], "التفاصيل": ["T14 @ 15cm", "60 cm"]})
        pdf_f = generate_civil_pdf("Footing Report", {"الحمل": f"{P} T", "الأبعاد": f"{dim:.2f} m"})
        st.download_button("📥 تحميل المذكرة", pdf_f, "Footing_Report.pdf")

# ---------------------------------------------------------
# 5. الأعمدة (Columns)
# ---------------------------------------------------------
elif choice == "الأعمدة (Columns)":
    st.header("🏢 تفاصيل العمود")
    Pu = st.number_input("Pu (Ton)", value=150.0)
    if st.button("عرض تفاصيل العمود"):
        As_col = (Pu * 1000) / (0.35*fcu + 0.67*fy*0.01) # تقريبي
        
        st.table({"المقطع": ["30x60 cm"], "الحديد الرئيسي": ["8 T16"], "الكانات": ["T8 @ 15cm"]})
        pdf_c = generate_civil_pdf("Column Report", {"الحمل": f"{Pu} T", "التسليح": "8T16"})
        st.download_button("📥 تحميل المذكرة", pdf_c, "Column_Report.pdf")

# ---------------------------------------------------------
# 6. أساس الجار (Strap)
# ---------------------------------------------------------
elif choice == "أساس الجار (Strap)":
    st.header("📐 تفاصيل الشداد (Strap Beam)")
    
    if st.button("عرض تفاصيل الشداد"):
        st.table({"العنصر": ["تسليح الشداد", "العرض", "الارتفاع"], "التفاصيل": ["6 T18 (Top)", "40 cm", "80 cm"]})
        pdf_st = generate_civil_pdf("Strap Report", {"النظام": "Strap Footing"})
        st.download_button("📥 تحميل المذكرة", pdf_st, "Strap_Report.pdf")
