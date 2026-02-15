import streamlit as st
import numpy as np
import ezdxf
import io

# 1. القالب الملكي (The Golden Vault)
st.set_page_config(page_title="Pelan Beast v68", layout="wide")
st.markdown("<style>.stApp{background-color:#0b1619;color:#fff}.card{background:rgba(20,45,45,0.95);border:2px solid #d4af37;border-radius:15px;padding:20px;margin-bottom:15px}.gold{color:#d4af37;font-weight:bold}</style>", unsafe_allow_html=True)

st.markdown("<div class='card' style='text-align:center;'><h1 style='color:#d4af37;'>🏗️ Pelan Diamond Shield v68</h1><p class='gold'>الموسوعة الشاملة (2026) | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. لوحة المدخلات (Sidebar)
with st.sidebar:
    st.header("⚙️ الإعدادات")
    category = st.selectbox("المجال:", ["الخرسانة المسلحة", "هندسة الخزانات", "التحليل الزلزالي"])
    method = st.radio("المنهجية:", ["Ultimate", "Elastic"])
    st.divider()
    B = st.number_input("العرض B (cm):", 20, 500, 30)
    H = st.number_input("الارتفاع H (cm):", 10, 500, 60)
    L = st.number_input("الطول L (m):", 1.0, 30.0, 5.0)
    Load = st.number_input("الحمل (kN):", 1.0, 100000.0, 100.0)
    phi = st.selectbox("القطر (mm):", [12, 14, 16, 18, 20, 25, 32], index=2)

# 3. محرك الحسابات الذكي (The Resilient Engine)
f_y, f_cu, area_bar = 420, 25, (np.pi * phi**2) / 4
results = {}
bbs_out = "Φ16"

# --- قسم الخرسانة (منفصل تماماً) ---
if category == "الخرسانة المسلحة":
    sub = st.sidebar.selectbox("العنصر:", ["جائز", "عمود", "أساس"])
    if sub == "جائز":
        M = (Load * L**2) / 8 if method == "Ultimate" else (Load * L**2) / 10
        As = (M * 10**6) / (0.87 * f_y * (H-5) * 10)
        n = max(2, int(np.ceil(As / area_bar)))
        results = {"العزم": f"{M:.1f} kNm", "الحديد": f"{n} T {phi}", "الكانات": "Φ10 @ 15cm"}
        bbs_out = f"{n} T {phi}"
    if sub == "عمود":
        As_req = (Load * 1000 - 0.35 * f_cu * (B * H * 100)) / (0.67 * f_y)
        n = max(4, int(np.ceil(max(As_req, 0.01*B*H*100) / area_bar)))
        results = {"الحمل": f"{Load} kN", "الحديد": f"{n} T {phi}"}
        bbs_out = f"{n} T {phi}"
    if sub == "أساس":
        n = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar)))
        results = {"القطاع": f"{B}x{H} cm", "الحديد": f"{n} T {phi} /m'"}
        bbs_out = f"{n} T {phi} /m'"

# --- قسم الخزانات (منفصل تماماً) ---
if category == "هندسة الخزانات":
    M_t = (10 * (H/100) * L**2) / 12
    n = max(7, int(np.ceil(((M_t * 10**6) / (0.87 * f_y * (H-5) * 10)) / area_bar)))
    results = {"عزم الجدار": f"{M_t:.1f} kNm", "تسليح الجدار": f"{n} T {phi} /m'"}
    bbs_out = f"{n} T {phi} /m'"

# --- قسم الزلازل (منفصل تماماً) ---
if category == "التحليل الزلزالي":
    V_b = 0.15 * Load
    results = {"قص القاعدة Vb": f"{V_b:.1f} kN", "معامل Z": "0.15"}
    bbs_out = "تسليح مقاوم للقص"

# 4. واجهة العرض (UI Layout)
c1, c2 = st.columns([1.2, 1])

with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 النتائج الإنشائية")
    for k, v in results.items():
        st.write(f"**{k}:** {v}")
    st.divider()
    if category == "الخرسانة المسلحة":
            elif category == "هندسة الخزانات":
            st.info("👨‍🏫 تصميم م. بيلان: تم التحقق من الكود 2026.")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🖋️ تفريد الحديد")
    st.markdown(f"<div style='border:2px dashed #d4af37;padding:25px;text-align:center;border-radius:15px;background:#132a2a'><h2 style='color:#50c878'>{bbs_out}</h2><p class='gold'>↑ سهم رفع التفريد ↑</p></div>", unsafe_allow_html=True)
    if st.button("🛠️ تصدير DXF 🚀"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_text(f"PELAN v68", dxfattribs={'height': 5}).set_placement((0, 0))
        buf = io.StringIO(); doc.write(buf)
        st.download_button("📥 تحميل المخطط", buf.getvalue(), "Pelan_Beast.dxf")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center;color:#d4af37'>Pelan Diamond Shield v68 | Final Secure Version</p>", unsafe_allow_html=True)
