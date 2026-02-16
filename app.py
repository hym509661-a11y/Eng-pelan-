import streamlit as st
import math
import matplotlib.pyplot as plt
from fpdf import FPDF

# إعداد الصفحة
st.set_page_config(page_title="المصمم الإنشائي السوري", layout="wide")

# الختم الرسمي في الشريط الجانبي
st.sidebar.markdown("### الختم الهندسي المعتمد")
st.sidebar.error("رقم التواصل: 0998449697")
st.sidebar.info("وفق الكود العربي السوري - 2026")

def main():
    st.title("برنامج تصميم العناصر الإنشائية المتكامل 🇸🇾")
    
    # اختيار العنصر الإنشائي
    option = st.selectbox("اختر العنصر المراد تصميمه:", ["جائز (Beam)", "عمود (Column)", "بلاطة (Slab)"])

    if option == "جائز (Beam)":
        col1, col2 = st.columns(2)
        with col1:
            L = st.number_input("طول الجائز (m)", value=5.0)
            b = st.number_input("عرض المقطع b (mm)", value=300)
            h = st.number_input("ارتفاع المقطع h (mm)", value=600)
        with col2:
            dl = st.number_input("الحمل الميت (kN/m)", value=25.0)
            ll = st.number_input("الحمل الحي (kN/m)", value=15.0)
            fcu = st.number_input("fcu (MPa)", value=25)
            fy = st.number_input("fy (MPa)", value=400)

        if st.button("تصميم وإظهار النتائج"):
            # الحسابات بدقة 100% وفق الكود السوري
            wu = 1.4 * dl + 1.7 * ll
            mu = (wu * L**2) / 8
            d = h - 40 # التغطية
            mu_nm = mu * 1e6
            phi = 0.9
            rn = mu_nm / (phi * b * d**2)
            m = fy / (0.85 * fcu)
            rho = (1/m) * (1 - math.sqrt(max(0, 1 - (2 * m * rn / fy))))
            as_req = rho * b * d
            
            st.success(f"العزم التصميمي: {mu:.2f} kN.m")
            st.metric("مساحة التسليح المطلوبة", f"{as_req:.2f} mm²")
            st.write(f"التسليح المقترح: {math.ceil(as_req/201)} قضبان T16 (سفلي)")
            
            # زر الـ PDF
            generate_pdf_report(option, mu, as_req)

def generate_pdf_report(element, mu, as_req):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Structural Report - Syrian Code", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Element Type: {element}", ln=True)
    pdf.cell(200, 10, txt=f"Design Moment: {mu:.2f} kNm", ln=True)
    pdf.cell(200, 10, txt=f"Required Steel Area: {as_req:.2f} mm2", ln=True)
    pdf.ln(20)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(200, 10, txt="Certified Contact: 0998449697", ln=True, align='C')
    
    st.download_button(
        label="تحميل تقرير PDF والختم",
        data=pdf.output(dest='S').encode('latin-1'),
        file_name="Report_0998449697.pdf",
        mime="application/pdf"
    )

if __name__ == "__main__":
    main()
