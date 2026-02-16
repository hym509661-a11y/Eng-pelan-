import streamlit as st
import pandas as pd
import numpy as np
import ezdxf
import io
import matplotlib.pyplot as plt

# الهوية المهنية للمهندس بيلان
ST_NAME, ST_TEL, ST_WORK = "بيلان مصطفى عبد الكريم", "0998449697", "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v112", layout="wide")

# تصميم الواجهة الاحترافية (CSS)
st.markdown(f"""
<style>
    .stApp {{ background: #0e1117; color: white; }}
    .calc-card {{ background: #ffffff; color: #1a1a1a; padding: 25px; border-radius: 15px; direction: rtl; border-right: 12px solid #d4af37; }}
    .pro-stamp {{ border: 3px double #d4af37; padding: 10px; width: 300px; text-align: center; background: white; color: black; float: left; border-radius: 10px; }}
</style>
""", unsafe_allow_html=True)

st.title(f"🏗️ المكتب الهندسي الرقمي | {ST_NAME}")

# فصل العناصر تماماً باستخدام التبويبات
tab_beam, tab_col, tab_foot = st.tabs(["📏 الجوائز", "🏛️ الأعمدة", "🦶 الأساسات"])

# --- 1. قسم الجوائز (Beams) ---
with tab_beam:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📑 معطيات وتسليح الجائز")
        b = st.number_input("العرض B (cm):", 20, 100, 30, key="b1")
        h = st.number_input("الارتفاع H (cm):", 20, 200, 60, key="h1")
        phi_main = st.selectbox("قطر السفلي (mm):", [14, 16, 18, 20], index=1)
        phi_top = st.selectbox("قطر العلوي (mm):", [10, 12, 14, 16], index=1)
        
        # حسابات سريعة
        n_bot = 4; n_top = 2 # قيم افتراضية للتوضيح
        st.write(f"✅ التسليح السفلي: {n_bot} T {phi_main}")
        st.write(f"✅ التسليح العلوي: {n_top} T {phi_top}")
        st.write(f"✅ الكانات: T 8 @ 15 cm")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.subheader("🖼️ المقطع الإنشائي الفوري")
        # توليد الرسمة داخلياً (حل مشكلة الصورة المكسورة)
        fig, ax = plt.subplots(figsize=(4, 5))
        ax.add_patch(plt.Rectangle((0, 0), b, h, fill=False, color='black', lw=4)) # خرسانة
        ax.add_patch(plt.Rectangle((3, 3), b-6, h-6, fill=False, color='red', lw=1.5)) # كانة
        # رسم الحديد
        for i in range(n_bot): ax.scatter([6 + i*(b-12)/(n_bot-1)], [6], color='blue', s=100)
        for i in range(n_top): ax.scatter([6 + i*(b-12)/(n_top-1)], [h-6], color='blue', s=80)
        ax.set_aspect('equal'); plt.axis('off')
        st.pyplot(fig) # الرسم سيظهر هنا فوراً

# --- 2. قسم الأعمدة (Columns) ---
with tab_col:
    st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
    st.subheader("📑 خصائص تسليح الأعمدة")
    col_b = st.number_input("عرض العمود (cm):", 20, 100, 30)
    col_h = st.number_input("طول العمود (cm):", 20, 200, 50)
    st.write("✅ التسليح الطولي المفصل: 8 T 16 موزع على المحيط")
    st.write("✅ الكانات: T 8 @ 15 cm مع أربطة داخلية")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 3. قسم الأساسات (Footings) ---
with tab_foot:
    st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
    st.subheader("📑 خصائص تسليح الأساسات")
    st.write("✅ الحصيرة التسليحية: T 14 @ 15 cm في الاتجاهين")
    st.write("✅ سمك الأساس: 50 cm مع تغطية خرسانية 5 cm")
    st.markdown("</div>", unsafe_allow_html=True)

# --- أزرار التصدير (حل مشكلة الإكسل والأوتوكاد) ---
st.divider()
col_ex, col_cad = st.columns(2)
with col_ex:
    if st.button("📥 تصدير المذكرة (Excel)"):
        try:
            buf = io.BytesIO()
            df = pd.DataFrame({"العنصر": ["جائز", "عمود"], "التسليح": ["4T16+2T12", "8T16"]})
            with pd.ExcelWriter(buf, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            st.download_button("اضغط لتحميل الإكسل", buf.getvalue(), "Pelan_Report.xlsx")
        except: st.error("⚠️ يرجى تحديث ملف requirements.txt")

with col_cad:
    if st.button("🚀 توليد مخطط AutoCAD"):
        doc = ezdxf.new(); msp = doc.modelspace()
        msp.add_lwpolyline([(0,0), (b*10,0), (b*10,h*10), (0,h*10), (0,0)])
        buf_cad = io.StringIO(); doc.write(buf_cad)
        st.download_button("تحميل ملف DXF", buf_cad.getvalue(), "Drawing.dxf")

# الختم الرسمي الثابت
st.markdown(f"""
<div class='pro-stamp'>
    <p>المهندس المدني</p>
    <p style='color:#d4af37; font-size:20px; font-weight:bold;'>{ST_NAME}</p>
    <p>{ST_WORK}</p>
    <p><b>TEL: {ST_TEL}</b></p>
</div>
""", unsafe_allow_html=True)
