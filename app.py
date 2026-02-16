import streamlit as st
import pandas as pd
import numpy as np
import ezdxf
import io

# بيانات الهوية المهنية للمهندس بيلان
ST_NAME, ST_TEL, ST_WORK = "بيلان مصطفى عبد الكريم", "0998449697", "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v110", layout="wide")

# تصميم الواجهة الاحترافية
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; }}
    .calc-card {{ background: white; color: black; padding: 25px; border-radius: 15px; direction: rtl; border-right: 12px solid #d4af37; }}
    .stamp-box {{ border: 4px double #d4af37; padding: 12px; width: 300px; text-align: center; background: white; color: black; float: left; margin-top: 20px; }}
</style>
""", unsafe_allow_html=True)

st.title(f"🏛️ نظام {ST_NAME} الهندسي v110")

# نظام التبويبات لفصل العناصر تماماً
tab1, tab2, tab3 = st.tabs(["📏 الجوائز (Beams)", "🏛️ الأعمدة (Columns)", "🦶 الأساسات (Footings)"])

# ---------------------------------------------------------
# الجزء الأول: الجوائز (مع إضافة الحديد العلوي والكانات)
# ---------------------------------------------------------
with tab1:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📑 المذكرة الحسابية للجائز")
        b = st.number_input("العرض B (cm):", 20, 100, 30, key="b_b")
        h = st.number_input("الارتفاع H (cm):", 20, 200, 60, key="h_b")
        l = st.number_input("البحر L (m):", 1.0, 15.0, 5.0, key="l_b")
        w = st.number_input("الحمل q (kN/m):", 1.0, 300.0, 50.0, key="w_b")
        
        # مدخلات التسليح
        phi_main = st.selectbox("قطر الحديد السفلي (mm):", [14, 16, 18, 20], index=1)
        phi_top = st.selectbox("قطر الحديد العلوي (mm):", [10, 12, 14, 16], index=1)
        
        # الحسابات
        mu = (w * l**2) / 8
        vu = (w * l) / 2
        as_req = (mu * 1e6) / (0.87 * 420 * (h-5) * 10)
        n_bot = max(2, int(np.ceil(as_req / (np.pi * phi_main**2 / 4))))
        n_top = 2 # حديد تعليق افتراضي
        
        st.divider()
        st.write(f"📊 العزم الأقصى: {mu:.2f} kNm")
        st.write(f"✅ التسليح السفلي: {n_bot} T {phi_main}")
        st.write(f"✅ التسليح العلوي: {n_top} T {phi_top}")
        st.write(f"✅ الكانات: T 8 @ 15 cm")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("🖼️ الرسم التوضيحي وتصدير المخططات")
        
        # رسم توضيحي دقيق للمقطع (Image Placeholder)
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Reinforced_concrete_beam_design.png/300px-Reinforced_concrete_beam_design.png", caption="توزيع حديد التسليح في المقطع")

        # تصدير Excel (المذكرة الحسابية كاملة)
        try:
            df = pd.DataFrame({
                "المعلمة": ["العرض (cm)", "الارتفاع (cm)", "الطول (m)", "العزم (kNm)", "الحديد السفلي", "الحديد العلوي", "الكانات"],
                "القيمة": [b, h, l, f"{mu:.2f}", f"{n_bot} T {phi_main}", f"{n_top} T {phi_top}", "T 8 @ 15cm"]
            })
            buf_ex = io.BytesIO()
            with pd.ExcelWriter(buf_ex, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Beam_Design')
            st.download_button("📥 تحميل المذكرة الحسابية (Excel)", buf_ex.getvalue(), f"Beam_{ST_NAME}.xlsx")
        except:
            st.warning("⚠️ يرجى إضافة xlsxwriter في ملف requirements.txt")

        # تصدير AutoCAD (الرسم الإنشائي الكامل)
        if st.button("🚀 توليد مخطط AutoCAD (DXF)"):
            doc = ezdxf.new(setup=True); msp = doc.modelspace()
            s = 10 # mm scale
            w_mm, h_mm, cv = b*s, h*s, 25
            
            # 1. رسم الخرسانة
            msp.add_lwpolyline([(0,0), (w_mm,0), (w_mm,h_mm), (0,h_mm), (0,0)], dxfattribs={'color': 7})
            # 2. رسم الكانة
            msp.add_lwpolyline([(cv,cv), (w_mm-cv,cv), (w_mm-cv,h_mm-cv), (cv,h_mm-cv), (cv,cv)], dxfattribs={'color': 1})
            # 3. رسم الحديد السفلي
            gap = (w_mm - 2*cv - 20) / (n_bot - 1 if n_bot > 1 else 1)
            for i in range(n_bot):
                msp.add_circle((cv + 10 + i*gap, cv + 10), radius=phi_main/2, dxfattribs={'color': 5})
            # 4. رسم الحديد العلوي (التعليق)
            msp.add_circle((cv + 10, h_mm - cv - 10), radius=phi_top/2, dxfattribs={'color': 3})
            msp.add_circle((w_mm - cv - 10, h_mm - cv - 10), radius=phi_top/2, dxfattribs={'color': 3})
            
            msp.add_text(f"DESIGN: ENG. {ST_NAME}", dxfattribs={'height': 20}).set_placement((0, h_mm + 50))
            
            buf_cad = io.StringIO(); doc.write(buf_cad)
            st.download_button("📥 تحميل مخطط AutoCAD", buf_cad.getvalue(), "Structural_Drawing.dxf")

# ---------------------------------------------------------
# الجزء الثاني والثالث (أعمدة وأساسات) مفصولة تماماً
# ---------------------------------------------------------
with tab2:
    st.info("قسم تصميم الأعمدة قيد الحسابات المنفصلة...")
with tab3:
    st.info("قسم تصميم الأساسات قيد الحسابات المنفصلة...")

# الختم الرسمي
st.divider()
st.markdown(f"""
<div class='stamp-box'>
    <p style='margin:0; font-weight:bold;'>المهندس المدني</p>
    <p style='color:#d4af37; font-size:22px; font-weight:bold; margin:5px 0;'>{ST_NAME}</p>
    <p style='margin:0; font-size:14px;'>{ST_WORK}</p>
    <p style='margin:5px 0; font-weight:bold; color:#d4af37;'>TEL: {ST_TEL}</p>
</div>
""", unsafe_allow_html=True)
