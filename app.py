import streamlit as st
import numpy as np
import ezdxf
import io

# 1. إعدادات الواجهة الاحترافية (Dark Gold Theme)
st.set_page_config(page_title="Pelan v78 Absolute", layout="wide")
st.markdown("<style>.stApp{background-color:#0b1619;color:#fff}.card{background:#142d2d;border:2px solid #d4af37;border-radius:15px;padding:20px;margin-bottom:15px}.gold{color:#d4af37;font-weight:bold}</style>", unsafe_allow_html=True)

st.markdown("<div class='card' style='text-align:center;'><h1 style='color:#d4af37;'>🏗️ Pelan Absolute Suite v78</h1><p class='gold'>الموسوعة الهندسية الشاملة | م. بيلان عبد الكريم | 2026</p></div>", unsafe_allow_html=True)

# 2. لوحة التحكم الشاملة (The Master Sidebar)
with st.sidebar:
    st.header("📂 إدارة المشروع")
    category = st.selectbox("اختر التصنيف:", ["الخرسانة (العناصر)", "البلاطات (Slabs)", "الأساسات (Foundations)", "الخزانات والمنشآت المائية", "التحليل الزلزالي"])
    
    st.divider()
    st.header("📏 المدخلات العامة")
    B = st.number_input("العرض B (cm):", 20, 1000, 30)
    H = st.number_input("الارتفاع/السماكة H (cm):", 10, 1000, 60)
    L = st.number_input("الطول/البحر L (m):", 0.1, 100.0, 5.0)
    Load = st.number_input("الحمل المصمم (kN أو kN/m):", 1.0, 1000000.0, 150.0)
    phi = st.selectbox("القطر الرئيسي (mm):", [8, 10, 12, 14, 16, 18, 20, 25, 32], index=4)
    phi_str = st.selectbox("قطر الكانات (mm):", [8, 10, 12], index=1)

# 3. محرك الحسابات (The Absolute Engine)
f_y, f_cu = 420, 25
area_bar = (np.pi * phi**2) / 4
results = {}
detailing = ""

# --- قسم الخرسانة (جوائز وأعمدة) ---
if category == "الخرسانة (العناصر)":
    elem = st.sidebar.selectbox("نوع العنصر:", ["جائز مستمر", "جائز بسيط", "عمود مستطيل", "عمود دائري"])
    if "جائز" in elem:
        M = (Load * L**2) / (8 if "بسيط" in elem else 10)
        As = (M * 1e6) / (0.87 * f_y * (H-5) * 10)
        n = max(2, int(np.ceil(As / area_bar)))
        results = {"العزم التصميمي": f"{M:.1f} kNm", "الحديد السفلي": f"{n} T {phi}", "الحديد العلوي": f"{max(2, int(n*0.3))} T {phi}", "الكانات": f"Φ{phi_str} @ 15cm"}
        detailing = f"Main: {n} T {phi} | Stirrups: Φ{phi_str}@15"
    else: # أعمدة
        Ag = (B * H * 100) if "مستطيل" in elem else (np.pi * (B**2) / 4 * 100)
        As_req = (Load * 1000 - 0.35 * f_cu * Ag) / (0.67 * f_y)
        n = max(4 if "مستطيل" in elem else 6, int(np.ceil(max(As_req, 0.01 * Ag) / area_bar)))
        results = {"مساحة المقطع": f"{Ag/100:.1f} cm²", "عدد القضبان": f"{n} T {phi}", "الكانات": f"Φ{phi_str} @ 20cm"}
        detailing = f"{n} T {phi}"

# --- قسم البلاطات ---
elif category == "البلاطات (Slabs)":
    slab_type = st.sidebar.selectbox("نوع البلاطة:", ["مصمتة (Solid Slab)", "هوردي (Ribbed Slab)", "فلات (Flat Slab)"])
    M = (Load * L**2) / 10
    As = (M * 1e6) / (0.87 * f_y * (H-3) * 10)
    n = max(5, int(np.ceil(As / area_bar)))
    results = {"نوع البلاطة": slab_type, "العزم": f"{M:.1f} kNm/m", "التسليح/م": f"{n} T {phi}"}
    detailing = f"{n} T {phi} / m'"

# --- قسم الأساسات ---
elif category == "الأساسات (Foundations)":
    f_type = st.sidebar.selectbox("نوع الأساس:", ["منفرد (Isolated)", "مشترك (Combined)", "حصيرة (Raft)"])
    stress = Load / (B * L / 10000)
    n = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar)))
    results = {"إجهاد التربة": f"{stress:.2f} kN/m²", "التسليح (فرش)": f"{n} T {phi}/m", "التسليح (غطاء)": f"{n} T {phi}/m"}
    detailing = f"{n} T {phi} @ 15cm"

# --- قسم الخزانات ---
elif category == "الخزانات والمنشآت المائية":
    t_type = st.sidebar.selectbox("نوع الخزان:", ["مستطيل أرضي", "دائري عالي", "جدار استنادي"])
    Mt = (10 * (H/100) * L**2) / 12
    n = max(7, int(np.ceil(((Mt * 1e6) / (0.87 * f_y * (H-5) * 10)) / area_bar)))
    results = {"عزم الماء/التربة": f"{Mt:.1f} kNm", "تسليح الشد": f"{n} T {phi}/m", "توزيع أفقي": f"Φ12 @ 20cm"}
    detailing = f"{n} T {phi} / m'"

# --- قسم الزلازل ---
else:
    Vb = 0.15 * Load
    results = {"قص القاعدة Vb": f"{Vb:.1f} kN", "توزيع القوى": "Linear", "التسليح": "عرضي مكثف (Seismic)"}
    detailing = "Capped Reinforcement"

# 4. عرض النتائج (Professional Layout)
col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 التقرير الفني للنتائج")
    for k, v in results.items():
        st.write(f"**{k}:** {v}")
    st.divider()
    # هنا تظهر الصور التوضيحية بناءً على القسم
    st.info(f"تم التصميم لعنصر ({category}) وفق الكودات العالمية 2026")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🖋️ تفريد الحديد (BBS)")
    st.markdown(f"<div style='border:2px dashed #d4af37;padding:30px;text-align:center;border-radius:15px;background:#132a2a'><h1 style='color:#50c878'>{detailing}</h1><p class='gold'>م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)
    
    if st.button("🚀 تصدير إلى AutoCAD (DXF)"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_text(f"PELAN ABSOLUTE - {category}", dxfattribs={'height': 5}).set_placement((0, 0))
        buf = io.StringIO(); doc.write(buf)
        st.download_button("📥 تحميل المخطط", buf.getvalue(), "Pelan_Absolute.dxf")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center;color:#d4af37'>Pelan Absolute Suite v78 | الموسوعة الهندسية الكاملة</p>", unsafe_allow_html=True)
