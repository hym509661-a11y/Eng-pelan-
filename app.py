import streamlit as st
import numpy as np
import ezdxf
import io
from datetime import datetime

# 1. إعدادات الهوية البصرية الفاخرة
ST_NAME = "بيلان مصطفى عبد الكريم"
ST_JOB = "المهندس المدني"
ST_WORK = "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Pro v84", layout="wide")

# CSS لتصميم الواجهة السوداء والذهبية والمذكرة البيضاء
st.markdown(f"""
<style>
    .stApp {{ background-color: #0b1619; color: white; }}
    .main-container {{ background: white; color: #1a1a1a; padding: 30px; border-radius: 5px; direction: rtl; border-right: 12px solid #d4af37; }}
    .blueprint-area {{ background: #1a1c23; border: 2px solid #333; padding: 20px; border-radius: 10px; text-align: center; color: #50c878; margin: 20px 0; }}
    .gold-stamp {{ border: 3px double #d4af37; padding: 15px; width: 300px; text-align: center; background: #fff; color: #000; float: left; margin-top: 30px; box-shadow: 5px 5px 15px rgba(0,0,0,0.1); }}
    .calc-row {{ display: flex; justify-content: space-between; border-bottom: 1px solid #eee; padding: 10px 0; }}
    .gold-btn {{ background: linear-gradient(to bottom, #d4af37, #b8860b); color: black !important; font-weight: bold; border-radius: 5px; }}
</style>
""", unsafe_allow_html=True)

# 2. لوحة التحكم الجانبية (Inputs)
with st.sidebar:
    st.markdown("<h2 style='color:#d4af37;'>Project Inputs</h2>", unsafe_allow_html=True)
    p_name = st.text_input("اسم المشروع:", "مشروع بيلان الهندسي")
    category = st.selectbox("العنصر الإنشائي:", ["الجوائز (Beams)", "البلاطات (Slabs)", "الأساسات (Footings)", "الخزانات (Tanks)"])
    st.divider()
    B = st.number_input("العرض B (cm):", 20, 500, 30)
    H = st.number_input("الارتفاع H (cm):", 10, 500, 60)
    L = st.number_input("الطول L (m):", 1.0, 50.0, 5.0)
    Load = st.number_input("الحمل (kN):", 1.0, 100000.0, 125.0)
    phi = st.selectbox("القطر (mm):", [12, 14, 16, 18, 20, 25], index=2)

# 3. محرك الحسابات
fy, fcu = 420, 25
area_bar = (np.pi * phi**2) / 4
res = []
detailing = ""

if "الجوائز" in category:
    M = (Load * L**2) / 8
    As = (M * 1e6) / (0.87 * fy * (H-5) * 10)
    n = max(2, int(np.ceil(As / area_bar)))
    res = [("العزم التصميمي", f"{M:.1f} kNm"), ("التسليح الرئيسي", f"{n} T {phi}")]
    detailing = f"{n} T {phi}"
    img_tag = ""

elif "البلاطات" in category:
    M = (Load * L**2) / 10
    As = (M * 1e6) / (0.87 * fy * (H-3) * 10)
    n = max(5, int(np.ceil(As / area_bar)))
    res = [("سماكة البلاطة", f"{H} cm"), ("تسليح المتر", f"{n} T {phi}/m")]
    detailing = f"{n} T {phi} / m'"
    img_tag = ""

elif "الأساسات" in category:
    stress = Load / (B * L / 10000)
    n = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar)))
    res = [("إجهاد التربة", f"{stress:.2f} kN/m²"), ("تسليح القاعدة", f"{n} T {phi}/m")]
    detailing = f"{n} T {phi} @ 15cm"
    img_tag = ""

else: # الخزانات
    Mt = (10 * (H/100) * L**2) / 12
    n = max(7, int(np.ceil(((Mt * 1e6) / (0.87 * fy * (H-5) * 10)) / area_bar)))
    res = [("عزم الجدار", f"{Mt:.1f} kNm"), ("تسليح الجدار", f"{n} T {phi}/m")]
    detailing = f"{n} T {phi} / m'"
    img_tag = ""

# 4. المذكرة الحسابية والمخطط (The Professional Layout)
st.markdown(f"<h1 style='text-align:center; color:#d4af37;'>🏗️ Pelan Pro Office - {p_name}</h1>", unsafe_allow_html=True)

st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.subheader("📝 المذكرة الحسابية الهندسية")
st.write(f"التاريخ: {datetime.now().strftime('%Y-%m-%d')}")
st.divider()

# عرض الحسابات
for label, val in res:
    st.markdown(f"<div class='calc-row'><span><b>{label}:</b></span><span style='color:#d4af37;'>{val}</span></div>", unsafe_allow_html=True)

st.markdown(f"<div style='background:#f8f9fa; padding:15px; border-radius:5px; margin-top:15px;'><b>نتيجة التسليح:</b> <span style='font-size:20px;'>{detailing}</span></div>", unsafe_allow_html=True)

# المخطط الإنشائي (Blueprint Master)
st.markdown("<div class='blueprint-area'>", unsafe_allow_html=True)
st.markdown(f"<h3>🖋️ المخطط الإنشائي التفصيلي (CAD Style)</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#3498db;'>العنصر: {category} | التسليح: {detailing}</p>", unsafe_allow_html=True)
st.markdown(img_tag, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# الختم الملكي الذهبي
st.markdown(f"""
<div class='gold-stamp'>
    <p style='margin:0; font-weight:bold;'>{ST_JOB}</p>
    <p style='color:#d4af37; font-size:20px; font-weight:bold; margin:5px 0;'>{ST_NAME}</p>
    <p style='margin:0; font-size:14px;'>{ST_WORK}</p>
    <hr style='border:1px solid #d4af37;'>
    <p style='font-size:10px;'>ختم الاعتماد الهندسي v84</p>
</div>
<div style='clear:both;'></div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# أزرار الإجراءات
st.divider()
if st.button("🚀 تصدير AutoCAD (DXF)", key="gold_btn"):
    doc = ezdxf.new(setup=True); msp = doc.modelspace()
    msp.add_text(f"ENG. PELAN - {category}", dxfattribs={'height': 5})
    buf = io.StringIO(); doc.write(buf)
    st.download_button("📥 تحميل ملف DXF", buf.getvalue(), "Pelan_Drawing.dxf")

st.markdown("<p style='text-align:center; color:#d4af37;'>Pelan Pro Office © 2026 - Verified</p>", unsafe_allow_html=True)
