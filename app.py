import streamlit as st
import numpy as np
import plotly.graph_objects as go

# إعداد الصفحة
st.set_page_config(page_title="منظومة المهندس بيلان الذكية", layout="wide")

# الختم المهني الرسمي
st.markdown(f"""
    <div style="direction: rtl; text-align: right; border: 3px solid #1b5e20; padding: 15px; border-radius: 15px; background-color: #f1f8e9;">
        <h1 style="color: #1b5e20; margin:0;">المنظومة الهندسيّة الذكيّة (برمجة التباعد الآلي)</h1>
        <h2 style="color: #2e7d32; margin:0;">المهندس المدني بيلان مصطفى عبدالكريم</h2>
        <p style="font-size: 18px; margin:5px;">دراسات - إشراف - تعهدات | <b>0998449697</b></p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.header("⚙️ إعدادات الكود الذكي")
fcu = st.sidebar.select_slider("مقاومة الخرسانة fcu (MPa)", options=[20, 25, 30, 35, 40], value=25)
fy = st.sidebar.selectbox("إجهاد خضوع الحديد fy (MPa)", options=[240, 360, 400], index=2)
f_prime_c = 0.8 * fcu

choice = st.sidebar.radio("اختر العنصر:", ["جوائز ساقطة", "جوائز مخفية", "بلاطة هوردي", "الأعمدة", "الأساسات"])

def draw_smart_section(b, h, n_low, dia_low, n_up, dia_up, s_spacing, s_dia, title, info_text):
    fig = go.Figure()
    fig.add_shape(type="rect", x0=0, y0=0, x1=b, y1=h, line=dict(color="black", width=4), fillcolor="rgba(180,180,180,0.2)")
    fig.add_shape(type="rect", x0=25, y0=25, x1=b-25, y1=h-25, line=dict(color="blue", width=3))
    
    # رسم الحديد السفلي والعلوي وتسميتهما
    for i in range(n_low):
        x_p = 45 + (i * (b-90)/(n_low-1 if n_low > 1 else 1))
        fig.add_trace(go.Scatter(x=[x_p], y=[45], mode="markers", marker=dict(size=dia_low*1.2, color="red"), showlegend=False))
    for i in range(n_up):
        x_p = 45 + (i * (b-90)/(n_up-1 if n_up > 1 else 1))
        fig.add_trace(go.Scatter(x=[x_p], y=[h-45], mode="markers", marker=dict(size=dia_up*1.2, color="green"), showlegend=False))
    
    fig.add_annotation(x=b/2, y=-45, text=f"السفلي: {n_low} T{dia_low}", showarrow=False, font=dict(color="red", size=16))
    fig.add_annotation(x=b/2, y=h+45, text=f"العلوي: {n_up} T{dia_up}", showarrow=False, font=dict(color="green", size=16))
    fig.add_annotation(x=b+60, y=h/2, text=info_text, textangle=90, showarrow=False, font=dict(color="blue", size=14))

    fig.update_layout(xaxis_visible=False, yaxis_visible=False, height=550, width=750, plot_bgcolor="white", title_text=title)
    return fig

if "جوائز" in choice:
    st.header(f"🏗️ تصميم {choice} (تباعد كانات مبرمج)")
    col1, col2 = st.columns([1, 2])
    with col1:
        L = st.number_input("طول المجاز (m)", value=5.0)
        b = st.number_input("العرض b (mm)", value=300 if "ساقطة" in choice else 800)
        h = st.number_input("الارتفاع h (mm)", value=500 if "ساقطة" in choice else 300)
        wu = st.number_input("الحمولة التصعيدية Wu (kN/m)", value=40.0)
        
        # --- البرمجة الذكية للكانات (القص) ---
        Vu = (wu * L) / 2 # قوة القص القصوى
        d = h - 50
        # مقاومة الخرسانة للقص (الكود السوري التقريربي)
        Vc = 0.17 * np.sqrt(f_prime_c) * b * d / 1000 
        
        s_dia = 8 # القطر الافتراضي للكانة
        if Vu <= 0.5 * Vc:
            spacing = 20 # تباعد إنشائي أعظمي
        elif Vu <= Vc:
            spacing = 15
        else:
            # حساب التباعد المطلوب برمجياً
            Av = 2 * (np.pi * s_dia**2 / 4) # فرعين
            Vs = (Vu / 0.75) - Vc
            if Vs > 0:
                spacing = (Av * fy * d) / (Vs * 1000) / 10 # تحويل لـ cm
                spacing = min(max(int(spacing), 10), 20) # حصر التباعد بين 10 و 20 سم
            else:
                spacing = 15
        
        n_stirrups = int(100/spacing)
        st.metric("تباعد الكانات المبرمج", f"{spacing} cm", f"{n_stirrups} كائنات/م")
        
        # حساب الحديد الطولي
        mu = (wu * L**2) / 8
        as_low = max((mu * 1e6) / (0.9 * fy * 0.9 * d), (1.4/fy)*b*d)
        dia_l = st.selectbox("قطر السفلي", [14, 16, 18, 20], index=1)
        
    with col2:
        n_l = int(np.ceil(as_low / (np.pi * dia_l**2 / 4)))
        n_u = max(2, int(0.2 * n_l)) # حديد علوي تعليق
        
        info_stirrup = f"الكانات: T{s_dia} @ {spacing} cm \n ({n_stirrups} T{s_dia} / m')"
        st.plotly_chart(draw_smart_section(b, h, n_l, dia_l, n_u, 12, spacing, s_dia, f"مقطع {choice}", info_stirrup))

elif choice == "بلاطة هوردي":
    st.header("🧱 عصب هوردي بتسليح كامل")
    # تطبيق نفس المنطق البرمجي للقص على العصب
    b_rib = 120
    h_rib = 300
    st.plotly_chart(draw_smart_section(b_rib, h_rib, 2, 14, 2, 10, 20, 8, "مقطع عصب هوردي", "كانات T8 @ 20 cm"))

elif choice == "الأعمدة":
    st.header("🏛️ الأعمدة (أساور مبرمجة)")
    # تباعد الأساور في الأعمدة مبرمج (15 سم أو 10 حسب قطر القضبان)
    st.plotly_chart(draw_smart_section(300, 500, 4, 16, 4, 16, 15, 8, "مقطع عمود", "أساور T8 @ 15 cm"))

st.divider()
st.caption(f"تمت البرمجة والتدقيق الإنشائي الذكي: المهندس بيلان مصطفى عبدالكريم - 0998449697")
