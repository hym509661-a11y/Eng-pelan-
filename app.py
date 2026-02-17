import streamlit as st
import plotly.graph_objects as go
import numpy as np
import math

# إعدادات الصفحة
st.set_page_config(page_title="المهندس الإنشائي الآلي", layout="wide")
st.sidebar.title("🏗️ نظام التصميم الذكي")
st.sidebar.info("تطوير وتدقيق: 0998449697")

# --- 1. المعطيات المعمارية والإنشائية ---
st.header("1. المعطيات الأساسية للمشروع")
with st.container():
    c1, c2, c3 = st.columns(3)
    num_floors = c1.number_input("عدد الطوابق", min_value=1, value=1)
    apart_per_floor = c2.selectbox("عدد الشقق/طابق", [1, 2, 3, 4])
    rooms_per_apart = c3.number_input("عدد الغرف/شقة", min_value=1, value=3)

    c4, c5, c6 = st.columns(3)
    Lx = c4.number_input("عرض الغرفة (m)", value=4.0)
    Ly = c5.number_input("طول الغرفة (m)", value=5.0)
    fc = c6.number_input("f'c (MPa)", value=25)

# --- 2. محرك الحسابات الآلي (وفق الكود السوري) ---
# أحمال الكود السوري
DL = 4.5  # kN/m2
LL = 2.0  # kN/m2
qu = (1.4 * DL) + (1.7 * LL)

# أ. تصميم البلاطة (حساب الحديد تلقائياً)
d_slab = 0.12 # الارتفاع الفعال لسماكة 15سم
Mu_slab = (qu * Lx**2) / 8 # عزم تقريبي للبلاطة
# حساب مساحة الحديد As = Mu / (0.9 * fy * 0.9d)
As_slab = (Mu_slab * 10**6) / (0.9 * 400 * 0.9 * d_slab * 1000)
num_bars_slab = math.ceil(As_slab / 78.5) # عدد الأسياخ قطر 10mm لكل متر

# ب. تصميم العمود (تراكمي)
load_per_room = qu * Lx * Ly
total_P = load_per_room * num_floors * 1.1 # حمل العمود مع الوزن الذاتي
# حساب مساحة الحديد المطلوبة للعمود (بفرض نسبة 1%)
Ag_col = (total_P * 1000) / (0.35 * fc + 0.67 * 0.01 * 400)
As_col = 0.01 * Ag_col
num_bars_col = math.ceil(As_col / 154) # عدد الأسياخ قطر 14mm
if num_bars_col < 4: num_bars_col = 4 # الحد الأدنى للكود

# ج. تصميم الأساس
q_all = 200
area_f = (total_P * 1.1) / q_all
side_f = math.sqrt(area_f)

# --- 3. المنظور التفصيلي (الحديد والنتائج) ---
st.markdown("---")
st.header("2. النتائج التفصيلية والمنظور 3D")

col_res1, col_res2 = st.columns([1, 2])

with col_res1:
    st.subheader("📋 جداول التسليح المحسوبة")
    st.write(f"**البلاطة:** T10 كل {100/num_bars_slab:.0f} سم")
    st.write(f"**الجوائز:** {math.ceil(num_bars_slab*1.5)}T14 (تسليح رئيسي)")
    st.write(f"**الأعمدة:** {num_bars_col}T14 (تسليح طولي)")
    st.write(f"**الأساسات:** القاعدة {side_f:.2f}x{side_f:.2f} m")

with col_res2:
    fig = go.Figure()
    # رسم العناصر والحديد
    for f in range(num_floors):
        z = f * 3.0
        # بيتون شفاف
        fig.add_trace(go.Mesh3d(x=[0,0.4,0.4,0,0,0.4,0.4,0], y=[0,0,0.4,0.4,0,0,0.4,0.4], z=[z,z,z,z,z+3,z+3,z+3,z+3], color='grey', opacity=0.1))
        # أسياخ الحديد المحسوبة
        for i in range(num_bars_col):
            angle = (2 * math.pi * i) / num_bars_col
            px, py = 0.2 + 0.15*math.cos(angle), 0.2 + 0.15*math.sin(angle)
            fig.add_trace(go.Scatter3d(x=[px, px], y=[py, py], z=[z, z+3], mode='lines', line=dict(color='red', width=3), showlegend=False))

    fig.update_layout(scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False))
    st.plotly_chart(fig, use_container_width=True)

st.markdown(f"--- \n **تم الحساب والربط آلياً وفق الكود السوري | التدقيق الفني: 0998449697**")
