import streamlit as st
import numpy as np
import plotly.graph_objects as go

# إعداد الصفحة الاحترافي
st.set_page_config(page_title="المنظومة الإنشائية المتكاملة - م. بيلان", layout="wide")

# الختم المهني الرسمي
st.markdown(f"""
    <div style="direction: rtl; text-align: right; border: 3px solid #1b5e20; padding: 15px; border-radius: 15px; background-color: #f1f8e9;">
        <h1 style="color: #1b5e20; margin:0;">المنظومة الهندسيّة الاحترافيّة للتصميم والرسم</h1>
        <h2 style="color: #2e7d32; margin:0;">المهندس المدني بيلان مصطفى عبدالكريم</h2>
        <p style="font-size: 18px; margin:5px;">دراسات - إشراف - تعهدات | <b>0998449697</b></p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.header("🛠️ مواصفات المواد والكود")
fcu = st.sidebar.select_slider("مقاومة الخرسانة fcu (MPa)", options=[20, 25, 30, 35, 40], value=25)
fy = st.sidebar.selectbox("إجهاد خضوع الحديد fy (MPa)", options=[240, 360, 400], index=2)
f_prime_c = 0.8 * fcu

choice = st.sidebar.radio("اختر العنصر للتصميم التفصيلي:", 
                         ["بلاطة هوردي (Ribbed Slab)", "الأعمدة (Columns)", "الأساسات (Footings)", "الجوائز والبلاطات المسمطة"])

# --- محرك الرسم الهندسي الموحد ---
def draw_section(b, h, n_low, dia_low, n_up, dia_up, stirrup_txt, title, is_column=False):
    fig = go.Figure()
    # رسم الخرسانة
    fig.add_shape(type="rect", x0=0, y0=0, x1=b, y1=h, line=dict(color="black", width=4), fillcolor="rgba(128,128,128,0.1)")
    # رسم الكانة
    fig.add_shape(type="rect", x0=20, y0=20, x1=b-20, y1=h-20, line=dict(color="blue", width=2))
    
    # توزيع ورسم التسليح السفلي
    for i in range(n_low):
        x_p = 40 + (i * (b-80)/(n_low-1 if n_low > 1 else 1))
        fig.add_trace(go.Scatter(x=[x_p], y=[40], mode="markers", marker=dict(size=dia_low, color="red"), showlegend=False))
    fig.add_annotation(x=b/2, y=-15, text=f"الأسفل: {n_low} T{dia_low}", showarrow=False, font=dict(color="red", size=14))
    
    # توزيع ورسم التسليح العلوي
    for i in range(n_up):
        x_p = 40 + (i * (b-80)/(n_up-1 if n_up > 1 else 1))
        fig.add_trace(go.Scatter(x=[x_p], y=[h-40], mode="markers", marker=dict(size=dia_up, color="green"), showlegend=False))
    fig.add_annotation(x=b/2, y=h+15, text=f"الأعلى: {n_up} T{dia_up}", showarrow=False, font=dict(color="green", size=14))
    
    # تسمية الكانة
    fig.add_annotation(x=-15, y=h/2, text=stirrup_txt, textangle=-90, showarrow=False, font=dict(color="blue"))
    
    fig.update_layout(xaxis_visible=False, yaxis_visible=False, height=450, width=550, plot_bgcolor="white", title_text=title)
    return fig

# --- 1. بلاطة هوردي ---
if choice == "بلاطة هوردي (Ribbed Slab)":
    st.header("🧱 تصميم بلاطة هوردي (عصب منفرد)")
    col1, col2 = st.columns([1, 2])
    with col1:
        L = st.number_input("طول المجاز (m)", value=5.0)
        h_total = st.number_input("الارتفاع الكلي (cm)", value=30)
        b_rib = st.number_input("عرض العصب b (mm)", value=120)
        st.caption("التصميم لعصب واحد بعرض تحميل 50 سم")
        wu = (1.4 * 5.0) + (1.7 * 2.0) # أحمال نموذجية للهوردي
        mu = (wu * 0.5 * L**2) / 8
        d = (h_total * 10) - 30
        # حساب الحديد
        as_low = max((mu * 1e6) / (0.9 * fy * 0.9 * d), (1.4/fy)*b_rib*d)
        dia = st.selectbox("قطر السفلي", [12, 14, 16])
        n_low = int(np.ceil(as_low / (np.pi * dia**2 / 4)))
    with col2:
        st.plotly_chart(draw_section(b_rib, h_total*10, n_low, dia, 2, 10, "كانات مفتوحة T8", "مقطع في عصب الهوردي"))

# --- 2. الأعمدة ---
elif choice == "الأعمدة (Columns)":
    st.header("🏛️ تصميم عمود بيطوني مسلح")
    col1, col2 = st.columns([1, 2])
    with col1:
        pu = st.number_input("الحمل Pu (kN)", value=2000)
        b = st.number_input("العرض B (mm)", value=300)
        h = st.number_input("العمق H (mm)", value=500)
        ag = b * h
        ast = 0.01 * ag # نسبة 1% حديد
        dia = st.selectbox("قطر القضبان", [14, 16, 18, 20])
        n_total = int(np.ceil(ast / (np.pi * dia**2 / 4)))
        if n_total % 2 != 0: n_total += 1
    with col2:
        st.plotly_chart(draw_section(b, h, n_total//2, dia, n_total//2, dia, "أساور T8/15cm", "مقطع عمود تفصيلي"))

# --- 3. الأساسات ---
elif choice == "الأساسات (Footings)":
    st.header("🕋 تصميم أساس منفرد")
    col1, col2 = st.columns([1, 2])
    with col1:
        ps = st.number_input("الحمل التشغيلي (kN)", value=1200)
        q = st.number_input("تحمل التربة (kN/m2)", value=150)
        area = (ps * 1.1) / q
        side = np.sqrt(area) * 1000 # mm
        h_f = st.number_input("سماكة الأساس (mm)", value=600)
        as_f = (1.4/fy) * side * (h_f-70)
        dia = st.selectbox("القطر", [12, 14, 16])
        n_bars = int(np.ceil(as_f / (np.pi * dia**2 / 4)))
    with col2:
        st.plotly_chart(draw_section(side, h_f, n_bars//2, dia, 0, 0, "فرش وغطاء", "مقطع في الأساس"))

# --- 4. الجوائز والبلاطات المسمطة ---
else:
    st.header("🏗️ تصميم الجوائز والبلاطات المسمطة")
    # (نفس كود الجوائز السابق مع الرسم المطور)
    st.info("استخدم نفس محرك الرسم المطور أعلاه للجوائز")

st.divider()
st.warning(f"تم الاعتماد الفني: المهندس المدني بيلان مصطفى عبدالكريم دراسات-اشراف-تعهدات 0998449697")
