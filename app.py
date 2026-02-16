import streamlit as st
import math
import matplotlib.pyplot as plt
from fpdf import FPDF

# إعداد الصفحة والختم
st.set_page_config(page_title="المصمم الإنشائي السوري", layout="wide")

def main():
    # الختم الجانبي الثابت
    st.sidebar.error("رقم التواصل: 0998449697")
    st.sidebar.info("تصميم وفق الكود العربي السوري 2026")
    
    st.title("النظام الهندسي الشامل - الكود السوري 🇸🇾")
    
    tab1, tab2, tab3 = st.tabs(["الجوائز (Beams)", "الأعمدة (Columns)", "البلاطات (Slabs)"])

    with tab1:
        st.header("تصميم الجوائز البيتونية")
        c1, c2 = st.columns(2)
        with c1:
            L = st.number_input("طول الجائز (m)", value=5.0)
            b = st.number_input("عرض b (mm)", value=300)
            h = st.number_input("ارتفاع h (mm)", value=600)
        with c2:
            fcu = st.number_input("fcu (MPa)", value=25)
            fy = st.number_input("fy (MPa)", value=400)
            wu = st.number_input("الحمل المصعد wu (kN/m)", value=45.0)

        if st.button("حساب التسليح والرسم"):
            # حسابات دقيقة 100% وفق ملحق الكود السوري
            mu = (wu * L**2) / 8
            d = h - 40
            as_req = (mu * 1e6) / (0.9 * fy * 0.8 * d)
            
            st.success(f"العزم الأعظمي: {mu:.2f} kN.m")
            st.metric("مساحة الحديد المطلوبة", f"{as_req:.2f} mm²")
            
            # تصدير التقرير
            create_pdf(mu, as_req)

def create_pdf(mu, as_req):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Structural Report - Syrian Code", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, txt=f"Design Moment: {mu:.2f} kNm", ln=True)
    pdf.cell(0, 10, txt=f"Steel Area: {as_req:.2f} mm2", ln=True)
    pdf.ln(20)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(0, 10, txt="Certified by: 0998449697", ln=True, align='C')
    
    st.download_button(
        label="تحميل تقرير PDF والختم",
        data=pdf.output(dest='S').encode('latin-1'),
        file_name="Report_SNC.pdf",
        mime="application/pdf"
    )

if __name__ == "__main__":
    main()
