import streamlit as st
import numpy as np
import ezdxf
import io
from datetime import datetime

# 1. إعدادات الهوية (بيلان مصطفى عبد الكريم - 0998449697)
ST_NAME, ST_TEL = "بيلان مصطفى عبد الكريم", "0998449697"
ST_WORK = "المهندس المدني - دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v94", layout="wide")
st.markdown(f"""
<style>
 .stApp {{ background-color: #0b1619; color: white; }}
 .report-box {{ background: white; color: black; padding: 20px; border-radius: 10px; direction: rtl; border-right: 12px solid #d4af37; }}
 .cad-dark {{ background: #111; border: 2px solid #444; padding: 15px; border-radius: 8px; color: #50c878; text-align: center; }}
 .stamp-v94 {{ border: 4px double #d4af37; padding: 10px; width: 280px; text-align: center; background: #fff; color: #000; float: left; margin-top: 20px; }}
</style>
""", unsafe_allow_html=True)

# 2. لوحة التحكم (Sidebar)
with st.sidebar:
    st.header("⚙️ خيارات التصميم")
    mode = st.selectbox("نوع العنصر:", ["جائز (Beam)", "بلاطة (Slab)", "أساس (Footing)", "عمود (Column)", "خزان (Tank)"])
    B = st.number_input("العرض B (cm):", 20, 500, 30)
    H = st.number_input("الارتفاع H (cm):", 10, 500, 60)
    L = st.number_input("الطول L (m):", 1.0, 50.0, 5.0)
    st.divider()
    n_bot = st.number_input("عدد قضبان السفلي:", 2, 20, 4)
    phi_bot = st.selectbox("قطر السفلي (mm):", [12, 14, 16, 18, 20, 25], index=2)
    n_top = st.number_input("عدد قضبان العلوي:", 2, 20, 2)
    phi_top = st.selectbox("قطر العلوي (mm):", [10, 12, 14, 16], index=1)
    phi_stir = st.selectbox("قطر الكانة (mm):", [8, 10, 12])

# 3. محرك الرسم (AutoCAD Engine)
def build_dxf(m, b, h, nb, pb, nt, pt, ps):
    d = ezdxf.new(setup=True); msp = d.modelspace()
    w, hi, c = b*10, h*10, 30
    msp.add_lwpolyline([(0,0),(w,0),(w,hi),(0,hi),(0,0)], dxfattribs={'color': 7})
    msp.add_lwpolyline([(c,c),(w-c,c),(w-c,hi-c),(c,hi-c),(c,c)], dxfattribs={'color': 3})
    for i in range(nb):
        msp.add_circle((c+10+i*(w-2*c-20)/(nb-1 if nb>1 else 1), c+10), radius=pb/2, dxfattribs={'color': 5})
    for i in range(nt):
        msp.add_circle((c+10+i*(w-2*c-20)/(nt-1 if nt>1 else 1), hi-c-10), radius=pt/2, dxfattribs={'color': 5})
    msp.add_text(f"{nb}T{pb} Bottom", dxfattribs={'height': 15}).set_placement((w+20, 20))
    msp.add_text(f"{nt}T{pt} Top", dxfattribs={'height': 15}).set_placement((w+20, hi-20))
    msp.add_text(f"ENG. {ST_NAME} - {ST_TEL}", dxfattribs={'height': 20}).set_placement((0, hi+50))
    return d

# 4. واجهة العرض (Frontend)
st.markdown(f"<h1 style='text-align:center;'>🏢 Pelan Office v94 - {mode}</h1>", unsafe_allow_html=True)

c1, c2 = st.columns([1, 1.2])

with c1:
    st.markdown("<div class='report-box'>", unsafe_allow_html=True)
    st.subheader("📑 المذكرة الحسابية")
    st.write(f"**العنصر:** {mode} | **الأبعاد:** {B}x{H} cm")
    st.write(f"**تسليح السفلي (الفرش):** {n_bot} T {phi_bot}")
    st.write(f"**تسليح العلوي (التعليق):** {n_top} T {phi_top}")
    st.write(f"**الكانات:** Φ {phi_stir} @ 15cm")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='cad-dark'>", unsafe_allow_html=True)
    st.subheader("🖋️ مخطط تفريد الحديد")
    if "جائز" in mode:
        
    elif "أساس" in mode:
        
    elif "عمود" in mode:
        
    elif "بلاطة" in mode:
        
    else:
        
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""<div class='stamp-v94'><p><b>المهندس المدني</b></p><p style='color:#d4af37; font-size:18px; font-weight:bold;'>{ST_NAME}</p>
    <p style='font-size:12px;'>{ST_WORK}</p><p style='font-weight:bold;'>TEL: {ST_TEL}</p>
    <hr style='border:1px solid #d4af37;'><p style='font-size:10px;'>ختم الاعتماد الرسمي</p></div>""", unsafe_allow_html=True)

# 5. التصدير (AutoCAD)
st.divider()
if st.button("🚀 تصدير مخطط أوتوكاد التفصيلي"):
    dxf = build_dxf(mode, B, H, n_bot, phi_bot, n_top, phi_top, phi_stir)
    buf = io.StringIO(); dxf.write(buf)
    st.download_button("📥 تحميل ملف DXF", buf.getvalue(), f"Pelan_{mode}.dxf")
