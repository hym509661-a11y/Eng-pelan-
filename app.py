import streamlit as st
import pandas as pd
import numpy as np
import ezdxf
import io

# البيانات الشخصية للمهندس بيلان
NAME, TEL = "بيلان مصطفى عبد الكريم", "0998449697"
WORK_INFO = "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v107", layout="wide")

# تصميم الواجهة الراقية
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(135deg, #0f2027, #2c5364); color: white; }}
    .calc-card {{ background: white; color: black; padding: 25px; border-radius: 12px; direction: rtl; border-right: 12px solid #d4af37; }}
    .stamp-box {{ border: 4px double #d4af37; padding: 10px; width: 300px; text-align: center; background: white; color: black; float: left; margin-top: 20px; }}
</style>
""", unsafe_allow_html=True)

st.title("🏗️ المكتب الهندسي - الإصدار الاحترافي v107")

# المدخلات في القائمة الجانبية
with st.sidebar:
    st.header("📐 معايير التصميم")
    B = st.number_input("العرض B (cm):", 20, 100, 30)
    H = st.number_input("الارتفاع H (cm):", 20, 200, 60)
    L = st.number_input("البحر L (m):", 1.0, 20.0, 5.0)
    W = st.number_input("الحمل q (kN/m):", 1.0, 300.0, 50.0)
    phi_main = st.selectbox("قطر السفلي (mm):", [14, 16, 18, 20, 25], index=1)
    phi_stirrup = st.number_input("قطر الكانة (mm):", 8, 12, 8)
    spacing = st.number_input("تباعد الكانات (cm):", 10, 25, 15)

# الحسابات الإنشائية
mu = (W * L**2) / 8
vu = (W * L) / 2
as_req = (mu * 1e6) / (0.87 * 420 * (H-5) * 10)
n_bot = max(2, int(np.ceil(as_req / (np.pi * phi_main**2 / 4))))
n_top = 2  # حديد التعليق ثابت قضيبين

# العرض والنتائج
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
    st.subheader("📑 المذكرة الحسابية")
    st.write(f"📊 العزم التصميمي: {mu:.2f} kNm")
    st.write(f"📊 قوة القص: {vu:.2f} kN")
    st.divider()
    st.write(f"✅ **التسليح السفلي:** {n_bot} T {phi_main}")
    st.write(f"✅ **حديد التعليق (العلوي):** {n_top} T 12")
    st.write(f"✅ **الكانات:** T {phi_stirrup} @ {spacing} cm")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.subheader("📊 تصدير المخططات")
    
    # تصدير Excel
    try:
        df = pd.DataFrame({
            "Description": ["Beam Width", "Beam Height", "Span", "Max Moment", "Main Steel", "Hanger Steel", "Stirrups"],
            "Value": [f"{B} cm", f"{H} cm", f"{L} m", f"{mu:.2f} kNm", f"{n_bot} T {phi_main}", f"{n_top} T 12", f"T {phi_stirrup}@{spacing}cm"]
        })
        towrite = io.BytesIO()
        df.to_excel(towrite, index=False, engine='xlsxwriter')
        st.download_button("📥 تحميل المذكرة (Excel)", towrite.getvalue(), "Structural_Report.xlsx")
    except:
        st.error("⚠️ خطأ: يرجى إضافة xlsxwriter في ملف requirements.txt")

    # تصدير AutoCAD الشامل (الكانات + التعليق + السفلي)
    if st.button("🚀 توليد مخطط AutoCAD (DXF)"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        scale = 10 # تحويل لـ mm
        w_mm, h_mm, cv = B*scale, H*scale, 25 # التغطية 2.5 سم
        
        # 1. رسم الخرسانة (البرواز الخارجي)
        msp.add_lwpolyline([(0,0), (w_mm,0), (w_mm,h_mm), (0,h_mm), (0,0)], dxfattribs={'color': 7, 'lineweight': 30})
        
        # 2. رسم الكانة (المستطيل الداخلي)
        msp.add_lwpolyline([(cv,cv), (w_mm-cv,cv), (w_mm-cv,h_mm-cv), (cv,h_mm-cv), (cv,cv)], dxfattribs={'color': 3, 'lineweight': 15})
        
        # 3. رسم الحديد السفلي
        dx_b = (w_mm - 2*cv - 20) / (n_bot - 1 if n_bot > 1 else 1)
        for i in range(n_bot):
            msp.add_circle((cv + 10 + i*dx_b, cv + 10), radius=phi_main/2, dxfattribs={'color': 5})
        
        # 4. رسم حديد التعليق (العلوي)
        msp.add_circle((cv + 10, h_mm - cv - 10), radius=6, dxfattribs={'color': 5}) # يمين
        msp.add_circle((w_mm - cv - 10, h_mm - cv - 10), radius=6, dxfattribs={'color': 5}) # يسار
        
        # 5. كتابة البيانات
        msp.add_text(f"SECTION: {B}x{H} cm", dxfattribs={'height': 15}).set_placement((0, -30))
        msp.add_text(f"MAIN: {n_bot} T {phi_main}", dxfattribs={'height': 15}).set_placement((0, -55))
        msp.add_text(f"STIRRUPS: T{phi_stirrup} @ {spacing}", dxfattribs={'height': 15}).set_placement((0, -80))
        msp.add_text(f"ENG. {NAME}", dxfattribs={'height': 20}).set_placement((0, h_mm + 30))

        out_cad = io.StringIO()
        doc.write(out_cad)
        st.download_button("📥 تحميل الرسم الهندسي (DXF)", out_cad.getvalue(), "Beam_Final_Detail.dxf")

    # الختم
    st.markdown(f"""<div class='stamp-box'><p><b>المهندس المدني</b></p>
    <p style='color:#d4af37; font-size:20px;'><b>{NAME}</b></p>
    <p style='font-size:14px;'>{WORK_INFO}</p><b>{TEL}</b></div>""", unsafe_allow_html=True)

