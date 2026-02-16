import streamlit as st
import pandas as pd
import numpy as np
import ezdxf
import io
import matplotlib.pyplot as plt

# الهوية المهنية المعتمدة
ST_NAME, ST_TEL, ST_WORK = "بيلان مصطفى عبد الكريم", "0998449697", "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v114", layout="wide")

# تصميم الواجهة (CSS الاحترافي)
st.markdown(f"""
<style>
    .stApp {{ background: #0e1117; color: white; }}
    .calc-card {{ background: white; color: black; padding: 20px; border-radius: 12px; direction: rtl; border-right: 10px solid #d4af37; margin-bottom: 15px; }}
    .pro-stamp {{ border: 3px double #d4af37; padding: 10px; width: 280px; text-align: center; background: white; color: black; border-radius: 10px; }}
</style>
""", unsafe_allow_html=True)

st.title(f"🏛️ المكتب الهندسي المتكامل | {ST_NAME}")

# تبويبات فصل العناصر
tab_beam, tab_col, tab_foot = st.tabs(["📏 الجوائز (Beams)", "🏛️ الأعمدة (Columns)", "🦶 الأساسات (Footings)"])

# ---------------------------------------------------------
# 1. قسم الجوائز (Beams) - حمولات وتفاصيل تسليح
# ---------------------------------------------------------
with tab_beam:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📥 مدخلات الجائز والحمولات")
        b_b = st.number_input("العرض B (cm):", 20, 100, 30, key="b_b")
        h_b = st.number_input("الارتفاع H (cm):", 20, 200, 60, key="h_b")
        l_b = st.number_input("البحر L (m):", 1.0, 15.0, 5.0, key="l_b")
        
        st.write("⚙️ **الحمولات الموزعة (kN/m):**")
        dl_b = st.number_input("الحمل الميت (DL):", 0.0, 200.0, 25.0, key="dl_b")
        ll_b = st.number_input("الحمل الحي (LL):", 0.0, 200.0, 15.0, key="ll_b")
        wu_b = (1.4 * dl_b) + (1.7 * ll_b)
        
        mu = (wu_b * l_b**2) / 8
        as_req = (mu * 1e6) / (0.87 * 420 * (h_b-5) * 10)
        n_bot = max(2, int(np.ceil(as_req / (np.pi * 16**2 / 4))))
        
        st.success(f"الحمل التصميمي: {wu_b:.2f} kN/m")
        st.write(f"✅ التسليح: {n_bot} T 16 سفلي | 2 T 12 علوي")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.subheader("🖼️ مقطع الجائز")
        fig, ax = plt.subplots(figsize=(3, 4))
        ax.add_patch(plt.Rectangle((0, 0), b_b, h_b, fill=False, color='black', lw=3))
        ax.add_patch(plt.Rectangle((3, 3), b_b-6, h_b-6, fill=False, color='red', lw=1, ls='--'))
        for i in range(n_bot): ax.scatter([6+i*(b_b-12)/(n_bot-1)], [6], color='blue')
        ax.set_aspect('equal'); plt.axis('off'); st.pyplot(fig)

# ---------------------------------------------------------
# 2. قسم الأعمدة (Columns) - حمولات مركزة وتسليح محيطي
# ---------------------------------------------------------
with tab_col:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📥 حمولات وأبعاد العمود")
        b_c = st.number_input("العرض (cm):", 20, 100, 30, key="b_c")
        h_c = st.number_input("الطول (cm):", 20, 200, 50, key="h_c")
        
        st.write("⚙️ **الحمولات المركزة (kN):**")
        dl_c = st.number_input("حمل ميت مركز (DL):", 0, 5000, 800, key="dl_c")
        ll_c = st.number_input("حمل حي مركز (LL):", 0, 5000, 400, key="ll_c")
        pu = (1.4 * dl_c) + (1.7 * ll_c)
        
        # تسليح افتراضي 1% من مساحة المقطع
        as_c = (b_c * h_c) * 0.01
        n_c = max(4, int(np.ceil(as_c / (np.pi * 16**2 / 4))))
        if n_c % 2 != 0: n_c += 1
        
        st.success(f"الحمل المحوري Pu: {pu:.2f} kN")
        st.write(f"✅ التسليح الطولي: {n_c} T 16")
        st.write(f"✅ الكانات: T 8 @ 15 cm")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with c2:
        st.subheader("🖼️ مقطع العمود")
        fig2, ax2 = plt.subplots(figsize=(3, 4))
        ax2.add_patch(plt.Rectangle((0, 0), b_c, h_c, fill=False, color='black', lw=3))
        ax2.scatter([5, b_c-5, 5, b_c-5], [5, 5, h_c-5, h_c-5], color='blue')
        ax2.set_aspect('equal'); plt.axis('off'); st.pyplot(fig2)

# ---------------------------------------------------------
# 3. قسم الأساسات (Footings) - ضغط التربة وتسليح شبكي
# ---------------------------------------------------------
with tab_foot:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📥 حمولات التربة والأساس")
        q_allow = st.number_input("إجهاد التربة المسموح (kg/cm2):", 0.5, 5.0, 2.0)
        
        # حساب المساحة المطلوبة بناءً على حمل العمود السابق
        area_req = (pu / (q_allow * 100)) * 1.1 # 10% زيادة لوزن الأساس
        dim = np.sqrt(area_req) * 100 # تحويل لـ cm
        
        st.success(f"المساحة المطلوبة: {area_req:.2f} m2")
        st.write(f"✅ الأبعاد المقترحة: {dim:.0f} x {dim:.0f} cm")
        st.write(f"✅ التسليح: شبكة T 14 @ 15 cm")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# التصدير والختم
# ---------------------------------------------------------
st.divider()
if st.button("🚀 توليد مخطط AutoCAD للمشروع كامل"):
    st.info("جاري تجهيز ملف DXF لكافة العناصر...")

st.sidebar.markdown(f"""
<div class='pro-stamp'>
    <p><b>المهندس المدني</b></p>
    <p style='color:#d4af37; font-size:20px;'><b>{ST_NAME}</b></p>
    <p>{ST_WORK}</p>
    <p><b>TEL: {ST_TEL}</b></p>
</div>
""", unsafe_allow_html=True)
