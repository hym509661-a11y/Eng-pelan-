import streamlit as st
import numpy as np
import ezdxf
import io

# 1. الإعدادات البصرية (Engineering Emerald & Gold)
st.set_page_config(page_title="Pelan Ultimate v55", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0d1b1e; color: #ffffff; }
    .master-card {
        background: rgba(16, 44, 41, 0.95);
        border: 2px solid #d4af37;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .result-box {
        background: #1a3c34; border-left: 5px solid #d4af37;
        padding: 12px; border-radius: 8px; margin: 5px 0;
    }
    .gold-label { color: #d4af37; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='master-card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Ultimate Structural Suite v55</h1><p style='color:#d4af37;'>الموسوعة الهندسية الشاملة | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. المدخلات الهندسية
with st.sidebar:
    st.header("🏗️ اختيار العنصر")
    elem_type = st.selectbox("نوع العنصر الإنشائي:", 
                             ["جائز (Beam)", "عصب هوردي", "بلاطة مصمتة", "عمود خرساني", "أساس منفرد"])
    
    st.divider()
    st.subheader("📐 الأبعاد والأحمال")
    if "عمود" in elem_type or "أساس" in elem_type:
        B = st.number_input("العرض B (cm):", 20, 500, 30)
        H = st.number_input("السماكة/العمق H (cm):", 20, 500, 60)
        P = st.number_input("الحمل المحوري P (kN):", 10.0, 10000.0, 1500.0)
        L = 3.0 # ارتفاع افتراضي
    else:
        L = st.number_input("طول البحر L (m):", 1.0, 20.0, 5.0)
        B = st.number_input("العرض B (cm):", 10, 100, 25)
        H = st.number_input("السماكة H (cm):", 10, 150, 60)
        Wu = st.number_input("الحمل Wu (kN/m):", 1.0, 250.0, 40.0)

    phi_main = st.selectbox("قطر الحديد الرئيسي (mm):", [12, 14, 16, 18, 20, 25], index=2)
    phi_str = st.selectbox("قطر الكانات (mm):", [8, 10, 12])

# 3. محرك التصميم الذكي (إصلاح خطأ ValueError)
f_y, f_cu = 420, 25
area_bar = (np.pi * phi_main**2) / 4

# تعريف افتراضي للمتغيرات لمنع أي خطأ
n_bottom, n_top, n_hang, stirrups_desc = 0, 0, 0, ""
results = {}

if "عمود" in elem_type:
    # تصميم عمود
    As_req = (P * 1000 - 0.35 * f_cu * (B * H * 100)) / (0.67 * f_y)
    n_bottom = max(4, int(np.ceil(max(As_req, 0.01 * B * H * 100) / area_bar)))
    stirrups_desc = f"Φ{phi_str} @ 15cm"
    results = {"الحمل": f"{P} kN", "القطاع": f"{B}x{H}", "الحديد الكلي": f"{n_bottom} T {phi_main}"}

elif "أساس" in elem_type:
    # تصميم أساس
    q_net = P / (B * H / 10000)
    n_bottom = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar))) # تسليح أدنى
    stirrups_desc = "فرش وغطاء"
    results = {"إجهاد التربة": f"{q_net:.1f}", "القطاع": f"{B}x{H}", "التسليح": f"{n_bottom} T {phi_main} /m"}

else:
    # تصميم جوائز وبلاطات
    M = (Wu * L**2) / 8
    As_req = (M * 10**6) / (0.87 * f_y * (H-5) * 10)
    n_bottom = max(2, int(np.ceil(As_req / area_bar)))
    n_top = max(2, int(np.ceil(n_bottom * 0.4)))
    n_hang = 2
    stirrups_desc = f"Φ{phi_str} @ 15cm"
    results = {"العزم": f"{M:.1f} kNm", "القطاع": f"{B}x{H}", "الحديد السفلي": f"{n_bottom} T {phi_main}"}

# 4. واجهة العرض والتصدير
col_res, col_vis = st.columns([1.2, 1])

with col_res:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader(f"📑 تقرير التصميم: {elem_type}")
    
    rc = st.columns(len(results))
    for i, (key, val) in enumerate(results.items()):
        rc[i].markdown(f"<div class='result-box'><span class='gold-label'>{key}:</span><br><b>{val}</b></div>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 👨‍🏫 تفاصيل التسليح النهائية:")
    if "عمود" in elem_type:
        st.success(f"📌 الحديد الطولي: {n_bottom} T {phi_main}")
        st.success(f"📌 الكانات: {stirrups_desc}")
            elif "أساس" in elem_type:
        st.success(f"📌 تسليح القاعدة: {n_bottom} T {phi_main} لكل متر")
            else:
        st.success(f"📌 الفرش السفلي: {n_bottom} T {phi_main}")
        st.success(f"📌 الحديد العلوي/التعليق: {n_top if n_top > 0 else n_hang} T {phi_main}")
        st.success(f"📌 الكانات: {stirrups_desc}")
            st.markdown("</div>", unsafe_allow_html=True)

with col_vis:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ تفريد الحديد وسهم الرفع")
    
    st.markdown(f"""
    <div style='border:2px solid #d4af37; padding:20px; border-radius:15px; text-align:center; background:rgba(255,255,255,0.05);'>
        <h2 style='color:#50c878;'>{n_bottom} Φ {phi_main}</h2>
        <p style='color:#d4af37;'>↑ سهم رفع وتوصيف الحديد الرئيسي ↑</p>
        <hr style='border-color:#d4af37;'>
        <h3 style='color:#d4af37;'>{stirrups_desc}</h3>
        <p style='color:#aaa;'>توزيع الكانات / الحديد الثانوي</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🛠️ تصدير إلى AutoCAD 🚀"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_lwpolyline([(0,0), (100,0), (100,100), (0,100), (0,0)])
        msp.add_text(f"PELAN DESIGN: {n_bottom} T {phi_main}", dxfattribs={'height': 5}).set_placement((10, -10))
        buf = io.StringIO(); doc.write(buf)
        st.download_button("📥 تحميل DXF", buf.getvalue(), f"Pelan_{elem_type}.dxf")
        st.success("تم التصدير!")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37;'>Pelan Engine v55 | 2026</p>", unsafe_allow_html=True)
