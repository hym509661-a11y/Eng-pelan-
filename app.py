import streamlit as st
import pandas as pd  # المكتبة المسؤولة عن ملفات الاكسل
import numpy as np
import ezdxf
import io

# بيانات الهوية
ST_NAME, ST_TEL, ST_WORK = "بيلان مصطفى عبد الكريم", "0998449697", "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v101", layout="wide")

# تصميم الواجهة
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; }}
    .calc-card {{ background: white; color: black; padding: 20px; border-radius: 10px; direction: rtl; border-right: 10px solid #d4af37; }}
    .pro-stamp {{ border: 4px double #d4af37; padding: 10px; width: 300px; text-align: center; background: white; color: black; float: left; }}
</style>
""", unsafe_allow_html=True)

st.title("🏗️ نظام بيلان الهندسي - إصدار الجداول الذكية")

# فصل العناصر في تبويبات
tab1, tab2 = st.tabs(["📏 تصميم الجوائز", "🏛️ تصميم الأعمدة"])

# --- تبويب الجوائز ---
with tab1:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("المذكرة الحسابية")
        b = st.number_input("العرض (cm):", 20, 100, 30)
        h = st.number_input("الارتفاع (cm):", 20, 200, 60)
        l = st.number_input("الطول (m):", 1.0, 15.0, 5.0)
        q = st.number_input("الحمل (kN/m):", 1.0, 200.0, 40.0)
        phi = st.selectbox("قطر الحديد:", [14, 16, 18, 20])
        
        # حسابات
        m_max = (q * l**2) / 8
        n_bars = max(2, int(np.ceil((m_max * 1e6) / (0.87 * 420 * (h-5) * 10) / (np.pi * phi**2 / 4))))
        
        st.write(f"العزم الأقصى: {m_max:.2f} kNm")
        st.write(f"التسليح السفلي: {n_bars} T {phi}")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        
        
        # --- زر تصدير الاكسل (Excel) ---
        st.subheader("📊 تصدير البيانات")
        
        # تجهيز البيانات للجدول
        data = {
            "العنصر": ["جائز خرساني"],
            "العرض B (cm)": [b],
            "الارتفاع H (cm)": [h],
            "الطول L (m)": [l],
            "العزم Mu (kNm)": [round(m_max, 2)],
            "الحديد السفلي": [f"{n_bars} T {phi}"],
            "حديد التعليق": ["2 T 12"],
            "المهندس المصمم": [ST_NAME],
            "هاتف": [ST_TEL]
        }
        df = pd.DataFrame(data)

        # تحويل البيانات إلى ملف Excel في الذاكرة
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Design_Report')
        excel_data = output.getvalue()

        st.download_button(
            label="📥 تحميل المذكرة الحسابية (Excel)",
            data=excel_data,
            file_name=f"Pelan_Report_{phi}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # الختم
        st.markdown(f"""<div class='pro-stamp'><p><b>المهندس المدني</b></p><p style='color:#d4af37; font-size:20px;'><b>{ST_NAME}</b></p>
        <p>{ST_WORK}</p><p>TEL: {ST_TEL}</p></div>""", unsafe_allow_html=True)

# --- محرك الأوتوكاد (DXF) يبقى كما هو ---
st.divider()
st.info("ملاحظة: زر التحميل أعلاه يصدر لك ملف Excel حقيقي يحتوي على كافة النتائج والأرقام.")
