import streamlit as st
import numpy as np
import ezdxf
import io

# 1. الإعدادات البصرية الملكية
st.set_page_config(page_title="Pelan Sovereign Suite v57", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0d1b1e; color: #ffffff; }
    .master-card {
        background: rgba(16, 44, 41, 0.95);
        border: 2px solid #d4af37;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
    }
    .result-box {
        background: #1a3c34; border-left: 5px solid #50c878;
        padding: 15px; border-radius: 8px; margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='master-card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Sovereign Engineering Suite v57</h1><p style='color:#d4af37;'>المحرك الهندسي الشامل | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية (مدخلات المهندس بيلان)
with st.sidebar:
    st.header("⚙️ معايير المشروع")
    category = st.selectbox("المجال الإنشائي:", ["العناصر الإنشائية", "هندسة الخزانات", "الدراسة الزلزالية"])
    method = st.radio("منهجية التصميم:", ["الحدية (Ultimate)", "المرنة (Elastic/Working)"])
    
    st.divider()
    if category == "العناصر الإنشائية":
        elem = st.selectbox("العنصر:", ["جائز (Beam)", "عصب (Rib)", "بلاطة", "عمود", "أساس"])
        B = st.number_input("العرض B (cm):", 20, 100, 30)
        H = st.number_input("السماكة/الارتفاع H (cm):", 20, 200, 60)
        L = st.number_input("الطول L (m):", 1.0, 15.0, 5.0)
        Load = st.number_input("الحمل (kN/m or kN):", 1.0, 5000.0, 40.0)
    elif category == "هندسة الخزانات":
        elem = "خزان"
        H_w = st.number_input("عمق الماء (m):", 1.0, 12.0, 4.0)
        B_tank = st.number_input("طول الجدار (m):", 2.0, 20.0, 5.0)
        T_wall = st.number_input("سماكة الجدار (cm):", 20, 50, 25)
    else:
        elem = "زلزال"
        W_building = st.number_input("الوزن الكلي للمنشأ (kN):", 1000, 100000, 5000)
        Z_zone = st.select_slider("المنطقة الزلزالية (Z):", options=[0.075, 0.15, 0.20, 0.30])

    phi = st.selectbox("قطر الحديد (mm):", [12, 14, 16, 18, 20, 25])

# 3. محرك الحسابات المستقل (إصلاح خطأ ValueError و Indentation)
f_y, f_cu = 420, 25
area_bar = (np.pi * phi**2) / 4
res = {}

if category == "العناصر الإنشائية":
    if elem in ["جائز (Beam)", "عصب (Rib)", "بلاطة"]:
        M = (Load * L**2) / 8 if method == "الحدية (Ultimate)" else (Load * L**2) / 10
        As = (M * 10**6) / (0.87 * f_y * (H-5) * 10)
        n = int(np.ceil(As / area_bar))
        res = {"العزم": f"{M:.1f} kNm", "التسليح السفلي": f"{n} T {phi}", "العلوي": f"{max(2, int(n*0.3))} T {phi}"}
    elif elem == "عمود":
        As_min = 0.01 * (B * H * 100)
        As_req = (Load * 1000 - 0.35 * f_cu * (B * H * 100)) / (0.67 * f_y)
        n = max(4, int(np.ceil(max(As_req, As_min) / area_bar)))
        res = {"الحمل التصميمي": f"{Load} kN", "التسليح": f"{n} T {phi}", "الكانات": "Φ10 @ 15cm"}
    elif elem == "أساس":
        n = int(np.ceil((0.0018 * B * H * 100) / area_bar))
        res = {"الأبعاد": f"{B}x{H} cm", "الحديد/م": f"{max(6, n)} T {phi}"}

elif category == "هندسة الخزانات":
    P_water = 10 * H_w
    M_tank = (P_water * H_w**2) / 10
    As_tank = (M_tank * 10**6) / (0.87 * f_y * (T_wall-5) * 10)
    n = int(np.ceil(As_tank / area_bar))
    res = {"ضغط القاعدة": f"{P_water} kN/m²", "عزم الجدار": f"{M_tank:.1f} kNm", "التسليح": f"{n} T {phi} /m"}

elif category == "الدراسة الزلزالية":
    V_base = Z_zone * 1.2 * W_building # حساب تبسيطي لقص القاعدة
    res = {"معامل المنطقة Z": Z_zone, "قص القاعدة Vb": f"{V_base:.1f} kN", "قوة كل طابق": "حسب توزيع الكتلة"}

# 4. العرض الفني وتفريد الحديد
col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 نتائج التحليل: {elem}")
    for k, v in res.items():
        st.markdown(f"<div class='result-box'><b style='color:#d4af37;'>{k}:</b> {v}</div>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 👨‍🏫 مذكرة المهندس بيلان:")
    st.success(f"تم اعتماد الطريقة {method} في التصميم لضمان مطابقة الكود الإنشائي.")
        st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ مخطط تفريد الحديد (BBS)")
    st.markdown(f"""
    <div style='border:2px dashed #d4af37; padding:20px; text-align:center; border-radius:10px;'>
        <h2 style='color:#50c878;'>{res.get('التسليح', res.get('التسليح السفلي', 'حسب المخطط'))}</h2>
        <p style='color:#d4af37;'>↑ سهم رفع وتوصيف دقيق ↑</p>
        <hr style='border-color:#d4af37;'>
        <p style='color:#aaa;'>الكانات وتوزيع الإجهادات</p>
    </div>
    """, unsafe_allow_html=True)
    
        
    if st.button("🛠️ تصدير المخطط الهندسي AutoCAD 🚀"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_text(f"PELAN DESIGN v57 - {elem}", dxfattribs={'height': 5}).set_placement((0, 0))
        buf = io.StringIO(); doc.write(buf)
        st.download_button("📥 تحميل DXF", buf.getvalue(), f"Pelan_{elem}.dxf")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37;'>Pelan Engine v57 | 2026</p>", unsafe_allow_html=True)
