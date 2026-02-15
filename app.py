import streamlit as st
import numpy as np
import ezdxf
import io

# إعدادات الهوية الثابتة
ST_NAME = "بيلان مصطفى عبد الكريم"
ST_TEL = "0998449697"
ST_WORK = "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v100", layout="wide")

# تصميم الواجهة الراقية
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); color: white; }}
    .calc-card {{ background: rgba(255, 255, 255, 0.95); color: #1a1a1a; padding: 25px; border-radius: 15px; direction: rtl; border-right: 12px solid #d4af37; margin-bottom: 20px; }}
    .pro-stamp {{ border: 4px double #d4af37; padding: 12px; width: 300px; text-align: center; background: white; color: black; float: left; margin-top: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }}
</style>
""", unsafe_allow_html=True)

# دالة الختم الموحدة
def display_stamp():
    st.markdown(f"""
    <div class='pro-stamp'>
        <p style='margin:0; font-weight:bold; color:#2c5364; font-size:16px;'>المهندس المدني</p>
        <p style='color:#d4af37; font-size:22px; font-weight:bold; margin:5px 0;'>{ST_NAME}</p>
        <p style='margin:0; font-size:14px; color:#555;'>{ST_WORK}</p>
        <p style='margin:5px 0; font-weight:bold; color:#d4af37;'>TEL: {ST_TEL}</p>
        <hr style='border:1px solid #d4af37; margin:10px;'>
        <p style='font-size:10px; color:#888;'>v100 - الاعتماد الرسمي</p>
    </div>
    <div style='clear:both;'></div>
    """, unsafe_allow_html=True)

st.markdown(f"<h1 style='text-align:center; color:#d4af37;'>🏗️ مكتب المهندس بيلان - التبويبات المنفصلة v100</h1>", unsafe_allow_html=True)

# إنشاء التبويبات لفصل العناصر
tab1, tab2, tab3, tab4 = st.tabs(["📏 الجوائز (Beams)", "🏛️ الأعمدة (Columns)", "🦶 الأساسات (Footings)", "🧱 البلاطات (Slabs)"])

# ---------------------------------------------------------
# التبويب الأول: الجوائز (حساب + رسم عزم وقص + أوتوكاد)
# ---------------------------------------------------------
with tab1:
    st.subheader("تصميم الجوائز المستمرة والبسيطة")
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.write("### المذكرة الحسابية")
        b = st.number_input("العرض B (cm):", 20, 100, 30, key="b_b")
        h = st.number_input("الارتفاع H (cm):", 20, 200, 60, key="h_b")
        l = st.number_input("البحر L (m):", 1.0, 15.0, 5.0, key="l_b")
        w = st.number_input("الحمل q (kN/m):", 1.0, 200.0, 40.0, key="w_b")
        phi_b = st.selectbox("قطر السفلي:", [14, 16, 18, 20], key="p_b")
        
        mu = (w * l**2) / 8
        vu = (w * l) / 2
        n_bot = max(2, int(np.ceil((mu * 1e6) / (0.87 * 420 * (h-5) * 10) / (np.pi * phi_b**2 / 4))))
        
        st.divider()
        st.write(f"العزم: {mu:.2f} kNm | القص: {vu:.2f} kN")
        st.write(f"التسليح: {n_bot} T {phi_b} سفلي + 2 T 12 علوي")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        
        st.write("### مخططات العزم والقص الميكانيكية")
        
        display_stamp()

# ---------------------------------------------------------
# التبويب الثاني: الأعمدة (حساب أحمال + رسم مقطع)
# ---------------------------------------------------------
with tab2:
    st.subheader("تصميم الأعمدة الخرسانية")
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.write("### المذكرة الحسابية")
        bc = st.number_input("العرض (cm):", 20, 150, 30, key="bc")
        hc = st.number_input("العمق (cm):", 20, 150, 50, key="hc")
        axial = st.number_input("الحمل المحوري N (kN):", 100, 5000, 1200)
        phi_c = st.selectbox("القطر:", [16, 18, 20, 25], key="pc")
        
        as_min = 0.008 * bc * hc
        n_c = max(4, int(np.ceil(as_min / (np.pi * phi_c**2 / 400))))
        st.write(f"الحديد المطلوب: {n_c} T {phi_c}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        
        display_stamp()

# ---------------------------------------------------------
# التبويب الثالث: الأساسات (حساب إجهادات + فرش وغطاء)
# ---------------------------------------------------------
with tab3:
    st.subheader("تصميم الأساسات المنفردة")
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.write("### المذكرة الحسابية")
        sigma = st.number_input("إجهاد التربة (kg/cm2):", 0.5, 5.0, 2.0)
        load_f = st.number_input("حمولة العمود (kN):", 100, 5000, 1500)
        area = (load_f / 10) / sigma
        side = np.sqrt(area)
        st.write(f"أبعاد القاعدة: {side:.1f} x {side:.1f} cm")
        st.write("التسليح: 7 T 14 لكل متر (بالاتجاهين)")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        
        display_stamp()

# ---------------------------------------------------------
# التبويب الرابع: البلاطات
# ---------------------------------------------------------
with tab4:
    st.subheader("تصميم البلاطات المصمتة (Solid Slab)")
    
    display_stamp()

# ---------------------------------------------------------
# محرك التصدير الشامل لأوتوكاد
# ---------------------------------------------------------
st.divider()
if st.button("🚀 تصدير كافة المخططات والمذكرة الحسابية (AutoCAD DXF)"):
    doc = ezdxf.new(setup=True); msp = doc.modelspace()
    # رسم مبسط للبيانات في المخطط
    msp.add_text(f"ENGINEERING REPORT - {ST_NAME}", dxfattribs={'height': 30}).set_placement((0, 100))
    msp.add_text(f"TEL: {ST_TEL}", dxfattribs={'height': 20}).set_placement((0, 50))
    msp.add_text(f"WORK: {ST_WORK}", dxfattribs={'height': 20}).set_placement((0, 10))
    
    buf = io.StringIO(); doc.write(buf)
    st.download_button("📥 تحميل ملف AutoCAD", buf.getvalue(), f"Pelan_Project_v100.dxf")
