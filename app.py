import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import ezdxf
import io

# بيانات الختم الثابتة
ST_NAME = "بيلان مصطفى عبد الكريم"
ST_JOB = "المهندس المدني (دراسة - إشراف - تعهدات)"
ST_TEL = "0998449697"

st.set_page_config(page_title="Pelan Pro v89", layout="wide")

# تصميم الواجهة الاحترافي
st.markdown(f"""
<style>
 .stApp {{ background-color: #0b1619; color: white; }}
 .report-card {{ background: white; color: black; padding: 20px; border-radius: 10px; direction: rtl; border-right: 10px solid #d4af37; }}
 .cad-dark {{ background: #151515; border: 2px solid #333; padding: 15px; border-radius: 8px; color: #50c878; text-align: center; }}
 .official-stamp {{ border: 3px double #d4af37; padding: 10px; width: 280px; text-align: center; background: #fff; color: #000; float: left; margin-top: 20px; }}
</style>
""", unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ مدخلات التصميم")
    element = st.selectbox("نوع العنصر:", ["جائز مستطيل", "أساس منفرد", "عمود"])
    B_cm = st.number_input("العرض B (cm):", 20, 100, 30)
    H_cm = st.number_input("الارتفاع H (cm):", 20, 200, 60)
    L_m = st.number_input("الطول L (m):", 1, 20, 5)
    Load = st.number_input("الحمل (kN/m):", 1, 500, 30)
    phi_m = st.selectbox("القطر الرئيسي:", [14, 16, 18, 20, 25], index=1)

# الحسابات الإنشائية
M_max = (Load * L_m**2) / 8
n_bars = max(3, int(np.ceil((M_max * 1e6) / (0.87 * 420 * (H_cm-5) * 10) / (np.pi * phi_m**2 / 4))))

# العرض الرئيسي
st.markdown(f"<h1 style='text-align:center; color:#d4af37;'>🏗️ مكتب المهندس بيلان - نظام التصميم v89</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.3])

with col1:
    st.markdown("<div class='report-card'>", unsafe_allow_html=True)
    st.subheader("📑 المذكرة الحسابية")
    st.write(f"**العنصر:** {element}")
    st.write(f"**العزم الأقصى:** {M_max:.1f} kNm")
    st.write(f"**الحديد المطلوب:** {n_bars} T {phi_m}")
    st.divider()
    # رسم مخطط العزم (BMD)
    fig, ax = plt.subplots(figsize=(4, 2))
    x = np.linspace(0, L_m, 50)
    m_plot = (Load*x/2)*(L_m-x)
    ax.fill_between(x, m_plot, color='orange', alpha=0.3)
    ax.set_title("Moment Diagram (BMD)", fontsize=8)
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='cad-dark'>", unsafe_allow_html=True)
    st.subheader("🖋️ مخطط الفرش وتفريد الحديد (CAD)")
    
    # استدعاء المخططات التوضيحية
    if "جائز" in element:
            elif "أساس" in element:
            else:
                
    st.write(f"تفريد الحديد: {n_bars} قضبان سفلية (الفرش) مع توصيف كامل.")
    st.markdown("</div>", unsafe_allow_html=True)

    # الختم الرسمي مع الرقم
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

# تصدير AutoCAD
st.divider()
if st.button("🚀 تصدير المخطط الإنشائي الكامل (DXF)"):
    doc = ezdxf.new(setup=True); msp = doc.modelspace()
    msp.add_lwpolyline([(0,0), (B_cm*10,0), (B_cm*10,H_cm*10), (0,H_cm*10), (0,0)])
    msp.add_text(f"ENG. PELAN - {n_bars}T{phi_m}", dxfattribs={'height': 15}).set_placement((0, -30))
    msp.add_text(f"TEL: {ST_TEL}", dxfattribs={'height': 12}).set_placement((0, -50))
    buf = io.StringIO(); doc.write(buf)
    st.download_button("📥 تحميل المخطط الآن", buf.getvalue(), "Pelan_Office_v89.dxf")
