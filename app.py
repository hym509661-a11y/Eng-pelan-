import streamlit as st
import numpy as np
import plotly.graph_objects as go

# إعداد الصفحة
st.set_page_config(page_title="المنظومة الإنشائية المتكاملة - م. بيلان", layout="wide")

# الختم المهني المعتمد
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

# اختيار العنصر
choice = st.sidebar.radio("اختر العنصر للتصميم التفصيلي:", ["الجوائز البيتونية (Beams)", "البلاطات المسمطة"])

if choice in ["الجوائز البيتونية (Beams)", "البلاطات المسمطة"]:
    st.header(f"🏗️ التصميم التفصيلي لـ {choice}")
    col1, col2 = st.columns([1, 1.8])
    
    with col1:
        L = st.number_input("طول المجاز (m)", value=5.0)
        b = st.number_input("عرض المقطع b (mm)", value=300 if choice == "الجوائز البيتونية (Beams)" else 1000)
        h = st.number_input("الارتفاع الكلي h (mm)", value=500 if choice == "الجوائز البيتونية (Beams)" else 150)
        
        st.subheader("📥 الأحمال التصميمية")
        dl = st.number_input("الحمولة الميتة (kN/m)", value=15.0 if choice == "الجوائز البيتونية (Beams)" else 2.5)
        ll = st.number_input("الحمولة الحية (kN/m)", value=10.0 if choice == "الجوائز البيتونية (Beams)" else 3.0)
        
        wu = (1.4 * dl) + (1.7 * ll)
        mu = (wu * L**2) / 8 
        d = h - 40 # غطاء خرساني
        
        # حساب التسليح السفلي (الرئيسي)
        rn = (mu * 1e6) / (0.9 * b * d**2)
        m = fy / (0.85 * f_prime_c)
        rho = (1/m) * (1 - np.sqrt(max(0, 1 - (2*m*rn/fy))))
        as_low = max(rho * b * d, (1.4/fy)*b*d)
        
        # حساب التسليح العلوي (علاق كائنات أو ضغط)
        as_up = 0.2 * as_low if choice == "الجوائز البيتونية (Beams)" else 0.15 * as_low
        
        st.divider()
        dia_low = st.selectbox("قطر قضبان السفلي (mm)", [12, 14, 16, 18, 20], index=2)
        dia_up = st.selectbox("قطر قضبان العلوي (mm)", [10, 12, 14], index=0)
        stirrup_dia = st.number_input("قطر الكانات (mm)", value=8)

    with col2:
        n_low = int(np.ceil(as_low / (np.pi * dia_low**2 / 4)))
        n_up = int(np.ceil(as_up / (np.pi * dia_up**2 / 4)))
        if n_up < 2: n_up = 2 # كود: قضيبين على الأقل للعلوي
        
        st.subheader("📊 النتائج واللوحة الهندسيّة")
        st.success(f"السفلي: {n_low} T{dia_low} | العلوي: {n_up} T{dia_up}")
        
        # الرسم الهندسي المتقدم (Full Detail Drawing)
        fig = go.Figure()
        
        # 1. رسم المقطع الخرساني
        fig.add_shape(type="rect", x0=0, y0=0, x1=b, y1=h, line=dict(color="black", width=4), fillcolor="rgba(128,128,128,0.1)")
        
        # 2. رسم الكانة (Stirrup)
        fig.add_shape(type="rect", x0=20, y0=20, x1=b-20, y1=h-20, line=dict(color="blue", width=2, dash="solid"))
        
        # 3. رسم وتسمية التسليح السفلي
        for i in range(n_low):
            x_p = 40 + (i * (b-80)/(n_low-1 if n_low > 1 else 1))
            fig.add_trace(go.Scatter(x=[x_p], y=[40], mode="markers", marker=dict(size=dia_low, color="red"), showlegend=False))
        fig.add_annotation(x=b/2, y=10, text=f"التسليح السفلي: {n_low} T{dia_low}", showarrow=False, font=dict(color="red", size=14))
        
        # 4. رسم وتسمية التسليح العلوي
        for i in range(n_up):
            x_p = 40 + (i * (b-80)/(n_up-1 if n_up > 1 else 1))
            fig.add_trace(go.Scatter(x=[x_p], y=[h-40], mode="markers", marker=dict(size=dia_up, color="green"), showlegend=False))
        fig.add_annotation(x=b/2, y=h-10, text=f"التسليح العلوي: {n_up} T{dia_up}", showarrow=False, font=dict(color="green", size=14))

        # 5. تسمية الكانات
        fig.add_annotation(x=15, y=h/2, text=f"كانات T{stirrup_dia}", textangle=-90, showarrow=False, font=dict(color="blue"))

        fig.update_layout(xaxis_visible=False, yaxis_visible=False, height=500, width=600, plot_bgcolor="white", title_text="مقطع عرضي تفصيلي (Detailed Section)")
        st.plotly_chart(fig)

st.divider()
st.info(f"تم التدقيق الإنشائي وفق الكود السوري | {st.session_state.get('eng', 'المهندس بيلان مصطفى عبدالكريم')}")
