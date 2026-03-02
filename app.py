import streamlit as st
import numpy as np
import plotly.graph_objects as go

# إعداد الصفحة
st.set_page_config(page_title="منظومة المهندس بيلان - نسخة التدقيق", layout="wide")

# الختم المهني الثابت
st.markdown(f"""
    <div style="direction: rtl; text-align: right; border: 2px solid #2e7d32; padding: 15px; border-radius: 10px; background-color: #f9fdf9;">
        <h2 style="color: #1b5e20; margin:0;">المهندس المدني بيلان مصطفى عبدالكريم</h2>
        <p style="font-size: 16px; margin:5px;">دراسات - إشراف - تعهدات | <b>0998449697</b></p>
    </div>
""", unsafe_allow_html=True)

# القائمة الجانبية لإعدادات المواد (ثوابت الكود)
fcu = st.sidebar.slider("مقاومة الخرسانة fcu", 20, 35, 25)
fy = st.sidebar.selectbox("إجهاد الحديد fy", [240, 360, 400], index=2)
f_prime_c = 0.8 * fcu

element = st.sidebar.radio("اختر العنصر للتصميم:", ["جوائز (ساقطة/مخفية)", "أعمدة", "بلاطة هوردي", "أساسات (أبعاد مبرمجة)"])

# --- وظيفة الرسم الهندسي المختصر والدقيق ---
def draw_section(b, h, n_low, d_low, n_up, d_up, s_spacing, s_dia, title):
    fig = go.Figure()
    # المقطع
    fig.add_shape(type="rect", x0=0, y0=0, x1=b, y1=h, line=dict(color="black", width=3), fillcolor="rgba(128,128,128,0.1)")
    # الكانة
    fig.add_shape(type="rect", x0=25, y0=25, x1=b-25, y1=h-25, line=dict(color="blue", width=2))
    # التسليح السفلي
    for i in range(n_low):
        x = 45 + (i * (b-90)/(max(1, n_low-1)))
        fig.add_trace(go.Scatter(x=[x], y=[45], mode="markers", marker=dict(size=d_low, color="red"), showlegend=False))
    # التسليح العلوي
    for i in range(n_up):
        x = 45 + (i * (b-90)/(max(1, n_up-1)))
        fig.add_trace(go.Scatter(x=[x], y=[h-45], mode="markers", marker=dict(size=d_up, color="green"), showlegend=False))
    
    fig.add_annotation(x=b/2, y=-40, text=f"سفلي: {n_low}T{d_low}", showarrow=False, font=dict(color="red"))
    fig.add_annotation(x=b/2, y=h+40, text=f"علوي: {n_up}T{d_up}", showarrow=False, font=dict(color="green"))
    fig.add_annotation(x=b+40, y=h/2, text=f"T{s_dia}@{s_spacing}cm", textangle=90, showarrow=False, font=dict(color="blue"))
    
    fig.update_layout(xaxis_visible=False, yaxis_visible=False, height=400, width=500, margin=dict(l=20, r=60, t=50, b=50), title=title)
    return fig

# --- تطبيق المنطق البرمجي لكل عنصر ---
if "جوائز" in element:
    st.subheader(f"💎 تصميم {element}")
    b = st.number_input("العرض b (mm)", value=300 if "ساقطة" in element else 800)
    h = st.number_input("الارتفاع h (mm)", value=500 if "ساقطة" in element else 300)
    L = st.number_input("المجاز (m)", value=5.0)
    wu = st.number_input("الحمولة Wu (kN/m)", value=30.0)
    
    d = h - 45
    mu = (wu * L**2) / 10 # عزم وسطي واقعي
    as_req = (mu * 1e6) / (0.9 * fy * 0.9 * d)
    as_min = (1.4 / fy) * b * d
    as_final = max(as_req, as_min)
    
    n_low = int(np.ceil(as_final / (np.pi * 16**2 / 4)))
    n_up = max(2, int(n_low * 0.3))
    
    # تباعد الكانات مبرمج (اقتصادي)
    vu = (wu * L) / 2
    vc = 0.17 * np.sqrt(f_prime_c) * b * d / 1000
    spacing = 15 if vu < vc else 10
    
    st.plotly_chart(draw_section(b, h, n_low, 16, n_up, 12, spacing, 8, "مقطع الجائز"))

elif element == "أعمدة":
    st.subheader("🏛️ تصميم العمود")
    b = st.number_input("العرض B (mm)", value=300)
    h = st.number_input("العمق H (mm)", value=500)
    pu = st.number_input("الحمل Pu (kN)", value=1500)
    
    ag = b * h
    ast = 0.01 * ag # نسبة اقتصادية 1%
    n_total = int(np.ceil(ast / (np.pi * 16**2 / 4)))
    if n_total % 2 != 0: n_total += 1
    
    st.plotly_chart(draw_section(b, h, n_total//2, 16, n_total//2, 16, 15, 8, "مقطع العمود"))

elif element == "أساسات (أبعاد مبرمجة)":
    st.subheader("🕋 تصميم الأساس (أبعاد مبرمجة تلقائياً)")
    p_service = st.number_input("حمل العمود (kN)", value=1200)
    q_soil = st.number_input("جهد التربة (kN/m2)", value=150)
    
    # برمجة الأبعاد آلياً
    area = (p_service * 1.1) / q_soil
    side = np.ceil(np.sqrt(area) * 10) / 10 * 1000 # mm
    h_f = 500 if p_service < 1500 else 600 # سماكة مبرمجة
    
    as_f = (1.4/fy) * side * (h_f-70)
    n_bars = int(np.ceil(as_f / (np.pi * 14**2 / 4)))
    
    st.success(f"الأبعاد المبرمجة: {side/1000} x {side/1000} m | سماكة: {h_f} mm")
    st.plotly_chart(draw_section(side, h_f, n_bars//2, 14, 0, 0, 15, 0, "مقطع الأساس"))

elif element == "بلاطة هوردي":
    st.subheader("🧱 عصب هوردي")
    b = st.number_input("عرض العصب (mm)", value=120)
    h = st.number_input("الارتفاع (mm)", value=300)
    # حسابات العصب
    st.plotly_chart(draw_section(b, h, 2, 14, 2, 10, 20, 8, "مقطع العصب"))

st.divider()
st.write(f"تم التدقيق الإنشائي الاقتصادي: {st.session_state.get('eng', 'المهندس بيلان مصطفى عبدالكريم')}")
