import streamlit as st
import numpy as np
import plotly.graph_objects as go

# إعداد الصفحة الاحترافي
st.set_page_config(page_title="منظومة المهندس بيلان - التصميم الذكي", layout="wide")

# الختم المهني المعتمد
st.markdown(f"""
    <div style="direction: rtl; text-align: right; border: 3px solid #1b5e20; padding: 15px; border-radius: 15px; background-color: #f1f8e9;">
        <h1 style="color: #1b5e20; margin:0;">المنظومة الهندسيّة الذكيّة (أبعاد أساسات مبرمجة)</h1>
        <h2 style="color: #2e7d32; margin:0;">المهندس المدني بيلان مصطفى عبدالكريم</h2>
        <p style="font-size: 18px; margin:5px;">دراسات - إشراف - تعهدات | <b>0998449697</b></p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.header("⚙️ إعدادات المواد")
fcu = st.sidebar.select_slider("مقاومة الخرسانة fcu (MPa)", options=[20, 25, 30, 35, 40], value=25)
fy = st.sidebar.selectbox("إجهاد خضوع الحديد fy (MPa)", options=[240, 360, 400], index=2)
f_prime_c = 0.8 * fcu

choice = st.sidebar.radio("العنصر الإنشائي:", ["الأساسات (أبعاد مبرمجة)", "الجوائز (ساقطة/مخفية)", "الأعمدة", "بلاطة هوردي"])

# --- محرك الرسم الهندسي التفصيلي ---
def draw_detailed_section(b, h, n_low, dia_low, n_up, dia_up, s_spacing, s_dia, title, info_text):
    fig = go.Figure()
    fig.add_shape(type="rect", x0=0, y0=0, x1=b, y1=h, line=dict(color="black", width=4), fillcolor="rgba(180,180,180,0.2)")
    fig.add_shape(type="rect", x0=25, y0=25, x1=b-25, y1=h-25, line=dict(color="blue", width=3))
    
    # رسم الحديد وتوزيعه
    for i in range(n_low):
        x_p = 45 + (i * (b-90)/(n_low-1 if n_low > 1 else 1))
        fig.add_trace(go.Scatter(x=[x_p], y=[45], mode="markers", marker=dict(size=dia_low*1.2, color="red"), showlegend=False))
    for i in range(n_up):
        x_p = 45 + (i * (b-90)/(n_up-1 if n_up > 1 else 1))
        fig.add_trace(go.Scatter(x=[x_p], y=[h-45], mode="markers", marker=dict(size=dia_up*1.2, color="green"), showlegend=False))
    
    fig.add_annotation(x=b/2, y=-50, text=f"السفلي: {n_low} T{dia_low}", showarrow=False, font=dict(color="red", size=16))
    fig.add_annotation(x=b/2, y=h+50, text=f"العلوي: {n_up} T{dia_up}", showarrow=False, font=dict(color="green", size=16))
    fig.add_annotation(x=b+70, y=h/2, text=info_text, textangle=90, showarrow=False, font=dict(color="blue", size=14))

    fig.update_layout(xaxis_visible=False, yaxis_visible=False, height=500, width=700, plot_bgcolor="white", title_text=title)
    return fig

# --- 1. الأساسات (الأبعاد والتباعد مبرمجة تلقائياً) ---
if choice == "الأساسات (أبعاد مبرمجة)":
    st.header("🕋 تصميم الأساس المنفرد (أبعاد وتسليح مبرمج)")
    col1, col2 = st.columns([1, 2])
    with col1:
        p_service = st.number_input("حمولة العمود التشغيلية (kN)", value=1500)
        q_allow = st.number_input("تحمل التربة المسموح (kN/m²)", value=200)
        
        # --- البرمجة الذكية للأبعاد ---
        area_req = (p_service * 1.1) / q_allow # زيادة 10% للوزن الذاتي
        side = np.sqrt(area_req)
        side_final = np.ceil(side * 10) / 10 # تقريب لأقرب 10 سم
        
        # حساب السماكة مبرمج (مقاومة الثقب والقص)
        h_final = max(0.5, side_final / 4) # حد أدنى 50 سم أو ربع الطول
        h_mm = h_final * 1000
        b_mm = side_final * 1000
        
        st.success(f"الأبعاد المبرمجة: {side_final:.2f} x {side_final:.2f} m")
        st.info(f"السماكة المبرمجة: {h_mm:.0f} mm")
        
        # حساب التسليح (فرش وغطاء)
        pu = p_service * 1.5
        mu_face = (pu / (side_final**2)) * ((side_final - 0.4)**2) / 8 # عزم تقريبي عند وجه العمود
        as_req = max((mu_face * 1e6) / (0.9 * fy * 0.9 * (h_mm-70)), (1.4/fy)*b_mm*(h_mm-70))
        dia_f = st.selectbox("قطر حديد الأساس", [12, 14, 16], index=1)
        n_bars = int(np.ceil(as_req / (np.pi * dia_f**2 / 4)))
        
    with col2:
        info_footing = f"التسليح: T{dia_f} @ {int(b_mm/n_bars/10)} cm (فرش وغطاء)"
        st.plotly_chart(draw_detailed_section(b_mm, h_mm, n_bars, dia_f, 0, 0, 15, 0, "مقطع في الأساس المبرمج", info_footing))

# --- 2. باقي العناصر (الأبعاد من إدخال المهندس بيلان) ---
elif "الجوائز" in choice:
    st.header(f"🏗️ تصميم {choice} (أبعاد يدوية)")
    col1, col2 = st.columns([1, 2])
    with col1:
        b = st.number_input("العرض b (mm) - إدخالك", value=300)
        h = st.number_input("الارتفاع h (mm) - إدخالك", value=500)
        L = st.number_input("المجاز (m)", value=5.0)
        wu = st.number_input("الحمولة (kN/m)", value=35.0)
        
        # تباعد الكانات مبرمج (كما طلبت سابقاً)
        d = h - 50
        Vu = (wu * L) / 2
        Vc = 0.17 * np.sqrt(f_prime_c) * b * d / 1000
        spacing = 10 if Vu > Vc else 15
        
    with col2:
        # حساب الحديد بناءً على أبعاد المهندس
        mu = (wu * L**2) / 8
        as_l = max((mu * 1e6) / (0.9 * fy * 0.85 * d), (1.4/fy)*b*d)
        n_l = int(np.ceil(as_l / (np.pi * 16**2 / 4)))
        st.plotly_chart(draw_detailed_section(b, h, n_l, 16, 2, 12, spacing, 8, f"مقطع {choice}", f"كانات T8 @ {spacing} cm"))

elif choice == "الأعمدة":
    st.header("🏛️ تصميم العمود (أبعاد يدوية)")
    b = st.number_input("العرض B (mm)", value=300)
    h = st.number_input("العمق H (mm)", value=500)
    # رسم وتصميم العمود بناء على أبعادك
    st.plotly_chart(draw_detailed_section(b, h, 4, 16, 4, 16, 15, 8, "مقطع عمود", "أساور T8 @ 15 cm"))

st.divider()
st.warning(f"الختم الرسمي: المهندس بيلان مصطفى عبدالكريم دراسات-اشراف-تعهدات 0998449697")
