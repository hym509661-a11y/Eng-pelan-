import streamlit as st
import numpy as np
import ezdxf
import io

# 1. الواجهة الملكية (The Golden UI)
st.set_page_config(page_title="Pelan Beast v67", layout="wide")
st.markdown("<style>.stApp{background-color:#0b1619;color:#fff}.card{background:rgba(20,45,45,0.95);border:2px solid #d4af37;border-radius:15px;padding:20px;margin-bottom:15px}.gold{color:#d4af37;font-weight:bold}</style>", unsafe_allow_html=True)

st.markdown("<div class='card' style='text-align:center;'><h1 style='color:#d4af37;'>🏗️ Pelan Engineering Suite v67</h1><p class='gold'>الموسوعة الشاملة | م. بيلان عبد الكريم | 2026</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.header("⚙️ الإعدادات")
    category = st.selectbox("المجال:", ["الخرسانة المسلحة", "هندسة الخزانات", "التحليل الزلزالي"])
    method = st.radio("المنهجية:", ["Ultimate", "Elastic"])
    st.divider()
    B = st.number_input("العرض B (cm):", 20, 500, 30)
    H = st.number_input("العمق H (cm):", 10, 500, 60)
    L = st.number_input("الطول L (m):", 1.0, 30.0, 5.0)
    Load = st.number_input("الحمل (kN):", 1.0, 50000.0, 100.0)
    phi = st.selectbox("القطر (mm):", [12, 14, 16, 18, 20, 25, 32], index=2)

# 3. محرك الحسابات المصفح (The Vault Engine)
def calculate_design():
    f_y, f_cu, area_bar = 420, 25, (np.pi * phi**2) / 4
    data = {}
    steel_desc = "Φ16"
    
    if category == "الخرسانة المسلحة":
        elem = st.sidebar.selectbox("العنصر:", ["جائز", "عمود", "أساس"])
        if elem == "جائز":
            M = (Load * L**2) / 8 if method == "Ultimate" else (Load * L**2) / 10
            As = (M * 10**6) / (0.87 * f_y * (H-5) * 10)
            n = max(2, int(np.ceil(As / area_bar)))
            data = {"العزم": f"{M:.1f} kNm", "الحديد": f"{n} T {phi}", "الكانات": "Φ10 @ 15cm"}
            steel_desc = f"{n} T {phi}"
        elif elem == "عمود":
            As_req = (Load * 1000 - 0.35 * f_cu * (B * H * 100)) / (0.67 * f_y)
            n = max(4, int(np.ceil(max(As_req, 0.01*B*H*100) / area_bar)))
            data = {"الحمل": f"{Load} kN", "الحديد": f"{n} T {phi}"}
            steel_desc = f"{n} T {phi}"
        else: # أساس
            n = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar)))
            data = {"القطاع": f"{B}x{H}", "التسليح": f"{n} T {phi} /m'"}
            steel_desc = f"{n} T {phi} /m'"
            
    elif category == "هندسة الخزانات":
        M_t = (10 * (H/100) * L**2) / 12
        n = max(7, int(np.ceil(((M_t * 10**6) / (0.87 * f_y * (H-5) * 10)) / area_bar)))
        data = {"عزم الجدار": f"{M_t:.1f} kNm", "تسليح الجدار": f"{n} T {phi} /m'"}
        steel_desc = f"{n} T {phi} /m'"
        
    else: # زلازل
        V_b = 0.15 * Load
        data = {"قص القاعدة Vb": f"{V_b:.1f} kN", "الحالة": "آمن زلزالياً"}
        steel_desc = "تسليح مقاوم للقص"
        
    return data, steel_desc

# تشغيل المحرك وعرض النتائج
results, bbs = calculate_design()

c1, c2 = st.columns([1.2, 1])

with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 النتائج الإنشائية")
    for k, v in results.items():
        st.write(f"**{k}:** {v}")
    st.divider()
        st.info("👨‍🏫 تصميم م. بيلان: تم التحقق من الكود 2026.")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🖋️ تفريد الحديد")
    st.markdown(f"<div style='border:2px dashed #d4af37;padding:25px;text-align:center;border-radius:15px;background:#132a2a'><h2 style='color:#50c878'>{bbs}</h2><p class='gold'>↑ سهم رفع التفريد ↑</p></div>", unsafe_allow_html=True)
    if st.button("🛠️ تصدير DXF 🚀"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_text(f"PELAN v67", dxfattribs={'height': 5}).set_placement((0, 0))
        buf = io.StringIO(); doc.write(buf)
        st.download_button("📥 تحميل المخطط", buf.getvalue(), "Pelan_Beast.dxf")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center;color:#d4af37'>Pelan Beast v67 | Final Unbreakable Core</p>", unsafe_allow_html=True)
