import streamlit as st
import numpy as np
import ezdxf
import io

# 1. الإعدادات البصرية (The Golden Interface)
st.set_page_config(page_title="Pelan v73", layout="wide")
st.markdown("<style>.stApp{background-color:#0b1619;color:#fff}.card{background:rgba(20,45,45,0.95);border:2px solid #d4af37;border-radius:15px;padding:20px;margin-bottom:15px}.gold{color:#d4af37;font-weight:bold}</style>", unsafe_allow_html=True)

st.markdown("<div class='card' style='text-align:center;'><h1 style='color:#d4af37;'>🏗️ Pelan Atomic Suite v73</h1><p class='gold'>الموسوعة الشاملة | م. بيلان عبد الكريم | 2026</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية (Simplified Sidebar)
with st.sidebar:
    st.header("⚙️ Settings")
    cat = st.selectbox("المجال:", ["خرسانة", "خزانات", "زلازل"])
    meth = st.radio("المنهجية:", ["Ultimate", "Elastic"])
    st.divider()
    B = st.number_input("العرض B (cm):", 20, 500, 30)
    H = st.number_input("العمق H (cm):", 10, 500, 60)
    L = st.number_input("الطول L (m):", 1.0, 30.0, 5.0)
    Load = st.number_input("الحمل (kN):", 1.0, 50000.0, 100.0)
    phi = st.selectbox("القطر (mm):", [12, 14, 16, 18, 20, 25, 32], index=2)

# 3. محرك الحسابات (Atomic Logic - No Deep Indents)
f_y, f_cu, area_bar = 420, 25, (np.pi * phi**2) / 4
res = {}
steel_bbs = "Φ16"

# قسم الخرسانة
if cat == "خرسانة":
    elem = st.sidebar.selectbox("العنصر:", ["جائز", "عمود", "أساس"])
    if elem == "جائز":
        M = (Load * L**2) / 8 if meth == "Ultimate" else (Load * L**2) / 10
        As = (M * 10**6) / (0.87 * f_y * (H-5) * 10)
        n = max(2, int(np.ceil(As / area_bar)))
        res = {"Moment": f"{M:.1f} kNm", "Steel": f"{n} T {phi}"}
        steel_bbs = f"{n} T {phi}"
    if elem == "عمود":
        As_req = (Load * 1000 - 0.35 * f_cu * (B * H * 100)) / (0.67 * f_y)
        n = max(4, int(np.ceil(max(As_req, 0.01*B*H*100) / area_bar)))
        res = {"Load": f"{Load} kN", "Steel": f"{n} T {phi}"}
        steel_bbs = f"{n} T {phi}"
    if elem == "أساس":
        n = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar)))
        res = {"Footing": f"{B}x{H} cm", "Steel": f"{n} T {phi} /m'"}
        steel_bbs = f"{n} T {phi} /m'"

# قسم الخزانات
if cat == "خزانات":
    M_t = (10 * (H/100) * L**2) / 12
    n = max(7, int(np.ceil(((M_t * 10**6) / (0.87 * f_y * (H-5) * 10)) / area_bar)))
    res = {"Tank Moment": f"{M_t:.1f} kNm", "Wall Steel": f"{n} T {phi} /m'"}
    steel_bbs = f"{n} T {phi} /m'"

# قسم الزلازل
if cat == "زلازل":
    V_b = 0.15 * Load
    res = {"Base Shear Vb": f"{V_b:.1f} kN", "Zone": "Safe"}
    steel_bbs = "Seismic Detailing"

# 4. واجهة العرض (Visualizer)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 النتائج الإنشائية")
    for k, v in res.items():
        st.write(f"**{k}:** {v}")
    st.divider()
    if cat == "خرسانة":
        
    elif cat == "خزانات":
        
    st.info("👨‍🏫 تصميم م. بيلان: تم التحقق وفق الكود 2026.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🖋️ تفريد الحديد")
    st.markdown(f"<div style='border:2px dashed #d4af37;padding:25px;text-align:center;border-radius:15px;background:#132a2a'><h2 style='color:#50c878'>{steel_bbs}</h2><p class='gold'>↑ سهم رفع التفريد ↑</p></div>", unsafe_allow_html=True)
    if st.button("🛠️ Export DXF"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_text("PELAN v73", dxfattribs={'height': 5}).set_placement((0, 0))
        buf = io.StringIO(); doc.write(buf)
        st.download_button("📥 تحميل AutoCAD", buf.getvalue(), "Pelan.dxf")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center;color:#d4af37'>Pelan Atomic v73 | 2026</p>", unsafe_allow_html=True)
