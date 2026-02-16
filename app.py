import streamlit as st
import pandas as pd
import numpy as np
import ezdxf
import io

# البيانات الثابتة للمهندس بيلان
ST_NAME = "بيلان مصطفى عبد الكريم"
ST_TEL = "0998449697"
ST_WORK = "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v109", layout="wide")

# تصميم الواجهة المهنية
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(135deg, #1a1c2c, #4a192c); color: white; }}
    .calc-card {{ background: #ffffff; color: #1a1a1a; padding: 20px; border-radius: 15px; direction: rtl; border-right: 10px solid #d4af37; margin-bottom: 20px; }}
    .pro-stamp {{ border: 3px solid #d4af37; padding: 10px; width: 280px; text-align: center; background: white; color: black; float: left; border-radius: 10px; }}
</style>
""", unsafe_allow_html=True)

st.title(f"🏗️ مكتب {ST_NAME} الهندسي")

# نظام التبويبات لفصل العناصر الإنشائية تماماً
tab1, tab2, tab3 = st.tabs(["📏 الجوائز (Beams)", "🏛️ الأعمدة (Columns)", "🦶 الأساسات (Footings)"])

# ---------------------------------------------------------
# الجزء الأول: الجوائز (Beams)
# ---------------------------------------------------------
with tab1:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📑 تصميم الجوائز")
        b = st.number_input("العرض B (cm):", 20, 100, 30, key="b_b")
        h = st.number_input("الارتفاع H (cm):", 20, 200, 60, key="h_b")
        l = st.number_input("البحر L (m):", 1.0, 15.0, 5.0, key="l_b")
        w = st.number_input("الحمل q (kN/m):", 1.0, 300.0, 50.0, key="w_b")
        
        # الحسابات الهندسية
        mu = (w * l**2) / 8
        as_req = (mu * 1e6) / (0.87 * 420 * (h-5) * 10)
        n_bot = max(2, int(np.ceil(as_req / (np.pi * 16**2 / 4)))) # افتراض قطر 16
        
        st.write(f"🔹 العزم: {mu:.2f} kNm")
        st.write(f"✅ التسليح السفلي: {n_bot} T 16")
        st.write(f"✅ حديد التعليق: 2 T 12")
        st.write(f"✅ الكانات: T 8 @ 15 cm")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("📊 تصدير الجوائز")
        # تصدير Excel للجوائز
        try:
            df_b = pd.DataFrame({"Item": ["Beam", "B", "H", "Main Steel", "Hanger"], "Value": ["Concrete Beam", b, h, f"{n_bot}T16", "2T12"]})
            buf_ex = io.BytesIO()
            df_b.to_excel(buf_ex, index=False, engine='xlsxwriter')
            st.download_button("📥 تحميل مذكرة الجائز (Excel)", buf_ex.getvalue(), "Beam_Report.xlsx")
        except: st.warning("تأكد من إضافة xlsxwriter في ملف الإعدادات")

        # تصدير AutoCAD (الرسم مع الكانات والتعليق)
        if st.button("🚀 رسم الجائز (AutoCAD)"):
            doc = ezdxf.new(setup=True); msp = doc.modelspace()
            s = 10 # scale
            w_mm, h_mm, cv = b*s, h*s, 25
            # رسم الخرسانة والكانة والحديد
            msp.add_lwpolyline([(0,0), (w_mm,0), (w_mm,h_mm), (0,h_mm), (0,0)], dxfattribs={'color': 7})
            msp.add_lwpolyline([(cv,cv), (w_mm-cv,cv), (w_mm-cv,h_mm-cv), (cv,h_mm-cv), (cv,cv)], dxfattribs={'color': 1})
            for i in range(n_bot): msp.add_circle((cv+10+i*20, cv+10), radius=8, dxfattribs={'color': 5})
            msp.add_circle((cv+10, h_mm-cv-10), radius=6, dxfattribs={'color': 5})
            msp.add_circle((w_mm-cv-10, h_mm-cv-10), radius=6, dxfattribs={'color': 5})
            
            buf_cad = io.StringIO(); doc.write(buf_cad)
            st.download_button("📥 تحميل مخطط DXF", buf_cad.getvalue(), "Beam_Final.dxf")

# ---------------------------------------------------------
# الجزء الثاني: الأعمدة (Columns)
# ---------------------------------------------------------
with tab2:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📑 تصميم الأعمدة")
        ac = st.number_input("الحمل المحوري (kN):", 100, 5000, 1200)
        bc = st.number_input("عرض العمود (cm):", 20, 100, 30)
        hc = st.number_input("طول العمود (cm):", 20, 100, 50)
        st.write(f"✅ حديد التسليح: {max(4, int((bc*hc*0.01)/2))} T 16")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# الجزء الثالث: الأساسات (Footings)
# ---------------------------------------------------------
with tab3:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📑 تصميم الأساسات")
        q_soil = st.number_input("إجهاد التربة (kg/cm2):", 0.5, 4.0, 2.0)
        f_area = (1200 / 10) / q_soil # مثال تقريبي
        st.write(f"✅ الأبعاد المطلوبة: {np.sqrt(f_area):.1f} x {np.sqrt(f_area):.1f} cm")
        st.markdown("</div>", unsafe_allow_html=True)

# الختم الثابت في أسفل الصفحة
st.divider()
st.markdown(f"""
<div class='pro-stamp'>
    <p style='margin:0; font-weight:bold;'>المهندس المدني</p>
    <p style='color:#d4af37; font-size:20px; font-weight:bold; margin:5px 0;'>{ST_NAME}</p>
    <p style='margin:0; font-size:12px;'>{ST_WORK}</p>
    <p style='margin:5px 0; font-weight:bold;'>TEL: {ST_TEL}</p>
</div>
""", unsafe_allow_html=True)

# الصور التوضيحية
