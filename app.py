import streamlit as st
import numpy as np
import ezdxf
import io
from datetime import datetime

# بيانات الهوية
ST_NAME, ST_TEL = "بيلان مصطفى عبد الكريم", "0998449697"
ST_INFO = "المهندس المدني - دراسة وإشراف"

st.set_page_config(page_title="Pelan CAD Master v92", layout="wide")

# تصميم الواجهة
st.markdown(f"""
<style>
 .stApp {{ background-color: #0b1619; color: white; }}
 .report-card {{ background: white; color: black; padding: 20px; border-radius: 10px; direction: rtl; border-right: 12px solid #d4af37; }}
 .official-stamp {{ border: 3px double #d4af37; padding: 10px; width: 280px; text-align: center; background: #fff; color: #000; float: left; margin-top: 20px; }}
</style>
""", unsafe_allow_html=True)

# المدخلات
with st.sidebar:
    st.header("🏗️ تفاصيل التسليح")
    B = st.number_input("العرض B (cm):", 20, 100, 30)
    H = st.number_input("الارتفاع H (cm):", 20, 200, 60)
    st.subheader("حديد التسليح")
    n_bot = st.number_input("عدد القضبان السفلية:", 2, 10, 3)
    phi_bot = st.selectbox("قطر السفلي (mm):", [14, 16, 18, 20])
    n_top = st.number_input("عدد قضبان التعليق (علوي):", 2, 10, 2)
    phi_top = st.selectbox("قطر العلوي (mm):", [10, 12, 14])
    phi_stir = st.selectbox("قطر الكانات (mm):", [8, 10])

# محرك رسم الأوتوكاد المتطور
def draw_pro_cad(b_cm, h_cm, nb, pb, nt, pt, ps):
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    
    # تحويل لملم (Scale 1:10)
    w, h = b_cm * 10, h_cm * 10
    cv = 30 # Cover 3cm
    
    # 1. رسم الخرسانة (اللون الأبيض)
    msp.add_lwpolyline([(0,0), (w,0), (w,h), (0,h), (0,0)], dxfattribs={'color': 7})
    
    # 2. رسم الكانة (اللون الأخضر)
    msp.add_lwpolyline([(cv,cv), (w-cv,cv), (w-cv,h-cv), (cv,h-cv), (cv,cv)], dxfattribs={'color': 3})
    
    # 3. رسم الحديد السفلي (دوائر زرقاء)
    dist_b = (w - 2*cv - 20) / (nb - 1) if nb > 1 else 0
    for i in range(nb):
        x = cv + 10 + (i * dist_b)
        msp.add_circle((x, cv + 10), radius=pb/2, dxfattribs={'color': 5})
    
    # 4. رسم الحديد العلوي (دوائر زرقاء)
    dist_t = (w - 2*cv - 20) / (nt - 1) if nt > 1 else 0
    for i in range(nt):
        x = cv + 10 + (i * dist_t)
        msp.add_circle((x, h - cv - 10), radius=pt/2, dxfattribs={'color': 5})

    # 5. وضع الأسهم والتوصيف (Annotation)
    # سهم السفلي
    msp.add_line((w/2, cv), (w/2 + 50, -50), dxfattribs={'color': 1})
    msp.add_text(f"{nb} T {pb} (BOTTOM)", dxfattribs={'height': 15}).set_placement((w/2 + 55, -65))
    
    # سهم العلوي
    msp.add_line((w/2, h-cv), (w/2 + 50, h + 50), dxfattribs={'color': 1})
    msp.add_text(f"{nt} T {pt} (TOP)", dxfattribs={'height': 15}).set_placement((w/2 + 55, h + 55))

    # الختم داخل الأوتوكاد
    msp.add_text(f"ENG. {ST_NAME}", dxfattribs={'height': 20}).set_placement((0, h + 100))
    msp.add_text(f"TEL: {ST_TEL}", dxfattribs={'height': 15}).set_placement((0, h + 80))
    
    return doc

# العرض والنتائج
st.markdown(f"<h1 style='text-align:center;'>🏗️ Pelan Professional CAD Suite</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("<div class='report-card'>", unsafe_allow_html=True)
    st.subheader("📑 تفاصيل التسليح")
    st.write(f"🔹 **التسليح السفلي:** {n_bot} قضبان قطر {phi_bot} ملم")
    st.write(f"🔹 **حديد التعليق:** {n_top} قضبان قطر {phi_top} ملم")
    st.write(f"🔹 **الكانات:** Φ {phi_stir} كل 15 سم")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.subheader("🖋️ المخطط التفصيلي (Preview)")
    
    
    # الختم الرسمي
    st.markdown(f"""
    <div class='official-stamp'>
        <p style='margin:0; font-weight:bold;'>{ST_NAME}</p>
        <p style='margin:0; font-size:12px;'>{ST_INFO}</p>
        <p style='margin:5px 0; font-weight:bold; color:#d4af37;'>TEL: {ST_TEL}</p>
        <hr style='border:1px solid #d4af37; margin:5px;'>
        <p style='font-size:9px;'>تم التدقيق والختم إلكترونياً</p>
    </div>
    <div style='clear:both;'></div>
    """, unsafe_allow_html=True)

# التصدير
st.divider()
if st.button("🚀 إنشاء ملف AutoCAD (DXF) بفرش الحديد الكامل"):
    dxf_file = draw_pro_cad(B, H, n_bot, phi_bot, n_top, phi_top, phi_stir)
    buf = io.StringIO()
    dxf_file.write(buf)
    st.download_button("📥 تحميل المخطط النهائي", buf.getvalue(), "Pelan_Detailing.dxf")
