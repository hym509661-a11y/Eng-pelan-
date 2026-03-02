import streamlit as st
import numpy as np
import plotly.graph_objects as go

# إعداد الصفحة والختم
st.set_page_config(page_title="منظومة المهندس بيلان", layout="wide")

st.markdown(f"""
    <div style="direction: rtl; text-align: right; border: 2px solid #2e7d32; padding: 10px; border-radius: 10px; background-color: #f9fdf9;">
        <h2 style="color: #1b5e20; margin:0;">المهندس المدني بيلان مصطفى عبدالكريم</h2>
        <p style="margin:5px;">دراسات - إشراف - تعهدات | <b>0998449697</b></p>
    </div>
""", unsafe_allow_html=True)

# ثوابت المواد
st.sidebar.header("⚙️ ثوابت المواد")
fcu = st.sidebar.slider("المقاومة fcu (MPa)", 20, 35, 25)
fy = st.sidebar.selectbox("حديد التسليح fy (MPa)", [240, 360, 400], index=2)
f_prime_c = 0.8 * fcu

choice = st.sidebar.radio("اختر العنصر:", ["جوائز ساقطة", "جوائز مخفية", "أعمدة", "بلاطة هوردي", "أساسات (أبعاد مبرمجة)"])

# --- محرك الرسم الهندسي مع إظهار الأبعاد ---
def draw_detailed_section(b, h, n_low, dia_low, n_up, dia_up, spacing, s_dia, title):
    fig = go.Figure()
    
    # 1. رسم المقطع الخرساني
    fig.add_shape(type="rect", x0=0, y0=0, x1=b, y1=h, line=dict(color="black", width=3), fillcolor="rgba(128,128,128,0.1)")
    
    # 2. إضافة الأبعاد على الرسم (Dimensions)
    fig.add_annotation(x=b/2, y=h+50, text=f"B = {int(b)} mm", showarrow=False, font=dict(size=14, color="black"))
    fig.add_annotation(x=-60, y=h/2, text=f"H = {int(h)} mm", textangle=-90, showarrow=False, font=dict(size=14, color="black"))
    
    # 3. رسم الكانة
    fig.add_shape(type="rect", x0=25, y0=25, x1=b-25, y1=h-25, line=dict(color="blue", width=2))
    
    # 4. توزيع التسليح
    if n_low > 0:
        for i in range(n_low):
            x = 45 + (i * (b-90)/(max(1, n_low-1)))
            fig.add_trace(go.Scatter(x=[x], y=[45], mode="markers", marker=dict(size=dia_low*1.2, color="red"), showlegend=False))
    
    if n_up > 0:
        for i in range(n_up):
            x = 45 + (i * (b-90)/(max(1, n_up-1)))
            fig.add_trace(go.Scatter(x=[x], y=[h-45], mode="markers", marker=dict(size=dia_up*1.2, color="green"), showlegend=False))

    # 5. التسميات الفنية
    fig.add_annotation(x=b/2, y=-60, text=f"سفلي: {int(n_low)}T{dia_low}", showarrow=False, font=dict(color="red", size=15))
    fig.add_annotation(x=b/2, y=h+100, text=f"علوي: {int(n_up)}T{dia_up}", showarrow=False, font=dict(color="green", size=15))
    if spacing > 0:
        fig.add_annotation(x=b+80, y=h/2, text=f"كانات T{s_dia}@{spacing}cm", textangle=90, showarrow=False, font=dict(color="blue", size=14))

    fig.update_layout(xaxis_visible=False, yaxis_visible=False, height=500, width=600, plot_bgcolor="white", title=title, margin=dict(t=120, b=100))
    return fig

# --- تطبيق منطق التصميم ---
if "جوائز" in choice or "هوردي" in choice:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📥 المدخلات (يدوية)")
        b = st.number_input("العرض b (mm)", value=300 if "ساقطة" in choice else 800 if "مخفية" in choice else 120)
        h = st.number_input("الارتفاع h (mm)", value=500 if "ساقطة" in choice else 320 if "مخفية" in choice else 300)
        L = st.number_input("المجاز L (m)", value=5.0)
        wu = st.number_input("الحمولة التصعيدية (kN/m)", value=30.0 if "جوائز" in choice else 6.0)
        
        # حسابات اقتصادية (جامعة دمشق)
        d = h - 45
        mu = (wu * L**2) / 10 # عزم مستمر
        as_req = (mu * 1e6) / (0.9 * fy * 0.9 * d)
        as_min = (1.4/fy) * b * d
        as_final = max(as_req, as_min)
        
        # تحديد الأقطار والتباعد مبرمج
        n_low = int(np.ceil(as_final / (np.pi * 16**2 / 4)))
        n_up = max(2, int(n_low * 0.3))
        spacing = 15 if (wu * L / 2) < (0.17 * np.sqrt(f_prime_c) * b * d / 1000) else 10
        
    with col2:
        st.plotly_chart(draw_detailed_section(b, h, n_low, 16, n_up, 12, spacing, 8, f"مقطع {choice}"))

elif choice == "الأعمدة":
    col1, col2 = st.columns([1, 2])
    with col1:
        b = st.number_input("العرض B (mm)", value=300)
        h = st.number_input("العمق H (mm)", value=500)
        pu = st.number_input("الحمل Pu (kN)", value=1500)
        ast = 0.01 * b * h # نسبة 1% اقتصادية
        n_bars = int(np.ceil(ast / (np.pi * 16**2 / 4)))
        if n_bars % 2 != 0: n_bars += 1
    with col2:
        st.plotly_chart(draw_detailed_section(b, h, n_bars//2, 16, n_bars//2, 16, 15, 8, "مقطع عمود"))

elif choice == "أساسات (أبعاد مبرمجة)":
    col1, col2 = st.columns([1, 2])
    with col1:
        p_service = st.number_input("حمل العمود (kN)", value=1200)
        q_soil = st.number_input("جهد التربة (kN/m2)", value=150)
        
        # برمجة الأبعاد تلقائياً
        area = (p_service * 1.1) / q_soil
        side = np.ceil(np.sqrt(area) * 10) / 10 * 1000 # بالـ mm
        h_f = 500 if p_service < 1200 else 600
        
        as_f = (1.4/fy) * side * (h_f-70)
        n_bars = int(np.ceil(as_f / (np.pi * 14**2 / 4)))
        
        st.success(f"الأبعاد المحسوبة: {side/1000}m x {side/1000}m")
        st.success(f"السماكة المحسوبة: {h_f} mm")
        
    with col2:
        st.plotly_chart(draw_detailed_section(side, h_f, n_bars, 14, 0, 0, 0, 0, "مقطع أساس مبرمج"))

st.divider()
st.info(f"الختم المهني: م. بيلان مصطفى عبدالكريم | 0998449697")
