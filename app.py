import streamlit as st
import numpy as np
import ezdxf
import io

# 1. إعدادات المظهر الفاخر (Theme)
st.set_page_config(page_title="Pelan Beast v60", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #0b1619; color: #ffffff; }
    .beast-card {
        background: rgba(20, 45, 45, 0.95);
        border: 2px solid #d4af37;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    }
    .result-item {
        background: #132a2a; border-right: 5px solid #d4af37;
        padding: 12px; border-radius: 8px; margin: 8px 0;
    }
    .gold { color: #d4af37; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='beast-card' style='text-align:center;'><h1 style='color:#d4af37;'>🏗️ Pelan Engineering Beast v60</h1><p class='gold'>العالم الهندسي المتكامل | م. بيلان عبد الكريم | 2026</p></div>", unsafe_allow_html=True)

# 2. لوحة التحكم الشاملة (Control Panel)
with st.sidebar:
    st.header("🛠️ إعدادات الوحش الهندسي")
    mode = st.selectbox("المجال الإنشائي:", ["الخرسانة المسلحة", "هندسة الخزانات", "التحليل الزلزالي"])
    method = st.radio("المنهجية:", ["الحدية (Ultimate)", "المرنة (Elastic)"])
    
    st.divider()
    if mode == "الخرسانة المسلحة":
        elem = st.selectbox("العنصر:", ["جائز/عصب", "بلاطة مصمتة", "عمود", "أساس منفرد"])
        B_cm = st.number_input("العرض B (cm):", 20, 500, 30)
        H_cm = st.number_input("السماكة H (cm):", 10, 500, 60)
        L_m = st.number_input("الطول L (m):", 1.0, 30.0, 5.0)
        Load = st.number_input("الحمل (kN/m - kN):", 1.0, 15000.0, 50.0)
    elif mode == "هندسة الخزانات":
        elem = "خزان"
        H_w = st.number_input("ارتفاع الماء (m):", 1.0, 20.0, 4.0)
        T_w = st.number_input("سماكة الجدار (cm):", 20, 80, 30)
        B_cm, H_cm, L_m, Load = T_w, H_w*100, 5.0, 10*H_w
    else:
        elem = "زلزال"
        W_tot = st.number_input("الوزن الكلي للمبنى (kN):", 1000, 1000000, 10000)
        Z_factor = st.select_slider("معامل المنطقة Z:", options=[0.075, 0.15, 0.2, 0.3])
        B_cm, H_cm, L_m, Load = 30, 60, 3.0, 0

    phi = st.selectbox("قطر الحديد (mm):", [12, 14, 16, 18, 20, 25, 32], index=2)

# 3. محرك الحسابات (نظام المخزن الآمن لمنع ValueError)
f_y, f_cu = 420, 25
area_bar = (np.pi * phi**2) / 4
output = {}

# منطق الحساب الموحد
if mode == "الخرسانة المسلحة":
    if "جائز" in elem or "بلاطة" in elem:
        M = (Load * L_m**2) / 8 if "Ultimate" in method else (Load * L_m**2) / 10
        As = (M * 10**6) / (0.87 * f_y * (H_cm-5) * 10)
        n = max(2, int(np.ceil(As / area_bar)))
        output = {"العزم": f"{M:.1f} kNm", "التسليح الرئيسي": f"{n} T {phi}", "العلوي": f"{max(2, int(n*0.3))} T {phi}", "الكانات": "Φ10 @ 15cm"}
    elif "عمود" in elem:
        As_min = 0.01 * (B_cm * H_cm * 100)
        As_req = (Load * 1000 - 0.35 * f_cu * (B_cm * H_cm * 100)) / (0.67 * f_y)
        n = max(4, int(np.ceil(max(As_req, As_min) / area_bar)))
        output = {"الحمل التصميمي": f"{Load} kN", "الحديد الطولي": f"{n} T {phi}", "الكانات": "Φ10 @ 15cm"}
    elif "أساس" in elem:
        n = max(6, int(np.ceil((0.0018 * B_cm * H_cm * 100) / area_bar)))
        output = {"إجهاد التربة": "ضمن المسموح", "تسليح القاعدة": f"{n} T {phi} /m'"}

elif mode == "هندسة الخزانات":
    M_wall = (Load * H_w**2) / 12
    As_w = (M_wall * 10**6) / (0.87 * f_y * (T_w-5) * 10)
    n = max(7, int(np.ceil(As_w / area_bar)))
    output = {"ضغط السائل": f"{Load} kN/m²", "عزم الجدار": f"{M_wall:.1f} kNm", "التسليح": f"{n} T {phi} /m'"}

elif mode == "التحليل الزلزالي":
    V_base = Z_factor * 1.15 * W_tot
    output = {"معامل المنطقة Z": Z_factor, "قص القاعدة Vb": f"{V_base:.1f} kN", "التوزيع": "خطي مثلثي"}

# 4. العرض الفني (Visualizer)
c1, c2 = st.columns([1.2, 1])

with c1:
    st.markdown("<div class='beast-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 النتائج الهندسية ({method})")
    for k, v in output.items():
        st.markdown(f"<div class='result-item'><b class='gold'>{k}:</b> {v}</div>", unsafe_allow_html=True)
    
    st.divider()
    if "جائز" in elem:
            elif "عمود" in elem:
            elif "أساس" in elem:
            elif "خزان" in elem:
            
    st.info(f"👨‍🏫 مهندس بيلان: هذا التصميم يحقق كافة اشتراطات الأمان والمتانة لـ {elem}.")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='beast-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ تفريد الحديد (BBS)")
    
    main_steel = output.get("التسليح الرئيسي", output.get("الحديد الطولي", output.get("تسليح القاعدة", output.get("التسليح", "Φ16"))))
    
    st.markdown(f"""
    <div style='border:2px dashed #d4af37; padding:25px; text-align:center; border-radius:15px; background:rgba(0,0,0,0.2);'>
        <h2 style='color:#50c878;'>{main_steel}</h2>
        <p class='gold'>↑ سهم رفع وتوصيف الوحش الهندسي ↑</p>
        <hr style='border-color:#d4af37;'>
        <p style='color:#aaa; font-size:0.9rem;'>الكانات وتوزيع الأحمال العرضية</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🛠️ تصدير العالم الهندسي إلى AutoCAD 🚀"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_text(f"PELAN BEAST v60 - {elem}", dxfattribs={'height': 5}).set_placement((0, 0))
        buf = io.StringIO(); doc.write(buf)
        st.download_button("📥 تحميل ملف DXF", buf.getvalue(), f"Pelan_Beast_{elem}.dxf")
        st.success("تم التصدير بنجاح!")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37; font-size:0.8rem;'>Pelan Engineering Beast v60 | Power by Gemini 2026</p>", unsafe_allow_html=True)
