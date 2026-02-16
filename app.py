import streamlit as st
import pandas as pd
import numpy as np
import ezdxf
import io

# الهوية المهنية للمهندس بيلان
NAME, TEL = "بيلان مصطفى عبد الكريم", "0998449697"
WORK_INFO = "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v106", layout="wide")

# تصميم الواجهة الراقية
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(135deg, #0f2027, #2c5364); color: white; }}
    .calc-card {{ background: white; color: black; padding: 25px; border-radius: 12px; direction: rtl; border-right: 12px solid #d4af37; }}
    .stamp-box {{ border: 4px double #d4af37; padding: 10px; width: 300px; text-align: center; background: white; color: black; float: left; margin-top: 20px; }}
</style>
""", unsafe_allow_html=True)

st.title("🏗️ المكتب الهندسي - الإصدار الاحترافي v106")

# تبويبات منفصلة لكل عنصر إنشائي
tabs = st.tabs(["📏 الجوائز (Beams)", "🏛️ الأعمدة (Columns)", "🦶 الأساسات (Footings)"])

# محرك الجوائز (مثال)
with tabs[0]:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📑 المذكرة الحسابية")
        b_val = st.number_input("العرض B (cm):", 20, 100, 30, key="b_b")
        h_val = st.number_input("الارتفاع H (cm):", 20, 200, 60, key="h_b")
        l_val = st.number_input("البحر L (m):", 1.0, 20.0, 5.0, key="l_b")
        w_val = st.number_input("الحمل q (kN/m):", 1.0, 300.0, 50.0, key="w_b")
        
        # الحسابات
        mu = (w_val * l_val**2) / 8
        vu = (w_val * l_val) / 2
        as_req = (mu * 1e6) / (0.87 * 420 * (h_val-5) * 10)
        n_bot = max(2, int(np.ceil(as_req / (np.pi * 16**2 / 4))))
        
        st.divider()
        st.write(f"📊 العزم التصميمي: {mu:.2f} kNm")
        st.write(f"📊 قوة القص: {vu:.2f} kN")
        st.write(f"✅ التسليح السفلي: {n_bot} T 16")
        st.write(f"✅ الحديد العلوي: 2 T 12")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("📊 تصدير المذكرة والرسوم")
        
        # زر الإكسل (Excel)
        try:
            df = pd.DataFrame({
                "المعلمة": ["العنصر", "المقطع", "البحر", "العزم Max", "التسليح"],
                "القيمة": ["جائز خرساني", f"{b_val}x{h_val}", f"{l_val}m", f"{mu:.2f}", f"{n_bot}T16+2T12"]
            })
            towrite = io.BytesIO()
            df.to_excel(towrite, index=False, engine='xlsxwriter')
            st.download_button("📥 تحميل جدول الحصر (Excel)", towrite.getvalue(), "Structural_Report.xlsx")
        except:
            st.error("⚠️ يرجى إضافة xlsxwriter في ملف requirements.txt")

        # زر الأوتوكاد (DXF)
        if st.button("🚀 توليد مخطط AutoCAD"):
            doc = ezdxf.new(setup=True); msp = doc.modelspace()
            msp.add_lwpolyline([(0,0), (b_val*10,0), (b_val*10,h_val*10), (0,h_val*10), (0,0)], dxfattribs={'color': 7})
            msp.add_text(f"ENG. {NAME}", dxfattribs={'height': 20}).set_placement((0, h_val*10 + 50))
            out_cad = io.StringIO()
            doc.write(out_cad)
            st.download_button("📥 حفظ ملف الرسم (DXF)", out_cad.getvalue(), "Design_Detail.dxf")

        # الختم الرسمي
        st.markdown(f"""<div class='stamp-box'><p><b>المهندس المدني</b></p>
        <p style='color:#d4af37; font-size:20px;'><b>{NAME}</b></p>
        <p style='font-size:14px;'>{WORK_INFO}</p><b>{TEL}</b></div>""", unsafe_allow_html=True)

# الرسوم التوضيحية
