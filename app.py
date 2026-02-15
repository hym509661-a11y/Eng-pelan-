import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import ezdxf
import io

# بيانات الختم الثابتة
ST_NAME = "بيلان مصطفى عبد الكريم"
ST_JOB = "المهندس المدني (دراسة - إشراف - تعهدات)"
ST_TEL = "0998449697"

st.set_page_config(page_title="Pelan Pro v90", layout="wide")

# تصميم الواجهة الاحترافي لمنع تداخل النصوص العربية
st.markdown(f"""
<style>
 .stApp {{ background-color: #0b1619; color: white; }}
 .report-card {{ background: white; color: black; padding: 25px; border-radius: 10px; direction: rtl; border-right: 12px solid #d4af37; }}
 .cad-window {{ background: #111; border: 2px solid #444; padding: 20px; border-radius: 10px; color: #50c878; text-align: center; }}
 .official-stamp {{ border: 4px double #d4af37; padding: 15px; width: 320px; text-align: center; background: #fff; color: #000; float: left; margin-top: 30px; box-shadow: 5px 5px 15px rgba(0,0,0,0.2); }}
</style>
""", unsafe_allow_html=True)

# القائمة الجانبية (Inputs)
with st.sidebar:
    st.header("⚙️ إعدادات التصميم")
    element = st.selectbox("العنصر الإنشائي:", ["جائز (Beam)", "أساس (Footing)", "عمود (Column)"])
    B_cm = st.number_input("العرض B (cm):", 20, 100, 30)
    H_cm = st.number_input("الارتفاع H (cm):", 20, 200, 60)
    L_m = st.number_input("الطول L (m):", 1.0, 20.0, 5.0)
    Load = st.number_input("الحمل (kN/m):", 1.0, 500.0, 40.0)
    phi_m = st.selectbox("القطر الرئيسي (mm):", [12, 14, 16, 18, 20, 25], index=2)

# محرك الحسابات (Calculation Engine)
M_max = (Load * L_m**2) / 8
V_max = (Load * L_m) / 2
# حساب عدد القضبان بناءً على المساحة المطلوبة
As_req = (M_max * 1e6) / (0.87 * 420 * (H_cm - 5) * 10)
n_bars = int(np.ceil(As_req / (np.pi * phi_m**2 / 4)))
if n_bars < 2: n_bars = 2

# العرض الرئيسي للمذكرة
st.markdown(f"<h1 style='text-align:center; color:#d4af37;'>🏗️ Pelan Professional Office - v90</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.3])

with col1:
    st.markdown("<div class='report-card'>", unsafe_allow_html=True)
    st.subheader("📑 المذكرة الحسابية الهندسية")
    st.write(f"**العنصر:** {element} | **الأبعاد:** {B_cm}x{H_cm} cm")
    st.write(f"**العزم التصميمي (Mu):** {M_max:.2f} kNm")
    st.divider()
    st.markdown(f"### التسليح النهائي: **{n_bars} T {phi_m}**")
    
    # رسم مخطط القوى
    fig, ax = plt.subplots(figsize=(5, 3))
    x_plot = np.linspace(0, L_m, 100)
    m_curve = (Load * x_plot / 2) * (L_m - x_plot)
    ax.fill_between(x_plot, m_curve, color='orange', alpha=0.3)
    ax.set_title("Bending Moment Diagram (BMD)")
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='cad-window'>", unsafe_allow_html=True)
    st.subheader("🖋️ مخطط الفرش وتفريد الحديد (CAD Detail)")
    
    # عرض المخطط التفصيلي الدقيق بناءً على العنصر
    if "جائز" in element:
            elif "أساس" in element:
            else:
                
    st.markdown(f"**توصيف الحديد:** {n_bars} قضبان سفلية بقطر {phi_m} ملم مع سهم التوصيف.")
    st.markdown("</div>", unsafe_allow_html=True)

    # الختم الرسمي المتكامل مع الرقم (تم حل مشكلة التموضع)
    st.markdown(f"""
    <div class='official-stamp'>
        <p style='margin:0; font-size:14px;'><b>{ST_JOB}</b></p>
        <p style='color:#d4af37; font-size:20px; font-weight:bold; margin:5px 0;'>{ST_NAME}</p>
        <p style='margin:0; font-weight:bold; color:#1a1a1a;'>Tel: {ST_TEL}</p>
        <hr style='border:1px solid #d4af37; margin:10px;'>
        <p style='font-size:11px;'>دراسة - إشراف - تعهدات هندسية</p>
    </div>
    <div style='clear:both;'></div>
    """, unsafe_allow_html=True)

# محرك تصدير أوتوكاد المطور (رسم حقيقي وليس نصوص فقط)
st.divider()
if st.button("🚀 تصدير المخطط الإنشائي الكامل (DXF AutoCAD)"):
    doc = ezdxf.new(setup=True); msp = doc.modelspace()
    # رسم إطار الخرسانة
    msp.add_lwpolyline([(0,0), (B_cm*10,0), (B_cm*10,H_cm*10), (0,H_cm*10), (0,0)])
    # إضافة بيانات الحديد والتوصيف داخل ملف الرسم
    msp.add_text(f"REINFORCEMENT: {n_bars} T {phi_m}", dxfattribs={'height': 15}).set_placement((0, -30))
    msp.add_text(f"ENG. PELAN - {ST_TEL}", dxfattribs={'height': 15}).set_placement((0, -60))
    
    buf = io.StringIO(); doc.write(buf)
    st.download_button("📥 تحميل ملف AutoCAD المعتمد", buf.getvalue(), "Pelan_Office_v90.dxf")

st.info("ملاحظة هندسية: تم توزيع الحديد في الطبقة السفلية مع غطاء خرساني 5 سم.")
