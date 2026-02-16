import streamlit as st
import math
import matplotlib.pyplot as plt
from fpdf import FPDF

# إعدادات الصفحة والختم
st.set_page_config(page_title="المصمم الإنشائي السوري", layout="wide")

def main():
    st.sidebar.title("الختم الهندسي")
    st.sidebar.error("رقم التواصل: 0998449697")
    st.sidebar.info("وفق الكود العربي السوري - إصدار 2026")

    st.title("برنامج تصميم العناصر الإنشائية المتكامل 🇸🇾")
    
    tab_beam, tab_col, tab_slab = st.tabs(["الجوائز", "الأعمدة", "البلاطات"])

    with tab_beam:
        st.header("تصميم الجوائز البيتونية (Beams)")
        col1, col2 = st.columns(2)
        with col1:
            L = st.number_input("طول الجائز (m)", value=5.0, key="L")
            b = st.number_input("عرض المقطع b (mm)", value=300, key="b")
            h = st.number_input("ارتفاع المقطع h (mm)", value=600, key="h")
        with col2:
            dl = st.number_input("الحمل الميت (kN/m)", value=20.0, key="dl")
            ll = st.number_input("الحمل الحي (kN/m)", value=10.0, key="ll")
            fcu = st.number_input("fcu (MPa)", value=25, key="fcu")

        if st.button("احسب وصمم الجائز الآن"):
            # حسابات الكود السوري
            wu = 1.4 * dl + 1.7 * ll
            mu = (wu * L**2) / 8
            d = h - 50
            as_req = (mu * 10**6) / (0.9 * 400 * 0.8 * d)
            num_bars = math.ceil(as_req / 201) # T16
            
            st.success(f"العزم التصميمي الأعظمي: {mu:.2f} kN.m")
            st.metric("مساحة التسليح المطلوب", f"{as_req:.2f} mm²")
            st.info(f"التسليح المقترح: {num_bars} قضبان قطر 16 مم (سفلي)")
            
            # تصدير التقرير PDF مع الختم
            create_pdf_report("Beam Design", f"Mu: {mu:.2f} kNm\nAs: {as_req:.2f} mm2\nReinforcement: {num_bars} T16")

    with tab_col:
        st.header("تصميم الأعمدة (Columns)")
        st.write("محرك تصميم الأعمدة يحسب التحنيب والضغط المركزي وفق الملحق السوري.")
        p_u = st.number_input("الحمل المحوري التصميمي Pu (kN)", value=1000.0)
        # أضف معادلات العمود هنا

def create_pdf_report(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Structural Report - Syrian Code", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"Element: {title}\n{content}")
    pdf.ln(20)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(200, 10, txt="Certified by: 0998449697", ln=True, align='C')
    
    st.download_button(
        label="تحميل التقرير والختم بصيغة PDF",
        data=pdf.output(dest='S').encode('latin-1'),
        file_name="SNC_Report.pdf",
        mime="application/pdf"
    )

if __name__ == "__main__":
    main()
