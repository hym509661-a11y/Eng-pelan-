import streamlit as st
import pandas as pd
import numpy as np
import ezdxf
import io

# بيانات الهوية
NAME, TEL = "بيلان مصطفى عبد الكريم", "0998449697"
WORK = "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan v102", layout="wide")

# تصميم الخلفية الراقية
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(135deg, #0f2027, #2c5364); color: white; }}
    .main-box {{ background: white; color: black; padding: 25px; border-radius: 12px; direction: rtl; border-right: 10px solid #d4af37; }}
    .stamp {{ border: 4px double #d4af37; padding: 12px; width: 300px; text-align: center; background: white; color: black; float: left; margin-top: 20px; }}
</style>
""", unsafe_allow_html=True)

st.title("🏛️ نظام بيلان الهندسي - المذكرة والرسوم والجداول")

# فصل العناصر
tabs = st.tabs(["الجوائز", "الأعمدة", "الأساسات", "البلاطات"])

# --- محرك الحساب (للجوائز كمثال) ---
with tabs[0]:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("<div class='main-box'>", unsafe_allow_html=True)
        st.subheader("📑 المذكرة الحسابية")
        b = st.number_input("العرض (cm):", 20, 100, 30, key="b")
        h = st.number_input("الارتفاع (cm):", 20, 200, 60, key="h")
        l = st.number_input("البحر (m):", 1.0, 15.0, 5.0, key="l")
        w = st.number_input("الحمل (kN/m):", 1.0, 200.0, 45.0, key="w")
        
        # حسابات تلقائية
        mu = (w * l**2) / 8
        as_req = (mu * 1e6) / (0.87 * 420 * (h-5) * 10)
        n = max(2, int(np.ceil(as_req / (np.pi * 16**2 / 4)))) # افتراض قطر 16
        
        st.write(f"العزم: {mu:.2f} kNm")
        st.write(f"التسليح السفلي: {n} T 16")
        st.write(f"التسليح العلوي: 2 T 12")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.subheader("📊 تصدير الجداول والمخططات")
        
        # 1. تصدير Excel (جداول حصر ومذكرة)
        df = pd.DataFrame({
            "البيان": ["العنصر", "الأبعاد", "العزم", "التسليح السفلي", "التسليح العلوي", "المهندس", "الهاتف"],
            "القيمة": ["جائز خرساني", f"{b}x{h} cm", f"{mu:.2f} kNm", f"{n} T 16", "2 T 12", NAME, TEL]
        })
        
        output_ex = io.BytesIO()
        with pd.ExcelWriter(output_ex, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Structural_Report')
        
        st.download_button("📥 تحميل المذكرة (Excel)", output_ex.getvalue(), "Pelan_Report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # 2. تصدير AutoCAD (مقطع + عزم + قص)
        if st.button("🚀 إنشاء مخطط أوتوكاد DXF"):
            doc = ezdxf.new(setup=True); msp = doc.modelspace()
            # رسم المقطع
            msp.add_lwpolyline([(0,0), (b*10,0), (b*10,h*10), (0,h*10), (0,0)], dxfattribs={'color': 7})
            msp.add_text(f"ENG. {NAME} - TEL: {TEL}", dxfattribs={'height': 20}).set_placement((0, h*10 + 50))
            
            output_cad = io.StringIO()
            doc.write(output_cad)
            st.download_button("📥 تحميل ملف AutoCAD", output_cad.getvalue(), "Pelan_Design.dxf")

        # الختم
        st.markdown(f"""<div class='stamp'><p><b>المهندس المدني</b></p><p style='color:#d4af37; font-size:20px;'><b>{NAME}</b></p>
        <p>{WORK}</p><p>TEL: {TEL}</p></div>""", unsafe_allow_html=True)

# الرسوم التوضيحية
