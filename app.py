import streamlit as st
import numpy as np
import ezdxf
import io

# 1. المظهر الخارجي (الوحش الذهبي)
st.set_page_config(page_title="Pelan Beast v69", layout="wide")
st.markdown("<style>.stApp { background-color: #0b1619; color: #ffffff; } .beast-card { background: rgba(20, 45, 45, 0.95); border: 2px solid #d4af37; border-radius: 15px; padding: 20px; margin-bottom: 20px; } .result-box { background: #132a2a; border-right: 5px solid #d4af37; padding: 10px; border-radius: 8px; margin: 5px 0; } .gold { color: #d4af37; font-weight: bold; }</style>", unsafe_allow_html=True)

st.markdown("<div class='beast-card' style='text-align:center;'><h1 style='color:#d4af37;'>🏗️ Pelan Engineering Beast v69</h1><p class='gold'>الموسوعة الشاملة (زلازل - خزانات - خرسانة) | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. مدخلات الوحش (Sidebar)
with st.sidebar:
    st.header("⚙️ الإعدادات")
    category = st.selectbox("المجال:", ["الخرسانة المسلحة", "الخزانات", "الزلازل"])
    method = st.radio("المنهجية:", ["الحدية (Ultimate)", "المرنة (Elastic)"])
    st.divider()
    B = st.number_input("العرض B (cm):", 20, 500, 30)
    H = st.number_input("الارتفاع H (cm):", 10, 500, 60)
    L = st.number_input("البحر L (m):", 1.0, 30.0, 5.0)
    Load = st.number_input("الحمل (kN):", 1.0, 100000.0, 100.0)
    phi = st.selectbox("القطر (mm):", [12, 14, 16, 18, 20, 25, 32], index=2)

# 3. محرك الحسابات المصفح (Unbreakable Engine)
# تم تصميم هذا المحرك ليكون مسطحاً تماماً لتجنب أخطاء الإزاحة (Indentation) التي ظهرت في صورك
f_y, f_cu, area_bar = 420, 25, (np.pi * phi**2) / 4
res = {}
main_steel = "Φ16"

if category == "الخرسانة المسلحة":
    elem = st.sidebar.selectbox("العنصر:", ["جائز/عصب", "بلاطة", "عمود", "أساس"])
    if elem in ["جائز/عصب", "بلاطة"]:
        M = (Load * L**2) / 8 if "Ultimate" in method else (Load * L**2) / 10
        As = (M * 10**6) / (0.87 * f_y * (H-5) * 10)
        n = max(2, int(np.ceil(As / area_bar)))
        res = {"العزم": f"{M:.1f} kNm", "الحديد الرئيسي": f"{n} T {phi}", "العلوي": f"{max(2, int(n*0.3))} T {phi}", "الكانات": "Φ10 @ 15cm"}
        main_steel = f"{n} T {phi}"
    if elem == "عمود":
        As_req = (Load * 1000 - 0.35 * f_cu * (B * H * 100)) / (0.67 * f_y)
        n = max(4, int(np.ceil(max(As_req, 0.01*B*H*100) / area_bar)))
        res = {"الحمل": f"{Load} kN", "التسليح": f"{n} T {phi}", "الكانات": "Φ12 @ 15cm"}
        main_steel = f"{n} T {phi}"
    if elem == "أساس":
        n = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar)))
        res = {"القطاع": f"{B}x{H} cm", "فرش وغطاء": f"{n} T {phi} /m'"}
        main_steel = f"{n} T {phi} /m'"

if category == "الخزانات":
    M_t = (10 * (H/100) * L**2) / 12
    n = max(7, int(np.ceil(((M_t * 10**6) / (0.87 * f_y * (H-5) * 10)) / area_bar)))
    res = {"عزم الجدار": f"{M_t:.1f} kNm", "تسليح الجدار": f"{n} T {phi} /m'"}
    main_steel = f"{n} T {phi} /m'"

if category == "الزلازل":
    V_b = 0.15 * Load
    res = {"قص القاعدة Vb": f"{V_b:.1f} kN", "معامل المنطقة": "Z=0.15", "الحالة": "مبنى مقاوم"}
    main_steel = "تسليح عرضي مكثف"

# 4. العرض الفني وسهم الرفع (BBS)
c1, c2 = st.columns([1.2, 1])

with c1:
    st.markdown("<div class='beast-card'>", unsafe_allow_html=True)
    st.subheader("📊 النتائج الإنشائية")
    for k, v in res.items():
        st.markdown(f"<div class='result-box'><b class='gold'>{k}:</b> {v}</div>", unsafe_allow_html=True)
    st.divider()
        st.info("💡 تم حساب النتائج آلياً وفق معايير م. بيلان لعام 2026.")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='beast-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ سهم رفع التفريد")
    st.markdown(f"<div style='border:2px dashed #d4af37; padding:20px; text-align:center; border-radius:15px; background:rgba(0,0,0,0.2);'><h2 style='color:#50c878;'>{main_steel}</h2><p class='gold'>↑ توصيف الوحش الهندسي ↑</p></div>", unsafe_allow_html=True)
    if st.button("🛠️ تصدير DXF 🚀"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_text(f"PELAN BEAST v69", dxfattribs={'height': 5}).set_placement((0, 0))
        buf = io.StringIO(); doc.write(buf)
        st.download_button("📥 تحميل المخطط", buf.getvalue(), "Pelan_Beast.dxf")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37;'>Pelan Beast v69 | Final Unstoppable Version</p>", unsafe_allow_html=True)
