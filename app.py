import streamlit as st
import pandas as pd
import numpy as np
import ezdxf
import io

# البيانات الشخصية
NAME, TEL = "بيلان مصطفى عبد الكريم", "0998449697"
WORK = "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v105", layout="wide")

# التصميم الفخم
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(135deg, #0f2027, #2c5364); color: white; }}
    .calc-card {{ background: white; color: black; padding: 25px; border-radius: 12px; direction: rtl; border-right: 10px solid #d4af37; }}
    .stamp-box {{ border: 4px double #d4af37; padding: 10px; width: 300px; text-align: center; background: white; color: black; float: left; margin-top: 20px; }}
</style>
""", unsafe_allow_html=True)

st.title("🏗️ المكتب الهندسي الذكي - الإصدار v105")

# تبويبات منفصلة
tab_names = ["الجوائز (Beams)", "الأعمدة (Columns)", "الأساسات (Footings)"]
tabs = st.tabs(tab_names)

# --- محرك الجوائز ---
with tabs[0]:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📑 المذكرة الحسابية")
        b = st.number_input("العرض B (cm):", 20, 100, 30, key="b_beam")
        h = st.number_input("الارتفاع H (cm):", 20, 200, 60, key="h_beam")
        l = st.number_input("البحر L (m):", 1.0, 20.0, 5.0, key="l_beam")
        w = st.number_input("الحمل q (kN/m):", 1.0, 300.0, 50.0, key="w_beam")
        
        mu = (w * l**2) / 8
        as_req = (mu * 1e6) / (0.87 * 420 * (h-5) * 10)
        n_bot = max(2, int(np.ceil(as_req / (np.pi * 16**2 / 4))))
        
        st.divider()
        st.write(f"العزم التصميمي: {mu:.2f} kNm")
        st.write(f"الحديد السفلي: {n_bot} T 16")
        st.write(f"الحديد العلوي: 2 T 12")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("📊 التصدير والاعتماد")
        
        # تصدير Excel
        try:
            df = pd.DataFrame({
                "المعلمة": ["العنصر", "الأبعاد", "العزم", "التسليح"],
                "القيمة": ["جائز", f"{b}x{h}", f"{mu:.2f}", f"{n_bot}T16 + 2T12"]
            })
            towrite = io.BytesIO()
            df.to_excel(towrite, index=False, engine='xlsxwriter')
            st.download_button("📥 تحميل المذكرة (Excel)", towrite.getvalue(), "Report.xlsx")
        except:
            st.warning("يرجى مراجعة ملف requirements.txt")

        # تصدير AutoCAD
        if st.button("🚀 إنشاء مخطط أوتوكاد"):
            doc = ezdxf.new(setup=True); msp = doc.modelspace()
            msp.add_lwpolyline([(0,0), (b*10,0), (b*10,h*10), (0,h*10), (0,0)], dxfattribs={'color': 7})
            msp.add_text(f"ENG. {NAME}", dxfattribs={'height': 20}).set_placement((0, h*10 + 50))
            out_cad = io.StringIO()
            doc.write(out_cad)
            st.download_button("📥 تحميل الرسم (DXF)", out_cad.getvalue(), "Drawing.dxf")

        # الختم المهني
        st.markdown(f"""<div class='stamp-box'><p><b>المهندس المدني</b></p>
        <p style='color:#d4af37; font-size:20px;'><b>{NAME}</b></p>
        <p style='font-size:14px;'>{WORK}</p><b>{TEL}</b></div>""", unsafe_allow_html=True)

# الرسوم التوضيحية
