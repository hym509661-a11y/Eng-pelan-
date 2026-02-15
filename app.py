import streamlit as st
import numpy as np
import ezdxf
import io
from datetime import datetime

# بيانات الهوية والختم
ST_NAME, ST_TEL = "بيلان مصطفى عبد الكريم", "0998449697"
ST_INFO = "المهندس المدني - دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Ultimate v93", layout="wide")
st.markdown(f"""
<style>
 .stApp {{ background-color: #0b1619; color: white; }}
 .report-card {{ background: white; color: black; padding: 25px; border-radius: 10px; direction: rtl; border-right: 12px solid #d4af37; }}
 .cad-preview {{ background: #111; border: 2px solid #444; padding: 20px; border-radius: 10px; color: #50c878; text-align: center; }}
 .stamp-official {{ border: 3px double #d4af37; padding: 10px; width: 300px; text-align: center; background: #fff; color: #000; float: left; margin-top: 25px; }}
</style>
""", unsafe_allow_html=True)

# 1. لوحة التحكم الجانبية (مدخلات شاملة)
with st.sidebar:
    st.header("⚙️ إعدادات العنصر الإنشائي")
    mode = st.selectbox("اختر العنصر:", ["جائز (Beam)", "بلاطة (Slab)", "أساس (Footing)", "عمود (Column)", "خزان (Tank)"])
    B = st.number_input("العرض B (cm):", 20, 500, 30)
    H = st.number_input("الارتفاع/السماكة H (cm):", 10, 500, 60)
    L = st.number_input("البحر/الطول L (m):", 1.0, 50.0, 5.0)
    
    st.subheader("تفاصيل التسليح")
    n_bot = st.number_input("عدد القضبان السفلية:", 2, 20, 4)
    phi_bot = st.selectbox("قطر السفلي (mm):", [12, 14, 16, 18, 20, 25], index=2)
    n_top = st.number_input("عدد قضبان التعليق/العلوي:", 2, 20, 2)
    phi_top = st.selectbox("قطر العلوي (mm):", [10, 12, 14, 16], index=1)
    phi_stir = st.selectbox("قطر الكانات (mm):", [8, 10, 12])

# 2. محرك رسم AutoCAD المطور لجميع العناصر
def create_cad_pro(mode, b, h, nb, pb, nt, pt, ps):
    doc = ezdxf.new(setup=True); msp = doc.modelspace()
    w, hi, cv = b*10, h*10, 30 # تحويل لملم وغطاء 3سم
    
    # رسم المقطع الخرساني والكانة
    msp.add_lwpolyline([(0,0), (w,0), (w,hi), (0,hi), (0,0)], dxfattribs={'color': 7})
    msp.add_lwpolyline([(cv,cv), (w-cv,cv), (w-cv,hi-cv), (cv,hi-cv), (cv,cv)], dxfattribs={'color': 3})
    
    # رسم الحديد السفلي وتوصيفه
    step_b = (w - 2*cv - 20) / (nb - 1) if nb > 1 else 0
    for i in range(nb):
        msp.add_circle((cv + 10 + i*step_b, cv + 10), radius=pb/2, dxfattribs={'color': 5})
    msp.add_line((w/2, cv), (w/2 + 40, -40), dxfattribs={'color': 1})
    msp.add_text(f"{nb} T {pb} (Main/Bottom)", dxfattribs={'height': 15}).set_placement((w/2 + 45, -55))
    
    # رسم الحديد العلوي وتوصيفه
    step_t = (w - 2*cv - 20) / (nt - 1) if nt > 1 else 0
    for i in range(nt):
        msp.add_circle((cv + 10 + i*step_t, hi - cv - 10), radius=pt/2, dxfattribs={'color': 5})
    msp.add_line((w/2, hi-cv), (w/2 + 40, hi + 40), dxfattribs={'color': 1})
    msp.add_text(f"{nt} T {pt} (Top/Hangers)", dxfattribs={'height': 15}).set_placement((w/2 + 45, hi + 45))

    # الختم داخل المخطط
    msp.add_text(f"ENG. {ST_NAME}", dxfattribs={'height': 20}).set_placement((0, hi + 100))
    msp.add_text(f"TEL: {ST_TEL}", dxfattribs={'height': 15}).set_placement((0, hi + 75))
    return doc

# 3. واجهة المذكرة الحسابية
st.markdown(f"<h1 style='text-align:center;'>🏗️ مكتب المهندس بيلان - النسخة الشاملة v93</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("<div class='report-card'>", unsafe_allow_html=True)
    st.subheader("📑 المذكرة الحسابية")
    st.write(f"**العنصر:** {mode}")
    st.write(f"**الأبعاد:** {B} x {H} cm | **الطول:** {L} m")
    st.divider()
    st.write(f"✅ **التسليح السفلي:** {n_bot} T {phi_bot}")
    st.write(f"✅ **التسليح العلوي:** {n_top} T {phi_top}")
    st.write(f"✅ **الكانات:** Φ {phi_stir} @ 15cm")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='cad-preview'>", unsafe_allow_html=True)
    st.subheader("🖋️ مخطط الفرش (Preview)")
    
    # عرض الصور التوضيحية بدقة
    if "جائز" in mode:
        
    elif "أساس" in mode:
        
    elif "عمود" in mode:
        
    elif "بلاطة" in mode:
        
    else:
        
        
    st.markdown("</div>", unsafe_allow_html=True)

    # الختم الرسمي النهائي بالرقم
    st.markdown(f"""
    <div class='stamp-official'>
        <p style='margin:0; font-weight:bold;'>المهندس المدني</p>
        <p style='color:#d4af37; font-size:20px; font-weight:bold; margin:5px 0;'>{ST_NAME}</p>
        <p style='margin:0; font-size:13px;'>{ST_INFO}</p>
        <p style='margin:5px 0; font-weight:bold; color:#1a1a1a;'>TEL: {ST_TEL}</p>
        <hr style='border:1px solid #d4af37; margin:8px;'>
        <p style='font-size:10px;'>ختم الاعتماد الهندسي v93</p>
    </div>
    <div style='clear:both;'></div>
    """, unsafe_allow_html=True)

# 4. التصدير
st.divider()
if st.button("🚀 تصدير المخطط التفصيلي الكامل لجميع الأنواع (DXF)"):
    dxf_doc = create_cad_pro(mode, B, H, n_bot, phi_bot, n_top, phi_top, phi_stir)
    buf = io.StringIO()
    dxf_doc.write(buf)
    st.download_button("📥 تحميل ملف AutoCAD", buf.getvalue(), f"Pelan_Project_{mode}.dxf")
