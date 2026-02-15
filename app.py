import streamlit as st
import numpy as np
import ezdxf
import io

# 1. إعدادات الواجهة الملكية
st.set_page_config(page_title="Pelan Beast v71", layout="wide")
st.markdown("<style>.stApp{background-color:#0b1619;color:#fff}.card{background:#142d2d;border:2px solid #d4af37;border-radius:15px;padding:20px;margin-bottom:10px}.gold{color:#d4af37;font-weight:bold}</style>", unsafe_allow_html=True)
st.markdown("<div class='card' style='text-align:center;'><h1 style='color:#d4af37;'>🏗️ Pelan Engineering Suite v71</h1><p class='gold'>الموسوعة الشاملة | م. بيلان عبد الكريم | 2026</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.header("⚙️ Settings")
    mode = st.selectbox("المجال:", ["الخرسانة المسلحة", "هندسة الخزانات", "التحليل الزلزالي"])
    method = st.radio("المنهجية:", ["Ultimate", "Elastic"])
    B = st.number_input("العرض B (cm):", 20, 500, 30)
    H = st.number_input("الارتفاع H (cm):", 10, 500, 60)
    L = st.number_input("الطول L (m):", 1.0, 30.0, 5.0)
    Load = st.number_input("الحمل (kN):", 1.0, 100000.0, 100.0)
    phi = st.selectbox("القطر (mm):", [12, 14, 16, 18, 20, 25, 32], index=2)

# 3. محرك الحسابات (Simplified Logic for Mobile)
f_y, f_cu, area_bar = 420, 25, (np.pi * phi**2) / 4
res, steel_text = {}, "Φ16"

# -- معالجة الخرسانة --
if mode == "الخرسانة المسلحة":
    elem = st.sidebar.selectbox("العنصر:", ["جائز", "عمود", "أساس"])
    if elem == "جائز":
        M = (Load * L**2) / 8 if method == "Ultimate" else (Load * L**2) / 10
        As = (M * 10**6) / (0.87 * f_y * (H-5) * 10)
        n = max(2, int(np.ceil(As / area_bar)))
        res = {"العزم": f"{M:.1f} kNm", "التسليح": f"{n} T {phi}"}
        steel_text = f"{n} T {phi}"
    if elem == "عمود":
        As_req = (Load * 1000 - 0.35 * f_cu * (B * H * 100)) / (0.67 * f_y)
        n = max(4, int(np.ceil(max(As_req, 0.01*B*H*100) / area_bar)))
        res = {"الحمل": f"{Load} kN", "التسليح": f"{n} T {phi}"}
        steel_text = f"{n} T {phi}"
    if elem == "أساس":
        n = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar)))
        res = {"القطاع": f"{B}x{H} cm", "التسليح": f"{n} T {phi}/m'"}
        steel_text = f"{n} T {phi} /m'"

# -- معالجة الخزانات والزلازل --
if mode == "هندسة الخزانات":
    M_t = (10 * (H/100) * L**2) / 12
    n = max(7, int(np.ceil(((M_t * 10**6) / (0.87 * f_y * (H-5) * 10)) / area_bar)))
    res = {"عزم الجدار": f"{M_t:.1f} kNm", "تسليح الجدار": f"{n} T {phi}/m'"}
    steel_text = f"{n} T {phi} /m'"

if mode == "التحليل الزلزالي":
    V_b = 0.15 * Load
    res = {"قص القاعدة Vb": f"{V_b:.1f} kN", "الحالة": "آمن زلزالياً"}
    steel_text = "تسليح زلزالي"

# 4. العرض الفني (Visualizer)
c1, c2 = st.columns([1.2, 1])
with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 النتائج")
    for k, v in res.items():
        st.write(f"**{k}:** {v}")
    st.divider()
    if mode == "الخرسانة المسلحة":
        
    elif mode == "هندسة الخزانات":
        
    st.info("Design by Eng. Pelan | 2026")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🖋️ التفريد")
    st.markdown(f"<div style='border:2px dashed #d4af37;padding:25px;text-align:center;border-radius:15px;background:#132a2a'><h2 style='color:#50c878'>{steel_text}</h2></div>", unsafe_allow_html=True)
    if st.button("🛠️ Export DXF"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_text("PELAN v71", dxfattribs={'height': 5}).set_placement((0, 0))
        buf = io.StringIO(); doc.write(buf)
        st.download_button("📥 Download", buf.getvalue(), "Pelan.dxf")
    st.markdown("</div>", unsafe_allow_html=True)
