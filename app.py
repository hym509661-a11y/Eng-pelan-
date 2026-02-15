import streamlit as st
import numpy as np
import ezdxf
import io

# 1. القالب البصري الفاخر
st.set_page_config(page_title="Pelan Beast v61", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #0b1619; color: #ffffff; }
    .beast-card {
        background: rgba(20, 45, 45, 0.95); border: 2px solid #d4af37;
        border-radius: 15px; padding: 25px; box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    }
    .result-box {
        background: #132a2a; border-right: 5px solid #d4af37;
        padding: 12px; border-radius: 8px; margin: 8px 0;
    }
    .gold { color: #d4af37; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='beast-card' style='text-align:center;'><h1 style='color:#d4af37;'>🏗️ Pelan Engineering Beast v61</h1><p class='gold'>العالم الهندسي المتكامل | م. بيلان عبد الكريم | 2026</p></div>", unsafe_allow_html=True)

# 2. لوحة تحكم الوحش
with st.sidebar:
    st.header("🛠️ إعدادات الوحش")
    category = st.selectbox("المجال:", ["المنشآت الخرسانية", "هندسة الخزانات", "التحليل الزلزالي"])
    method = st.radio("المنهجية:", ["الحدية (Ultimate)", "المرنة (Elastic)"])
    st.divider()
    
    if category == "المنشآت الخرسانية":
        elem = st.selectbox("العنصر:", ["جائز/عصب", "بلاطة", "عمود", "أساس"])
        B = st.number_input("العرض B (cm):", 20, 500, 30)
        H = st.number_input("السماكة H (cm):", 10, 500, 60)
        L = st.number_input("الطول L (m):", 1.0, 30.0, 5.0)
        Load = st.number_input("الحمل (kN/m - kN):", 1.0, 20000.0, 50.0)
    elif category == "هندسة الخزانات":
        elem = "خزان"
        H_w = st.number_input("ارتفاع الماء (m):", 1.0, 20.0, 4.0)
        T_w = st.number_input("سماكة الجدار (cm):", 20, 80, 30)
        B, H, L, Load = T_w, H_w*100, 5.0, 10*H_w
    else:
        elem = "زلزال"
        W_tot = st.number_input("وزن المنشأ (kN):", 1000, 1000000, 10000)
        Z = st.select_slider("معامل Z:", options=[0.075, 0.15, 0.2, 0.3])
        B, H, L, Load = 30, 60, 3.0, 0
    
    phi = st.selectbox("قطر الحديد (mm):", [12, 14, 16, 18, 20, 25, 32], index=2)

# 3. محرك الحسابات المصفح (The Unbreakable Engine)
f_y, f_cu = 420, 25
area_bar = (np.pi * phi**2) / 4
res = {}

if category == "المنشآت الخرسانية":
    if elem in ["جائز/عصب", "بلاطة"]:
        M = (Load * L**2) / 8 if "Ultimate" in method else (Load * L**2) / 10
        As = (M * 10**6) / (0.87 * f_y * (H-5) * 10)
        n = max(2, int(np.ceil(As / area_bar)))
        res = {"العزم": f"{M:.1f} kNm", "الحديد الرئيسي": f"{n} T {phi}", "الحديد العلوي": f"{max(2, int(n*0.3))} T {phi}", "الكانات": "Φ10 @ 15cm"}
    elif elem == "عمود":
        As_min = 0.01 * (B * H * 100)
        As_req = (Load * 1000 - 0.35 * f_cu * (B * H * 100)) / (0.67 * f_y)
        n = max(4, int(np.ceil(max(As_req, As_min) / area_bar)))
        res = {"الحمل التصميمي": f"{Load} kN", "التسليح الطولي": f"{n} T {phi}", "الكانات": "Φ12 @ 15cm"}
    elif elem == "أساس":
        n = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar)))
        res = {"القطاع الخرساني": f"{B}x{H} cm", "التسليح (فرش/غطاء)": f"{n} T {phi} /m'"}

elif category == "هندسة الخزانات":
    M_tank = (Load * H_w**2) / 12
    As_tank = (M_tank * 10**6) / (0.87 * f_y * (T_w-5) * 10)
    n = max(7, int(np.ceil(As_tank / area_bar)))
    res = {"ضغط القاعدة": f"{Load} kN/m²", "عزم الجدار": f"{M_tank:.1f} kNm", "تسليح الجدران": f"{n} T {phi} /m'"}

elif category == "التحليل الزلزالي":
    V_b = Z * 1.15 * W_tot
    res = {"معامل المنطقة Z": Z, "قص القاعدة Vb": f"{V_b:.1f} kN", "التوصية": "مبنى ذو جساءة عالية"}

# 4. واجهة العرض والتفريد
c1, c2 = st.columns([1.2, 1])

with c1:
    st.markdown("<div class='beast-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 نتائج التحليل - {elem}")
    for k, v in res.items():
        st.markdown(f"<div class='result-box'><b class='gold'>{k}:</b> {v}</div>", unsafe_allow_html=True)
    st.divider()
    if "جائز" in elem:
            elif "عمود" in elem:
            elif "أساس" in elem:
            st.info(f"👨‍🏫 مذكرة م. بيلان: تم التصميم لضمان أعلى مستويات الأمان الإنشائي.")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='beast-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ تفريد الحديد (BBS)")
    main_bar = res.get("الحديد الرئيسي", res.get("التسليح الطولي", res.get("تسليح الجدران", res.get("التسليح (فرش/غطاء)", "Φ16"))))
    st.markdown(f"""
    <div style='border:2px dashed #d4af37; padding:25px; text-align:center; border-radius:15px; background:rgba(0,0,0,0.2);'>
        <h2 style='color:#50c878;'>{main_bar}</h2>
        <p class='gold'>↑ سهم رفع وتوصيف الحديد الرئيسي ↑</p>
        <hr style='border-color:#d4af37;'>
        <p style='color:#aaa; font-size:0.9rem;'>توزيع الكانات: {res.get('الكانات', 'Φ10 @ 15cm')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🛠️ تصدير المخطط إلى AutoCAD 🚀"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_text(f"PELAN BEAST v61 - {elem}", dxfattribs={'height': 5}).set_placement((0, 0))
        buf = io.StringIO(); doc.write(buf)
        st.download_button("📥 تحميل DXF", buf.getvalue(), f"Pelan_Beast_{elem}.dxf")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37; font-size:0.8rem;'>Pelan Engineering Beast v61 | 2026</p>", unsafe_allow_html=True)
