import streamlit as st
import numpy as np
import ezdxf
import io
from datetime import datetime

# 1. إعدادات الواجهة
st.set_page_config(page_title="Eng. Pelan Office", layout="wide")
st.markdown("<style>.stApp{background-color:#0b1619;color:#fff}.report-card{background:#fff;color:#000;padding:30px;border-radius:10px;direction:rtl;border-right:10px solid #d4af37}.stamp{border:3px double #d4af37;padding:10px;width:250px;text-align:center;margin-top:30px;background:#fff;color:#000;float:left}</style>", unsafe_allow_html=True)

# 2. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.header("⚙️ Settings")
    p_name = st.text_input("المشروع:", "فيلا سكنية")
    p_owner = st.text_input("المالك:", "م. بيلان")
    mode = st.selectbox("العنصر:", ["Beams", "Slabs", "Footing", "Tanks"])
    B = st.number_input("العرض B (cm):", 20, 500, 30)
    H = st.number_input("الارتفاع H (cm):", 10, 500, 60)
    L = st.number_input("الطول L (m):", 1.0, 50.0, 5.0)
    P = st.number_input("الحمل (kN):", 1.0, 100000.0, 150.0)
    phi = st.selectbox("القطر (mm):", [12, 14, 16, 18, 20, 25], index=2)

# 3. محرك الحسابات (Engine)
fy, fcu = 420, 25
area_bar = (np.pi * phi**2) / 4
res = []
bbs = ""

if mode == "Beams":
    M = (P * L**2) / 8
    As = (M * 1e6) / (0.87 * fy * (H-5) * 10)
    n = max(2, int(np.ceil(As / area_bar)))
    res = [("عزم الانعطاف", f"{M:.1f} kNm"), ("التسليح الرئيسي", f"{n} T {phi}")]
    bbs = f"{n} T {phi}"

if mode == "Slabs":
    M = (P * L**2) / 10
    As = (M * 1e6) / (0.87 * fy * (H-3) * 10)
    n = max(5, int(np.ceil(As / area_bar)))
    res = [("سماكة البلاطة", f"{H} cm"), ("تسليح المتر", f"{n} T {phi}/m")]
    bbs = f"{n} T {phi} / m'"

if mode == "Footing":
    stress = P / (B * L / 10000)
    n = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar)))
    res = [("إجهاد التربة", f"{stress:.2f} kN/m²"), ("تسليح القاعدة", f"{n} T {phi}/m")]
    bbs = f"{n} T {phi} @ 15cm"

if mode == "Tanks":
    Mt = (10 * (H/100) * L**2) / 12
    n = max(7, int(np.ceil(((Mt * 1e6) / (0.87 * fy * (H-5) * 10)) / area_bar)))
    res = [("عزم الجدار", f"{Mt:.1f} kNm"), ("تسليح الجدار", f"{n} T {phi}/m")]
    bbs = f"{n} T {phi} / m'"

# 4. المذكرة الهندسية والختم
st.markdown("<h1 style='text-align:center;'>🏗️ المذكرة الحسابية الهندسية</h1>", unsafe_allow_html=True)
st.markdown("<div class='report-card'>", unsafe_allow_html=True)
st.subheader(f"مشروع: {p_name} | المالك: {p_owner}")
st.write(f"تاريخ الإصدار: {datetime.now().strftime('%Y-%m-%d')}")
st.divider()

# عرض النتائج في جدول
for label, val in res:
    st.write(f"**{label}:** {val}")

st.markdown(f"<div style='background:#f0f0f0;padding:15px;border:1px dashed #d4af37;margin-top:10px;'><h3>التوصيف الإنشائي: {bbs}</h3></div>", unsafe_allow_html=True)

# الختم الرسمي
st.markdown(f"""
<div class='stamp'>
    <p><b>المهندس المدني</b></p>
    <p style='color:#d4af37;font-size:18px;'><b>بيلان مصطفى عبدالكريم</b></p>
    <p>دراسة - إشراف - تعهدات</p>
    <hr style='border:1px solid #d4af37;'>
    <p style='font-size:10px;'>ختم المكتب الهندسي المعتمد</p>
</div>
<div style='clear:both;'></div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# الصور التوضيحية
if mode == "Beams":
    
elif mode == "Slabs":
    
elif mode == "Footing":
    
elif mode == "Tanks":
    

# أزرار الإجراءات
st.divider()
if st.button("🚀 تصدير AutoCAD"):
    doc = ezdxf.new(setup=True); msp = doc.modelspace()
    msp.add_text(f"ENG. PELAN - {p_name}", dxfattribs={'height': 5})
    buf = io.StringIO(); doc.write(buf)
    st.download_button("📥 تحميل DXF", buf.getvalue(), "Project.dxf")
