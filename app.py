import streamlit as st

# بيانات الهوية الثابتة
ST_NAME = "بيلان مصطفى عبد الكريم"
ST_TEL = "0998449697"
ST_INFO = "المهندس المدني - دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v96", layout="wide")

# تصميم الواجهة
st.markdown(f"""
<style>
    .stApp {{ background-color: #0b1619; color: white; }}
    .report-card {{ background: white; color: black; padding: 20px; border-radius: 10px; direction: rtl; border-right: 10px solid #d4af37; margin-bottom: 20px; }}
    .cad-box {{ background: #111; border: 2px solid #444; padding: 15px; border-radius: 8px; color: #50c878; text-align: center; }}
    .stamp {{ border: 4px double #d4af37; padding: 10px; width: 280px; text-align: center; background: #fff; color: #000; float: left; margin-top: 20px; }}
</style>
""", unsafe_allow_html=True)

st.markdown(f"<h1 style='text-align:center; color:#d4af37;'>🏗️ مكتب المهندس بيلان - نظام العناصر المنفصلة</h1>", unsafe_allow_html=True)

# إنشاء التبويبات (Tabs) لفصل كل عنصر لحال
tab1, tab2, tab3, tab4 = st.tabs(["الجوائز (Beams)", "الأعمدة (Columns)", "الأساسات (Footings)", "البلاطات (Slabs)"])

# --- التبويب الأول: الجوائز ---
with tab1:
    st.subheader("🚀 تصميم وتفريد حديد الجوائز")
    c1, c2 = st.columns(2)
    with c1:
        b_b = st.number_input("العرض B (cm):", 20, 100, 30, key="b1")
        h_b = st.number_input("الارتفاع H (cm):", 20, 200, 60, key="h1")
        n_bot = st.number_input("عدد السفلي الرئيسي:", 2, 12, 4, key="n1")
        phi_b = st.selectbox("القطر:", [14, 16, 18, 20], key="p1")
    with c2:
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.write(f"**مذكرة الجائز:** {b_b}x{h_b}")
        st.write(f"**التسليح:** {n_bot} T {phi_b} سفلي + 2 T 12 تعليق")
        st.write(f"**الكانات:** Φ 8 @ 15cm")
        st.markdown("</div>", unsafe_allow_html=True)
    

# --- التبويب الثاني: الأعمدة ---
with tab2:
    st.subheader("🏛️ تصميم وتفريد حديد الأعمدة")
    c1, c2 = st.columns(2)
    with c1:
        b_c = st.number_input("العرض B (cm):", 20, 200, 30, key="b2")
        h_c = st.number_input("العمق H (cm):", 20, 200, 50, key="h2")
        n_c = st.number_input("إجمالي عدد القضبان:", 4, 24, 8, key="n2")
    with c2:
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.write(f"**مذكرة العمود:** {b_c}x{h_c}")
        st.write(f"**التسليح الطولي:** {n_c} T 16")
        st.write(f"**الأساور:** Φ 8 كل 15 سم")
        st.markdown("</div>", unsafe_allow_html=True)
    

# --- التبويب الثالث: الأساسات ---
with tab3:
    st.subheader("🦶 تصميم وتفريد حديد الأساسات")
    c1, c2 = st.columns(2)
    with c1:
        bf = st.number_input("عرض القاعدة B (cm):", 100, 500, 150, key="b3")
        hf = st.number_input("سماكة القاعدة H (cm):", 30, 150, 50, key="h3")
    with c2:
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.write(f"**مذكرة الأساس:** {bf}x{bf} cm")
        st.write(f"**الفرش والغطاء:** 7 T 14 / m'")
        st.markdown("</div>", unsafe_allow_html=True)
    

# --- التبويب الرابع: البلاطات ---
with tab4:
    st.subheader("📏 تصميم وتفريد حديد البلاطات")
    st.write("تفاصيل تسليح البلاطة المصمتة (Solid Slab)")
    

# الختم الرسمي الثابت في أسفل البرنامج
st.divider()
st.markdown(f"""
<div class='stamp'>
    <p style='margin:0; font-weight:bold;'>المهندس المدني</p>
    <p style='color:#d4af37; font-size:19px; font-weight:bold; margin:5px 0;'>{ST_NAME}</p>
    <p style='margin:0; font-size:13px;'>{ST_INFO}</p>
    <p style='margin:5px 0; font-weight:bold;'>TEL: {ST_TEL}</p>
    <hr style='border:1px solid #d4af37; margin:8px;'>
    <p style='font-size:10px;'>ختم الاعتماد الرسمي v96</p>
</div>
<div style='clear:both;'></div>
""", unsafe_allow_html=True)
