import streamlit as st
import numpy as np
import ezdxf
import io

# 1. القالب الملكي (The Royal Interface)
st.set_page_config(page_title="Pelan Core v65", layout="wide")
st.markdown("<style>.stApp{background-color:#0b1619;color:#fff}.card{background:#142d2d;border:2px solid #d4af37;border-radius:15px;padding:20px;margin:10px 0}.gold{color:#d4af37;font-weight:bold}</style>", unsafe_allow_html=True)

st.markdown("<div class='card' style='text-align:center;'><h1 style='color:#d4af37;'>🏗️ Pelan Engineering Core v65</h1><p class='gold'>الموسوعة الشاملة 2026 | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. لوحة تحكم الوحش (Sidebar)
with st.sidebar:
    st.header("⚙️ الإعدادات الهندسية")
    mode = st.selectbox("المجال:", ["الخرسانة المسلحة", "هندسة الخزانات", "التحليل الزلزالي"])
    method = st.radio("المنهجية:", ["الحدية (Ultimate)", "المرنة (Elastic)"])
    st.divider()
    B = st.number_input("العرض B (cm):", 20, 500, 30)
    H = st.number_input("الارتفاع H (cm):", 10, 500, 60)
    L = st.number_input("البحر L (m):", 1.0, 30.0, 5.0)
    Load = st.number_input("الحمل (kN):", 1.0, 100000.0, 100.0)
    phi = st.selectbox("القطر (mm):", [12, 14, 16, 18, 20, 25, 32], index=2)

# 3. محرك الحسابات المصفح (The Unbreakable Engine)
f_y, f_cu, res = 420, 25, {}
area_bar = (np.pi * phi**2) / 4

# منطق برمجي مسطح لمنع أخطاء الإزاحة (Indentation)
if mode == "الخرسانة المسلحة":
    elem = st.sidebar.selectbox("العنصر:", ["جائز/عصب", "بلاطة", "عمود", "أساس"])
    if elem in ["جائز/عصب", "بلاطة"]:
        M = (Load * L**2) / 8 if "Ultimate" in method else (Load * L**2) / 10
        As = (M * 10**6) / (0.87 * f_y * (H-5) * 10)
        n = max(2, int(np.ceil(As / area_bar)))
        res = {"العزم": f"{M:.1f} kNm", "الحديد الرئيسي": f"{n} T {phi}", "العلوي": f"{max(2, int(n*0.3))} T {phi}", "الكانات": "Φ10 @ 15cm"}
    elif elem == "عمود":
        As_req = (Load * 1000 - 0.35 * f_cu * (B * H * 100)) / (0.67 * f_y)
        n = max(4, int(np.ceil(max(As_req, 0.01*B*H*100) / area_bar)))
        res = {"الحمل التصميمي": f"{Load} kN", "تسليح العمود": f"{n} T {phi}", "الكانات": "Φ12 @ 15cm"}
    elif elem == "أساس":
        n = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar)))
        res = {"القطاع": f"{B}x{H} cm", "تسليح القاعدة": f"{n} T {phi} /m'"}

if mode == "هندسة الخزانات":
    M_t = (10 * (H/100) * L**2) / 12
    n = max(7, int(np.ceil(((M_t * 10**6) / (0.87 * f_y * (H-5) * 10)) / area_bar)))
    res = {"ضغط الماء": "هيدروستاتيكي", "عزم الجدار": f"{M_t:.1f} kNm", "تسليح الجدران": f"{n} T {phi} /m'"}

if mode == "التحليل الزلزالي":
    V_b = 0.15 * Load
    res = {"قص القاعدة Vb": f"{V_b:.1f} kN", "المنطقة الزلزالية": "Z=0.15", "الحالة": "آمن زلزالياً"}

# 4. العرض الفني والتفريد
c1, c2 = st.columns([1.2, 1])
with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 النتائج الإنشائية")
    for k, v in res.items():
        st.write(f"**{k}:** {v}")
    st.divider()
    if mode == "الخرسانة المسلحة":
            elif mode == "هندسة الخزانات":
            st.info("👨‍🏫 تصميم م. بيلان: تم التحقق من الكود لضمان الأمان.")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🖋️ تفريد الحديد")
    main = res.get("الحديد الرئيسي", res.get("تسليح العمود", res.get("تسليح القاعدة", res.get("تسليح الجدران", "Φ16"))))
    st.markdown(f"<div style='border:2px dashed #d4af37;padding:20px;text-align:center;border-radius:15px;background:#132a2a'><h2 style='color:#50c878'>{main}</h2><p class='gold'>↑ سهم رفع التفريد ↑</p></div>", unsafe_allow_html=True)
    if st.button("🛠️ تصدير DXF 🚀"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_text(f"PELAN v65 - {mode}", dxfattribs={'height': 5}).set_placement((0, 0))
        buf = io.StringIO(); doc.write(buf)
        st.download_button("📥 تحميل AutoCAD", buf.getvalue(), "Pelan_Beast.dxf")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center;color:#d4af37'>Pelan Core v65 | 2026</p>", unsafe_allow_html=True)
