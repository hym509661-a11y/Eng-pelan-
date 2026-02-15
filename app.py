import streamlit as st
import numpy as np

# 1. إعداد واجهة المهندس Pelan
st.set_page_config(page_title="Pelan Engineering Suite", layout="wide")

# تصميم الهوية البصرية
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .pelan-header {
        background-color: #002b5c;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        border-bottom: 5px solid #a8eb12;
    }
    </style>
    <div class="pelan-header">
        <h1>Pelan Engineering Suite</h1>
        <p>المصمم الإنشائي: م. بيلان عبد الكريم</p>
    </div>
""", unsafe_allow_html=True)

# 2. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.header("📋 مدخلات المشروع")
    elem = st.selectbox("اختر العنصر:", ["جائز (Beam)", "بلاطة مصمتة (Slab)", "أساسات (Footing)", "أعمدة (Column)"])
    
    st.divider()
    L = st.number_input("طول البحر L (m):", 1.0, 15.0, 5.0)
    h = st.number_input("السماكة h (cm):", 10, 150, 60)
    wu = st.number_input("الحمل Wu (t/m):", 0.1, 50.0, 2.5)
    
    st.divider()
    st.subheader("⚙️ خيارات التسليح")
    # أنت تختار القطر والبرنامج يحسب العدد
    phi = st.selectbox("اختر قطر السيخ (mm):", [8, 10, 12, 14, 16, 18, 20, 25], index=3)
    
    st.divider()
    fcu = 250
    fy = 4000

# 3. المحرك الحسابي
d = h - 5
area_single_bar = (np.pi * (phi/10)**2) / 4

# 4. عرض النتائج والرسومات
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📑 النتائج الحسابية")
    
    if elem in ["جائز (Beam)", "بلاطة مصمتة (Slab)"]:
        Mu = (wu * L**2) / 8
        As = (Mu * 100000) / (0.87 * fy * d)
        num_bars = int(np.ceil(As / area_single_bar))
        
        st.latex(r"M_u = \frac{w_u \cdot L^2}{8} = " + f"{Mu:.2f} " + r"\text{ t.m}")
        st.latex(r"A_s = \frac{M_u}{0.87 \cdot f_y \cdot d} = " + f"{As:.2f} " + r"\text{ cm}^2")
        
        st.success(f"النتيجة: استخدام {max(num_bars, 2)} قضبان بقطر {phi} مم ( {max(num_bars, 2)} T{phi} )")

    elif elem == "أساسات (Footing)":
        area = (wu / 2.0) * 1.1
        side = np.sqrt(area)
        As_f = 0.0015 * side * 100 * d # تسليح أدنى تقريبي
        num_bars = int(np.ceil(As_f / area_single_bar))
        
        st.success(f"مساحة القاعدة المطلوبة: {area:.2f} m2")
        st.info(f"الأبعاد المقترحة: {side:.2f} x {side:.2f} m")
        st.write(f"التسليح المقترح للقاعدة: {max(num_bars, 5)} T{phi} لكل متر")

    elif elem == "أعمدة (Column)":
        area_col = 30 * h
        capacity = (0.35 * fcu * area_col + 0.67 * fy * (0.01 * area_col)) / 1000
        # تسليح العمود 1%
        As_col = 0.01 * area_col
        num_bars = int(np.ceil(As_col / area_single_bar))
        
        st.success(f"قدرة تحمل العمود: {capacity:.1f} Ton")
        st.info(f"تسليح العمود المقترح: {max(num_bars, 4)} T{phi}")

with col2:
    st.subheader("🖼️ المخطط الإنشائي")
    if elem == "جائز (Beam)":
        
        st.caption("مخطط تفريد حديد الجائز")
    elif elem == "بلاطة مصمتة (Slab)":
        
        st.caption("مخطط تسليح البلاطة (الفرش والغطاء)")
    elif elem == "أساسات (Footing)":
        
        st.caption("تفاصيل تسليح القاعدة المنفردة")
    else:
        
        st.caption("مقطع عرضي في العمود يوضح الأساور والقضبان")

st.divider()
st.write("✅ **Pelan Engineering Suite - المذكرة الحسابية للمهندس بيلان عبد الكريم**")
