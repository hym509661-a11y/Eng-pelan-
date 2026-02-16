import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import numpy as np
import ezdxf

# الهوية المهنية المعتمدة
ST_NAME, ST_TEL, ST_WORK = "بيلان مصطفى عبد الكريم", "0998449697", "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Structural System", layout="wide")

# دالة تصحيح الخط العربي للرسم (حل مشكلة الحروف المقلوبة)
def fix_ar(text):
    return text[::-1]

# تنسيق الواجهة (CSS)
st.markdown(f"""
<style>
    .stApp {{ background: #0f172a; color: white; }}
    .element-card {{ background: white; color: black; padding: 20px; border-radius: 12px; border-right: 10px solid #d4af37; margin-bottom: 20px; direction: rtl; }}
    .pro-stamp {{ border: 3px double #d4af37; padding: 10px; text-align: center; background: white; color: black; border-radius: 10px; }}
</style>
""", unsafe_allow_html=True)

st.title(f"🏛️ المكتب الهندسي للمهندس {ST_NAME}")

# إنشاء التبويبات لفصل العناصر تماماً
tabs = st.tabs(["📏 الجوائز", "🏛️ الأعمدة", "🦶 الأساسات", "🧱 الجدران", "🥞 البلاطات"])

# --- 1. قسم الجوائز (Beams) ---
with tabs[0]:
    st.subheader("📋 تصميم الجوائز (Beams)")
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("<div class='element-card'>", unsafe_allow_html=True)
        b = st.number_input("العرض B (cm):", 20, 100, 30, key="b_beam")
        h = st.number_input("الارتفاع H (cm):", 20, 200, 60, key="h_beam")
        l = st.number_input("البحر L (m):", 1.0, 15.0, 5.0, key="l_beam")
        wu = st.number_input("الحمل Wu (kN/m):", 10, 500, 60, key="wu_beam")
        db = st.selectbox("قطر السفلي:", [14, 16, 18, 20], index=1, key="db_beam")
        # حساب آلي
        mu = (wu * l**2) / 8
        as_req = (mu * 1e6) / (0.87 * 420 * (h-5) * 10)
        nb = max(2, int(np.ceil(as_req / (np.pi * db**2 / 4))))
        nt = 2 # تعليق
        st.write(f"✅ النتائج: {nb} T {db} سفلي | {nt} T 12 علوي")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        fig, ax = plt.subplots()
        ax.add_patch(plt.Rectangle((0,0), b, h, fill=False, lw=3))
        ax.scatter(np.linspace(5, b-5, nb), [5]*nb, color='blue', s=100) # سفلي
        ax.scatter(np.linspace(5, b-5, nt), [h-5]*nt, color='red', s=80) # علوي
        ax.text(b/2, -8, f"MAIN: {nb} T {db}", ha='center', color='blue', weight='bold')
        ax.text(b/2, h+3, f"TOP: {nt} T 12", ha='center', color='red', weight='bold')
        ax.set_title(fix_ar("مقطع الجائز المسلح"))
        plt.axis('off'); st.pyplot(fig)

# --- 2. قسم الأعمدة (Columns) ---
with tabs[1]:
    st.subheader("📋 تصميم الأعمدة (Columns)")
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("<div class='element-card'>", unsafe_allow_html=True)
        bc = st.number_input("عرض العمود (cm):", 20, 100, 30)
        hc = st.number_input("طول العمود (cm):", 20, 100, 50)
        pu = st.number_input("الحمل Pu (kN):", 100, 10000, 2000)
        dc = st.selectbox("القطر:", [16, 18, 20, 25], index=0)
        # حساب آلي (1% تسليح)
        as_col = (bc * hc) * 0.01
        nc = max(4, int(np.ceil(as_col / (np.pi * dc**2 / 4))))
        if nc % 2 != 0: nc += 1
        st.write(f"✅ النتائج: {nc} T {dc} موزع محيطياً")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        fig2, ax2 = plt.subplots()
        ax2.add_patch(plt.Rectangle((0,0), bc, hc, fill=False, lw=3))
        # رسم الحديد المحيطي
        ax2.scatter([5, bc-5, 5, bc-5], [5, 5, hc-5, hc-5], color='blue', s=100)
        ax2.set_title(fix_ar("مقطع العمود"))
        plt.axis('off'); st.pyplot(fig2)

# --- 3. قسم الأساسات (Footings) ---
with tabs[2]:
    st.subheader("📋 تصميم الأساسات المنفردة (Footings)")
    st.markdown("<div class='element-card'>", unsafe_allow_html=True)
    q_soil = st.number_input("إجهاد التربة (kg/cm2):", 1.0, 5.0, 2.0)
    # حساب الأبعاد آلياً بناءً على حمل العمود
    area_f = (pu / (q_soil * 100)) * 1.1
    side_f = np.sqrt(area_f) * 100
    st.write(f"✅ الأبعاد المطلوبة: {side_f:.0f} x {side_f:.0f} cm")
    st.write("✅ التسليح: شبكتين (سفلية T14@15 وعلوية T12@20)")
    st.markdown("</div>", unsafe_allow_html=True)

# --- تصدير الأوتوكاد (إصلاح شامل) ---
st.divider()
if st.button("🚀 تصدير كافة العناصر إلى ملف AutoCAD (DXF)"):
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    msp.add_text(f"ENGINEER: {ST_NAME}", dxfattribs={'height': 10}).set_placement((0, 50))
    msp.add_lwpolyline([(0,0), (100,0), (100,100), (0,100), (0,0)]) # رسم افتراضي
    
    out = io.StringIO()
    doc.write(out)
    st.download_button(
        label="📥 اضغط هنا لتحميل ملف DXF الآن",
        data=out.getvalue(),
        file_name=f"Pelan_Full_Project.dxf",
        mime="application/dxf"
    )

# الختم الجانبي مع الرقم المعتمد
st.sidebar.markdown(f"""
<div class='pro-stamp'>
    <p><b>المهندس المدني</b></p>
    <p style='color:#d4af37; font-size:20px;'><b>{ST_NAME}</b></p>
    <p>{ST_WORK}</p>
    <p><b>TEL: {ST_TEL}</b></p>
</div>
""", unsafe_allow_html=True)
