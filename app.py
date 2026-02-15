import streamlit as st
import numpy as np
import ezdxf
import io
from datetime import datetime

# 1. الهوية المهنية المحدثة
ST_NAME = "بيلان مصطفى عبد الكريم"
ST_JOB = "المهندس المدني"
ST_WORK = "دراسة - إشراف - تعهدات"
ST_PHONE = "0998449697"

st.set_page_config(page_title="Pelan Office v87", layout="wide")
st.markdown(f"""
<style>
    .stApp {{ background-color: #0b1619; color: white; }}
    .main-report {{ background: white; color: black; padding: 25px; border-radius: 10px; direction: rtl; border-right: 12px solid #d4af37; }}
    .cad-preview {{ background: #1a1c23; border: 2px solid #444; padding: 20px; border-radius: 10px; color: #50c878; margin: 20px 0; text-align: center; }}
    .stamp-official {{ border: 3px double #d4af37; padding: 15px; width: 300px; text-align: center; background: #fff; color: #000; float: left; margin-top: 30px; box-shadow: 5px 5px 15px rgba(0,0,0,0.1); }}
    .calc-line {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; }}
</style>
""", unsafe_allow_html=True)

# 2. لوحة التحكم (Sidebar)
with st.sidebar:
    st.header("📂 إدارة التصميم")
    p_title = st.text_input("اسم المشروع:", "مشروع بيلان المتكامل")
    elem = st.selectbox("العنصر الإنشائي:", ["جائز (Beam)", "عمود (Column)", "أساس (Footing)"])
    B = st.number_input("العرض B (cm):", 20, 100, 30)
    H = st.number_input("الارتفاع H (cm):", 20, 200, 60)
    n_main = st.number_input("عدد القضبان الرئيسية:", 2, 24, 4)
    phi_main = st.selectbox("قطر الحديد (mm):", [12, 14, 16, 18, 20, 25], index=2)
    phi_stir = st.selectbox("قطر الكانة (mm):", [8, 10, 12], index=0)

# 3. محرك رسم AutoCAD التفصيلي
def generate_pro_dxf(b_cm, h_cm, n, p_m, p_s):
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    bw, bh = b_cm * 10, h_cm * 10
    c = 30 # Cover
    
    # رسم الخرسانة
    msp.add_lwpolyline([(0,0), (bw,0), (bw,bh), (0,bh), (0,0)], dxfattribs={'color': 7})
    # رسم الكانة
    msp.add_lwpolyline([(c,c), (bw-c,c), (bw-c,bh-c), (c,bh-c), (c,c)], dxfattribs={'color': 3})
    
    # رسم الحديد والأسهم
    bars_per_side = n // 2
    gap = (bw - 2*c - 20) / (bars_per_side - 1) if bars_per_side > 1 else 0
    
    for i in range(bars_per_side):
        x = c + 10 + (i * gap)
        # سفلي وعلوي
        msp.add_circle((x, c+10), radius=p_m/2, dxfattribs={'color': 5, 'layer': 'STEEL'})
        msp.add_circle((x, bh-c-10), radius=p_m/2, dxfattribs={'color': 5, 'layer': 'STEEL'})

    # إضافة توصيف الحديد بسهم
    msp.add_line((bw/2, c+10), (bw+100, -100), dxfattribs={'color': 1})
    msp.add_text(f"{n} T {p_m}", dxfattribs={'height': 15}).set_placement((bw+110, -110))
    
    # الختم داخل المخطط
    msp.add_text(f"DESIGNER: ENG. {ST_NAME.upper()}", dxfattribs={'height': 20}).set_placement((0, bh+50))
    msp.add_text(f"TEL: {ST_PHONE}", dxfattribs={'height': 15}).set_placement((0, bh+25))
    
    return doc

# 4. المذكرة الحسابية والختم المطور
st.markdown(f"<h1 style='text-align:center; color:#d4af37;'>🏗️ Pelan Professional Office v87</h1>", unsafe_allow_html=True)

st.markdown("<div class='main-report'>", unsafe_allow_html=True)
st.subheader("📑 المذكرة الحسابية الهندسية")
st.write(f"المشروع: {p_title} | التاريخ: {datetime.now().strftime('%Y-%m-%d')}")
st.divider()

st.markdown(f"<div class='calc-line'><b>العنصر المدروس:</b> <span>{elem}</span></div>", unsafe_allow_html=True)
st.markdown(f"<div class='calc-line'><b>الأبعاد الإنشائية:</b> <span>{B} x {H} cm</span></div>", unsafe_allow_html=True)
st.markdown(f"<div class='calc-line'><b>التسليح الرئيسي:</b> <span>{n_main} T {phi_main}</span></div>", unsafe_allow_html=True)
st.markdown(f"<div class='calc-line'><b>تسليح القص (الكانات):</b> <span>Φ {phi_stir} @ 15cm</span></div>", unsafe_allow_html=True)

# معاينة المخطط
st.markdown("<div class='cad-preview'>", unsafe_allow_html=True)
st.subheader("🖋️ معاينة تفاصيل الفرش وتفريد الحديد")
if "جائز" in elem:
    elif "أساس" in elem:
    else:
    st.markdown("</div>", unsafe_allow_html=True)

# الختم الجديد بالرقم
st.markdown(f"""
<div class='stamp-official'>
    <p style='margin:0; font-weight:bold;'>{ST_JOB}</p>
    <p style='color:#d4af37; font-size:19px; font-weight:bold; margin:5px 0;'>{ST_NAME}</p>
    <p style='margin:0; font-size:14px;'>{ST_WORK}</p>
    <p style='margin:5px 0; font-weight:bold; color:#1a1a1a;'>Tel: {ST_PHONE}</p>
    <hr style='border:1px solid #d4af37;'>
    <p style='font-size:10px;'>ختم الاعتماد الفني</p>
</div>
<div style='clear:both;'></div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 5. التصدير
st.divider()
if st.button("🚀 تصدير مخطط أوتوكاد التفصيلي المعتمد"):
    dxf = generate_pro_dxf(B, H, n_main, phi_main, phi_stir)
    buf = io.StringIO()
    dxf.write(buf)
    st.download_button("📥 تحميل ملف DXF (AutoCAD)", buf.getvalue(), "Pelan_Final_Drawing.dxf")

st.info("تم تحديث الختم وإضافة الرقم بنجاح. المذكرة جاهزة للطباعة.")
