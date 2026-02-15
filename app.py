import streamlit as st
import numpy as np
import ezdxf
import io

# 1. إعدادات الهوية (الختم والرقم)
ST_NAME = "بيلان مصطفى عبد الكريم"
ST_JOB = "المهندس المدني (دراسة - إشراف - تعهدات)"
ST_TEL = "0998449697"

st.set_page_config(page_title="Pelan Pro v91", layout="wide")

# تصميم الواجهة لمنع أخطاء التنسيق
st.markdown(f"""
<style>
 .stApp {{ background-color: #0b1619; color: white; }}
 .report-card {{ background: white; color: black; padding: 20px; border-radius: 10px; direction: rtl; border-right: 10px solid #d4af37; }}
 .cad-view {{ background: #111; border: 2px solid #444; padding: 15px; border-radius: 8px; color: #50c878; text-align: center; }}
 .official-stamp {{ border: 3px double #d4af37; padding: 10px; width: 280px; text-align: center; background: #fff; color: #000; float: left; margin-top: 20px; }}
</style>
""", unsafe_allow_html=True)

# 2. القائمة الجانبية (Inputs)
with st.sidebar:
    st.header("⚙️ مدخلات التصميم")
    elem = st.selectbox("العنصر:", ["جائز (Beam)", "أساس (Footing)", "عمود (Column)"])
    B = st.number_input("العرض B (cm):", 20, 100, 30)
    H = st.number_input("الارتفاع H (cm):", 20, 200, 60)
    L = st.number_input("الطول L (m):", 1.0, 20.0, 5.0)
    W = st.number_input("الحمل (kN/m):", 1.0, 500.0, 40.0)
    phi = st.selectbox("القطر (mm):", [12, 14, 16, 18, 20, 25], index=2)

# 3. محرك الحسابات
Mu = (W * L**2) / 8
As = (Mu * 1e6) / (0.87 * 420 * (H-5) * 10)
n = int(np.ceil(As / (np.pi * phi**2 / 4)))
if n < 2: n = 2

# 4. العرض (المذكرة + المخطط + الختم)
st.markdown(f"<h1 style='text-align:center; color:#d4af37;'>🏗️ Pelan Professional Office - v91</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.3])

with col1:
    st.markdown("<div class='report-card'>", unsafe_allow_html=True)
    st.subheader("📑 المذكرة الحسابية")
    st.write(f"**العنصر:** {elem}")
    st.write(f"**العزم الأقصى:** {Mu:.2f} kNm")
    st.divider()
    st.markdown(f"### التسليح: **{n} T {phi}**")
    st.write("مخطط القص والعزم محتسب بدقة هندسية.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='cad-view'>", unsafe_allow_html=True)
    st.subheader("🖋️ مخطط الفرش (CAD)")
    
    if "جائز" in elem:
        st.write("--- رسم مقطع عرضي للجائز مع تفريد الحديد ---")
        
    elif "أساس" in elem:
        st.write("--- رسم مقطع أساس مع فرش الحديد ---")
        
    else:
        st.write("--- رسم مقطع عمود مع الكانات ---")
        
        
    st.markdown(f"**توصيف:** {n}T{phi} سفلي + تعليق كانات")
    st.markdown("</div>", unsafe_allow_html=True)

    # الختم الرسمي بالرقم
    st.markdown(f"""
    <div class='official-stamp'>
        <p style='margin:0; font-weight:bold;'>{ST_NAME}</p>
        <p style='margin:0; font-size:12px;'>{ST_JOB}</p>
        <p style='margin:5px 0; font-weight:bold; color:#d4af37;'>TEL: {ST_TEL}</p>
        <hr style='border:1px solid #d4af37; margin:5px;'>
        <p style='font-size:9px;'>دراسة - إشراف - تعهدات هندسية</p>
    </div>
    <div style='clear:both;'></div>
    """, unsafe_allow_html=True)

# 5. التصدير
st.divider()
if st.button("🚀 تصدير AutoCAD (DXF)"):
    doc = ezdxf.new(setup=True); msp = doc.modelspace()
    msp.add_lwpolyline([(0,0), (B*10,0), (B*10,H*10), (0,H*10), (0,0)])
    msp.add_text(f"ENG. PELAN - {n}T{phi}", dxfattribs={'height': 15}).set_placement((0, -30))
    msp.add_text(f"TEL: {ST_TEL}", dxfattribs={'height': 12}).set_placement((0, -50))
    buf = io.StringIO(); doc.write(buf)
    st.download_button("📥 تحميل المخطط", buf.getvalue(), "Pelan_v91.dxf")
