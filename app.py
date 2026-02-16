import streamlit as st
import pandas as pd
import numpy as np
import ezdxf
import io

# البيانات الشخصية الثابتة
NAME, TEL = "بيلان مصطفى عبد الكريم", "0998449697"
WORK_INFO = "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v103", layout="wide")

# تصميم الواجهة الراقية
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; }}
    .calc-box {{ background: white; color: black; padding: 25px; border-radius: 12px; direction: rtl; border-right: 12px solid #d4af37; }}
    .pro-stamp {{ border: 4px double #d4af37; padding: 12px; width: 300px; text-align: center; background: white; color: black; float: left; margin-top: 20px; }}
</style>
""", unsafe_allow_html=True)

st.title("🏗️ المكتب الهندسي - المهندس بيلان v103")

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ خيارات التصميم")
    # استخدام أرقام بدلاً من نصوص عربية داخل الكود لتجنب أخطاء المتصفح
    elem_choice = st.radio("اختر العنصر:", ["جائز (Beam)", "عمود (Column)", "أساس (Footing)"])
    B = st.number_input("العرض B (cm):", 20, 100, 30)
    H = st.number_input("الارتفاع H (cm):", 20, 200, 60)
    L = st.number_input("البحر L (m):", 1.0, 15.0, 5.0)
    W = st.number_input("الحمل q (kN/m):", 1.0, 200.0, 45.0)

# الحسابات الإنشائية
mu = (W * L**2) / 8
vu = (W * L) / 2
as_req = (mu * 1e6) / (0.87 * 420 * (H-5) * 10)
n_bars = max(2, int(np.ceil(as_req / (np.pi * 16**2 / 4)))) # قطر 16 افتراضي

# العرض والنتائج
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("<div class='calc-box'>", unsafe_allow_html=True)
    st.subheader("📑 المذكرة الحسابية")
    st.write(f"**العنصر:** {elem_choice}")
    st.write(f"**العزم الأقصى:** {mu:.2f} kNm")
    st.write(f"**قوة القص:** {vu:.2f} kN")
    st.divider()
    st.write(f"✅ **التسليح السفلي:** {n_bars} T 16")
    st.write(f"✅ **التسليح العلوي:** 2 T 12")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.subheader("📊 تصدير الجداول والمخططات")
    
    # 1. تصدير Excel (جداول الحصر)
    # ملاحظة: إذا ظهر خطأ في الإكسل، تأكد من تحديث ملف requirements.txt
    try:
        df = pd.DataFrame({
            "المعلمة": ["نوع العنصر", "العرض (cm)", "الارتفاع (cm)", "الطول (m)", "العزم (kNm)", "التسليح"],
            "القيمة": [elem_choice, B, H, L, round(mu,2), f"{n_bars} T 16"]
        })
        output_ex = io.BytesIO()
        with pd.ExcelWriter(output_ex, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        st.download_button("📥 تحميل المذكرة (Excel)", output_ex.getvalue(), "Structural_Report.xlsx")
    except Exception as e:
        st.warning("لتفعيل الإكسل، أضف xlsxwriter إلى ملف requirements.txt")

    # 2. تصدير AutoCAD DXF
    if st.button("🚀 إنشاء مخطط أوتوكاد"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        # رسم المقطع
        msp.add_lwpolyline([(0,0), (B*10,0), (B*10,H*10), (0,H*10), (0,0)], dxfattribs={'color': 7})
        msp.add_text(f"ENG. {NAME}", dxfattribs={'height': 20}).set_placement((0, H*10 + 50))
        # تصدير الملف
        out_cad = io.StringIO()
        doc.write(out_cad)
        st.download_button("📥 تحميل الرسم (DXF)", out_cad.getvalue(), "Beam_Detail.dxf")

    # الختم الرسمي
    st.markdown(f"""
    <div class='pro-stamp'>
        <p style='margin:0; font-weight:bold; color:#1a1a2e;'>المهندس المدني</p>
        <p style='color:#d4af37; font-size:20px; font-weight:bold; margin:5px 0;'>{NAME}</p>
        <p style='margin:0; font-size:13px;'>{WORK_INFO}</p>
        <p style='margin:5px 0; font-weight:bold; color:#d4af37;'>TEL: {TEL}</p>
    </div>
    """, unsafe_allow_html=True)

# الرسوم التوضيحية
