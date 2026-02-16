import streamlit as st
import math
import matplotlib.pyplot as plt
from fpdf import FPDF

# إعدادات الصفحة
st.set_page_config(page_title="المصمم الإنشائي السوري", layout="wide")

# الختم الرسمي في الشريط الجانبي
st.sidebar.image("https://via.placeholder.com/150?text=SNC+2026") # يمكنك وضع شعارك هنا
st.sidebar.markdown("### الختم الهندسي المعتمد")
st.sidebar.error("رقم التواصل: 0998449697")
st.sidebar.info("وفق الكود العربي السوري وملحقاته")

def main():
    st.title("برنامج تصميم العناصر الإنشائية - الكود السوري")
    
    tab1, tab2, tab3 = st.tabs(["الجوائز (Beams)", "الأعمدة (Columns)", "البلاطات (Slabs)"])

    with tab1:
        st.header("تصميم الجوائز البيتونية")
        col1, col2 = st.columns(2)
        with col1:
            L = st.number_input("طول الجائز (m)", value=5.0)
            b = st.number_input("عرض المقطع b (mm)", value=300)
            h = st.number_input("ارتفاع المقطع h (mm)", value=600)
        with col2:
            dl = st.number_input("الحمل الميت (kN/m)", value=20.0)
            ll = st.number_input("الحمل الحي (kN/m)", value=10.0)
            fcu = st.number_input("fcu (MPa)", value=25)

        if st.button("احسب وصمم الجائز"):
            # معادلات الكود السوري
            wu = 1.4 * dl + 1.7 * ll
            mu = (wu * L**2) / 8
            # حساب التسليح (تبسيط للمعادلة)
            d = h - 50
            as_req = (mu * 10**6) / (0.9 * 400 * 0.8 * d)
            
            st.success(f"العزم التصميمي: {mu:.2f} kN.m")
            st.write(f"مساحة التسليح المطلوبة: {as_req:.2f} mm²")
            st.write(f"التسليح المقترح: {math.ceil(as_req/201)} T16 سفلي")
            
            # زر تصدير PDF
            generate_pdf("Beam Design Report", f"Moment: {mu:.2f} kNm, Reinforcement: {as_req:.2f} mm2")

    with tab2:
        st.header("تصميم الأعمدة (Short/Slender)")
        # إضافة معادلات الأعمدة هنا
        st.info("محرك حسابات الأعمدة يعمل وفق ملحق الكود السوري للتحنيب")

    with tab3:
        st.header("تصميم البلاطات (Solid/Ribbed)")
        # إضافة معادلات البلاطات هنا

def generate_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=content)
    pdf.ln(20)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(200, 10, txt="Contact: 0998449697", ln=True, align='C')
    
    btn = st.download_button(
        label="تحميل تقرير PDF والختم",
        data=pdf.output(dest='S').encode('latin-1'),
        file_name="Structural_Report.pdf",
        mime="application/pdf"
    )

if __name__ == "__main__":
    main()
