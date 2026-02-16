import streamlit as st
import pandas as pd
import numpy as np
import ezdxf
import io

# الهوية المهنية
NAME, TEL = "بيلان مصطفى عبد الكريم", "0998449697"
WORK = "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v104", layout="wide")

# تصميم الواجهة الفخمة
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(135deg, #0f2027, #2c5364); color: white; }}
    .calc-card {{ background: white; color: black; padding: 25px; border-radius: 12px; direction: rtl; border-right: 12px solid #d4af37; }}
    .stamp-box {{ border: 4px double #d4af37; padding: 10px; width: 280px; text-align: center; background: white; color: black; float: left; margin-top: 20px; }}
</style>
""", unsafe_allow_html=True)

st.title("🏗️ المكتب الهندسي الذكي - v104")

# تبويبات منفصلة تماماً لكل عنصر
tab1, tab2, tab3 = st.tabs(["📏 الجوائز (Beams)", "🏛️ الأعمدة (Columns)", "🦶 الأساسات (Footings)"])

# --- تبويب الجوائز ---
with tab1:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📑 المذكرة الحسابية")
        b = st.number_input("العرض B (cm):", 20, 100, 30, key="b1")
        h = st.number_input("الارتفاع H (cm):", 20, 200, 60, key="h1")
        l = st.number_input("البحر L (m):", 1.0, 15.0, 5.0, key="l1")
        w = st.number_input("الحمل q (kN/m):", 1.0, 250.0, 50.0, key="w1")
        
        # الحسابات الهندسية
        mu = (w * l**2) / 8
        vu = (w * l) / 2
        as_req = (mu * 1e6) / (0.87 * 420 * (h-5) * 10)
        n_bot = max(2, int(np.ceil(as_req / (np.pi * 16**2 / 4))))
        
        st.divider()
        st.write(f"العزم التصميمي: {mu:.2f} kNm")
        st.write(f"قوة القص: {vu:.2f} kN")
        st.write(f"الحديد السفلي: {n_bot} T 16")
        st.write(f"الحديد العلوي: 2 T 12")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("📊 تصدير البيانات والرسوم")
        
        # تصدير EXCEL (حل مشكلة الصورة 6)
        try:
            df = pd.DataFrame({
                "Parameter": ["Element", "Dimensions", "Span", "Max Moment", "Bottom Steel", "Top Steel"],
                "Value": ["Beam", f"{b}x{h} cm", f"{l} m", f"{mu:.2f} kNm", f"{n_bot} T 16", "2 T 12"]
            })
            towrite = io.BytesIO()
            df.to_excel(towrite, index=False, engine='xlsxwriter')
            towrite.seek(0)
            st.download_button("📥 تحميل جدول الحصر (Excel)", towrite, "Pelan_Report.xlsx")
        except:
            st.error("يرجى التأكد من إضافة xlsxwriter في ملف الإعدادات")

        # تصدير AutoCAD (حل الصورة 4)
        if st.button("🚀 توليد مخطط أوتوكاد"):
            doc = ezdxf.new(setup=True); msp = doc.modelspace()
            msp.add_lwpolyline([(0,0), (b*10,0), (b*10,h*10), (0,h*10), (0,0)], dxfattribs={'color': 7})
            msp.add_text(f"ENG. {NAME} - {TEL}", dxfattribs={'height': 20}).set_placement((0, h*10 + 40))
            out_cad = io.StringIO()
            doc.write(out_cad)
            st.download_button("📥 حفظ ملف DXF للرسم", out_cad.getvalue(), "Structural_Detail.dxf")

        # الختم
        st.markdown(f"""<div class='stamp-box'><p><b>المهندس المدني</b></p>
        <p style='color:#d4af37; font-size:18px;'><b>{NAME}</b></p>
        <p style='font-size:12px;'>{WORK}</p><b>{TEL}</b></div>""", unsafe_allow_html=True)

# الرسوم التوضيحية الإنشائية
