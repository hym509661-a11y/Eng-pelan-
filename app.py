import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math

# إعدادات الصفحة
st.set_page_config(page_title="المصمم الإنشائي السوري", layout="wide")

# العنوان والختم
st.title("🏗️ البرنامج الهندسي المتكامل (وفق الكود السوري)")
st.sidebar.markdown("### 📞 المطور والمدقق")
st.sidebar.info("المهندس المسؤول: 0998449697")

# --- موديول المدخلات ---
st.header("1. مدخلات المشروع العامة")
col_m1, col_m2 = st.columns(2)
fc = col_m1.number_input("المقاومة المميزة للبيتون f'c (MPa)", value=25)
fy = col_m2.number_input("إجهاد الخضوع للفولاذ fy (MPa)", value=400)

st.markdown("---")

# --- موديول البلاطات ونقل الأحمال ---
st.header("2. البلاطات والجوائز")
c1, c2, c3 = st.columns(3)
Lx = c1.number_input("طول الغرفة Lx (m)", value=4.0)
Ly = c2.number_input("طول الغرفة Ly (m)", value=5.0)
wu = c3.number_input("الحمل المصعد qu (kN/m2)", value=12.0)

r = Ly / Lx
st.write(f"نسبة الاستطالة r = {r:.2f}")

# حساب الحمل المنقول للجائز الطويل (شبه منحرف مكافئ)
if r <= 2:
    w_beam = (wu * Lx / 2) * (1 - (1 / (3 * r**2)))
    st.success(f"الحمل المكافئ على الجائز الطويل: {w_beam:.2f} kN/m")
else:
    w_beam = (wu * Lx) / 2
    st.warning("بلاطة تعمل في اتجاه واحد")

st.markdown("---")

# --- موديول الأعمدة والأساسات ---
st.header("3. الأعمدة والأساسات")
p_service = st.number_input("الحمل التشغيلي الواصل للأساس P (kN)", value=1000.0)
q_allow = st.number_input("إجهاد التربة المسموح (kN/m2)", value=200.0)

# حساب مساحة القاعدة
area_req = (p_service * 1.1) / q_allow
side = math.sqrt(area_req)
st.success(f"أبعاد القاعدة المطلوبة: {side:.2f} x {side:.2f} m")

st.markdown("---")

# --- موديول المنظور 3D ---
st.header("4. المنظور الإنشائي 3D")
if st.button("توليد النموذج ثلاثي الأبعاد"):
    fig = go.Figure()
    # رسم القاعدة
    fig.add_trace(go.Mesh3d(x=[0,side,side,0,0,side,side,0], y=[0,0,side,side,0,0,side,side], z=[-0.5,-0.5,-0.5,-0.5,0,0,0,0], color='brown', name='Base'))
    # رسم العمود
    fig.add_trace(go.Mesh3d(x=[side/2-0.2, side/2+0.2, side/2+0.2, side/2-0.2, side/2-0.2, side/2+0.2, side/2+0.2, side/2-0.2], 
                            y=[side/2-0.2, side/2-0.2, side/2+0.2, side/2+0.2, side/2-0.2, side/2-0.2, side/2+0.2, side/2+0.2], 
                            z=[0,0,0,0,3,3,3,3], color='grey', name='Column'))
    st.plotly_chart(fig)

st.markdown("---")
st.write("تم التصميم والتدقيق وفق الكود العربي السوري | 0998449697")
