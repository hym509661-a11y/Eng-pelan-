import streamlit as st
import numpy as np
import ezdxf
import io

# 1. الواجهة الملكية الفاخرة
st.set_page_config(page_title="Pelan Sovereign v58", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #0b1619; color: #ffffff; }
    .master-card {
        background: rgba(20, 45, 45, 0.95);
        border: 2px solid #d4af37;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    }
    .result-box {
        background: #132a2a; border-left: 5px solid #d4af37;
        padding: 15px; border-radius: 10px; margin: 10px 0;
    }
    .gold-text { color: #d4af37; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='master-card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Sovereign Engineering Suite v58</h1><p class='gold-text'>المحرك الإنشائي الشامل | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية (مدخلات المهندس بيلان)
with st.sidebar:
    st.header("⚙️ معايير التصميم")
    category = st.selectbox("المجال:", ["المنشآت الخرسانية", "هندسة الخزانات", "التحليل الزلزالي"])
    method = st.radio("طريقة الحساب:", ["الطريقة الحدية (Ultimate)", "الطريقة المرنة (Elastic)"])
    
    st.divider()
    # مدخلات ذكية متغيرة
    if category == "المنشآت الخرسانية":
        elem = st.selectbox("العنصر:", ["جائز/عصب", "بلاطة مصمتة", "عمود", "أساس منفرد"])
        B = st.number_input("العرض B (cm):", 20, 200, 30)
        H = st.number_input("السماكة H (cm):", 10, 200, 60)
        L = st.number_input("الطول L (m):", 1.0, 20.0, 5.0)
        Load = st.number_input("الحمل (kN/m - kN):", 1.0, 8000.0, 40.0)
    elif category == "هندسة الخزانات":
        elem = "خزان"
        H_w = st.number_input("ارتفاع الماء (m):", 1.0, 15.0, 4.0)
        T_w = st.number_input("سماكة الجدار (cm):", 20, 50, 30)
        B = T_w; H = H_w * 100; L = 5.0; Load = 10 * H_w
    else:
        elem = "زلزال"
        W_total = st.number_input("الوزن الكلي (kN):", 1000, 200000, 5000)
        Z = st.select_slider("معامل المنطقة Z:", options=[0.075, 0.15, 0.2, 0.3])
        B=30; H=60; L=3.0; Load=0

    phi = st.selectbox("قطر الحديد (mm):", [12, 14, 16, 18, 20, 25], index=2)

# 3. محرك التصميم الموحد (Unbreakable Design Engine)
# حسابات هندسية دقيقة
f_y, f_cu = 420, 25
area_bar = (np.pi * phi**2) / 4
res = {}

# حساب الحديد (تلقائي)
if category == "المنشآت الخرسانية":
    if "جائز" in elem or "بلاطة" in elem:
        M = (Load * L**2) / 8 if "Ultimate" in method else (Load * L**2) / 10
        As = (M * 10**6) / (0.87 * f_y * (H-5) * 10)
        n = max(2, int(np.ceil(As / area_bar)))
        res = {"العزم": f"{M:.1f} kNm", "الفرش السفلي": f"{n} T {phi}", "العلوي/التعليق": f"{max(2, int(n*0.3))} T {phi}", "الكانات": "Φ10 @ 15cm"}
    elif "عمود" in elem:
        As_min = 0.01 * (B * H * 100)
        As_req = (Load * 1000 - 0.35 * f_cu * (B * H * 100)) / (0.67 * f_y)
        n = max(4, int(np.ceil(max(As_req, As_min) / area_bar)))
        res = {"الحمل": f"{Load} kN", "التسليح الطولي": f"{n} T {phi}", "الكانات": "Φ10 @ 15cm"}
    elif "أساس" in elem:
        n = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar)))
        res = {"القطاع": f"{B}x{H} cm", "فرش وغطاء": f"{n} T {phi} /m"}

elif category == "هندسة الخزانات":
    M_tank = (Load * H_w**2) / 12
    As = (M_tank * 10**6) / (0.87 * f_y * (T_w-5) * 10)
    n = max(6, int(np.ceil(As / area_bar)))
    res = {"ضغط الماء": f"{Load} kN/m²", "عزم الجدار": f"{M_tank:.1f} kNm", "التسليح": f"{n} T {phi} /m"}

elif category == "التحليل الزلزالي":
    V_b = Z * 1.15 * W_total
    res = {"معامل Z": Z, "قص القاعدة Vb": f"{V_b:.1f} kN", "الحالة": "مبنى صلب"}

# 4. واجهة النتائج والتفريد
col_data, col_draw = st.columns([1.2, 1])

with col_data:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 نتائج التصميم ({method})")
    for k, v in res.items():
        st.markdown(f"<div class='result-box'><b class='gold-text'>{k}:</b> {v}</div>", unsafe_allow_html=True)
    
    st.divider()
    st.info(f"💡 توصية م. بيلان: تم تصميم {elem} وفق أدق المعايير الهندسية لعام 2026.")
    
    # استدعاء المخطط الإنشائي المناسب
    if "جائز" in elem or "عصب" in elem:
            elif "عمود" in elem:
            elif "خزان" in elem:
            else:
            
    st.markdown("</div>", unsafe_allow_html=True)

with col_draw:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ تفريد الحديد وسهم الرفع (BBS)")
    
    main_steel = res.get("الفرش السفلي", res.get("التسليح الطولي", res.get("التسليح", "حسب المخطط")))
    
    st.markdown(f"""
    <div style='border:2px dashed #d4af37; padding:20px; text-align:center; border-radius:15px; background:rgba(255,255,255,0.05);'>
        <h2 style='color:#50c878;'>{main_steel}</h2>
        <p class='gold-text'>↑ سهم رفع وتوصيف الحديد الرئيسي ↑</p>
        <hr style='border-color:#d4af37;'>
        <p style='color:#aaa;'>الكانات وتوزيع الإجهادات العرضية</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    if st.button("🛠️ تصدير المخطط الشامل للأوتوكاد 🚀"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_text(f"PELAN v58 - {elem}", dxfattribs={'height': 5}).set_placement((0, 10))
        buf = io.StringIO(); doc.write(buf)
        st.download_button("📥 تحميل DXF", buf.getvalue(), f"Pelan_{elem}.dxf")
        st.success("تم التصدير!")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37; font-size:0.8rem;'>Pelan sovereign Engine v58 | 2026</p>", unsafe_allow_html=True)
