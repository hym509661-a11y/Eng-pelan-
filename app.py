import streamlit as st
import pandas as pd
import numpy as np
import ezdxf
import io

# الهوية المهنية
NAME, TEL = "بيلان مصطفى عبد الكريم", "0998449697"
WORK = "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v108", layout="wide")

# تصميم الواجهة
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(135deg, #0f2027, #203a43); color: white; }}
    .calc-box {{ background: white; color: black; padding: 20px; border-radius: 10px; direction: rtl; border-right: 10px solid #d4af37; }}
    .stamp {{ border: 4px double #d4af37; padding: 10px; width: 280px; text-align: center; background: white; color: black; float: left; margin-top: 20px; }}
</style>
""", unsafe_allow_html=True)

st.title("🏗️ المكتب الهندسي - الإصدار v108 (الكامل)")

# المدخلات
with st.sidebar:
    st.header("⚙️ معطيات التصميم")
    b_cm = st.number_input("العرض B (cm):", 20, 100, 30)
    h_cm = st.number_input("الارتفاع H (cm):", 20, 200, 60)
    l_m = st.number_input("البحر L (m):", 1.0, 15.0, 5.0)
    w_kn = st.number_input("الحمل q (kN/m):", 1.0, 250.0, 50.0)
    phi_bot = st.selectbox("قطر السفلي (mm):", [14, 16, 18, 20], index=1)
    phi_st = st.number_input("قطر الكانة (mm):", 8, 12, 8)

# الحسابات
mu = (w_kn * l_m**2) / 8
vu = (w_kn * l_m) / 2
as_req = (mu * 1e6) / (0.87 * 420 * (h_cm-5) * 10)
n_bot = max(2, int(np.ceil(as_req / (np.pi * phi_bot**2 / 4))))
n_top = 2 # حديد التعليق ثابت

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("<div class='calc-box'>", unsafe_allow_html=True)
    st.subheader("📑 المذكرة الحسابية")
    st.write(f"**العزم:** {mu:.2f} kNm | **القص:** {vu:.2f} kN")
    st.divider()
    st.write(f"✅ **السفلي:** {n_bot} T {phi_bot}")
    st.write(f"✅ **العلوي (تعليق):** {n_top} T 12")
    st.write(f"✅ **الكانات:** T {phi_st} @ 15 cm")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.subheader("📊 تصدير المخططات")
    
    # تصدير Excel
    try:
        df = pd.DataFrame({
            "Description": ["Moment", "Shear", "Main Steel", "Hanger Steel", "Stirrups"],
            "Value": [f"{mu:.2f}", f"{vu:.2f}", f"{n_bot}T{phi_bot}", "2T12", f"T{phi_st}@15"]
        })
        towrite = io.BytesIO()
        df.to_excel(towrite, index=False, engine='xlsxwriter')
        st.download_button("📥 تحميل المذكرة (Excel)", towrite.getvalue(), "Structural_Report.xlsx")
    except:
        st.error("⚠️ يرجى إضافة xlsxwriter في ملف requirements.txt على GitHub")

    # تصدير AutoCAD (رسم كامل للكانات والتعليق)
    if st.button("🚀 توليد مخطط AutoCAD"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        s = 10 # scale to mm
        w_mm, h_mm, cv = b_cm*s, h_cm*s, 25 # cover 2.5cm
        
        # 1. رسم الخرسانة
        msp.add_lwpolyline([(0,0), (w_mm,0), (w_mm,h_mm), (0,h_mm), (0,0)], dxfattribs={'color': 7})
        # 2. رسم الكانة
        msp.add_lwpolyline([(cv,cv), (w_mm-cv,cv), (w_mm-cv,h_mm-cv), (cv,h_mm-cv), (cv,cv)], dxfattribs={'color': 1})
        # 3. رسم السفلي
        gap = (w_mm - 2*cv - 20) / (n_bot - 1 if n_bot > 1 else 1)
        for i in range(n_bot):
            msp.add_circle((cv + 10 + i*gap, cv + 10), radius=phi_bot/2, dxfattribs={'color': 5})
        # 4. رسم التعليق
        msp.add_circle((cv + 10, h_mm - cv - 10), radius=6, dxfattribs={'color': 5})
        msp.add_circle((w_mm - cv - 10, h_mm - cv - 10), radius=6, dxfattribs={'color': 5})
        
        msp.add_text(f"ENG. {NAME}", dxfattribs={'height': 20}).set_placement((0, h_mm + 40))
        
        out_cad = io.StringIO()
        doc.write(out_cad)
        st.download_button("📥 اضغط هنا لحفظ ملف الرسم (DXF)", out_cad.getvalue(), "Beam_Drawing.dxf")

    st.markdown(f"""<div class='stamp'><p><b>المهندس المدني</b></p>
    <p style='color:#d4af37; font-size:18px;'><b>{NAME}</b></p>
    <p>{WORK}</p><b>{TEL}</b></div>""", unsafe_allow_html=True)

# الرسوم التوضيحية لضمان الفهم
