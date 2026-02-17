import streamlit as st
from PyNite import Visualization
from PyNite.FEModel3D import FEModel3D
import pandas as pd

st.set_page_config(page_title="Pro Structural Analyzer", layout="wide")
st.title("🏗️ نظام التحليل الإنشائي المتقدم (FEA Engine)")

# 1. إعداد النموذج (مثل ميكانيكا ETABS)
model = FEModel3D()

# إضافة العقد (Nodes)
model.add_node('N1', 0, 0, 0)
model.add_node('N2', 6, 0, 0) # كمرة بطول 6 متر

# تعريف المادة والمقطع (Material & Section)
E = 25000000 # kN/m2
G = 10000000
Iz = 0.0005   # Inertia
Iy = 0.0002
J = 0.0001
A = 0.12     # Area (30x40 cm)

# إضافة العنصر (Member)
model.add_member('M1', 'N1', 'N2', E, G, Iy, Iz, J, A)

# 2. الشروط الحدودية والتحميل (Supports & Loads)
model.def_support('N1', True, True, True, True, True, True) # وثاقة
model.def_support('N2', True, True, True, True, True, True) # وثاقة

# إضافة حمل موزع (مثل Safe)
model.add_member_dist_load('M1', 'FY', -20, -20) # 20 kN/m

# 3. معالجة التحليل (Solver)
if st.button('تشغيل التحليل الإنشائي الحقيقي'):
    model.analyze()
    
    st.subheader("✅ نتائج التحليل (Output Data)")
    
    # استخراج العزوم وردود الأفعال
    m_max = model.get_member('M1').max_moment('Mz')
    r_y = model.get_node('N1').RxnFY
    
    col1, col2 = st.columns(2)
    col1.metric("أقصى عزم (Max Moment)", f"{round(m_max, 2)} kN.m")
    col2.metric("رد الفعل الرأسي (Reaction)", f"{round(r_y, 2)} kN")

    # عرض الجداول (Excel Style)
    st.write("### جدول عزوم العقد")
    results = {"Node": ["N1", "N2"], "Reaction FY (kN)": [model.get_node('N1').RxnFY, model.get_node('N2').RxnFY]}
    st.table(pd.DataFrame(results))

    st.success("التحليل تم باستخدام محرك Finite Element Method (FEM)")

st.markdown("---")
st.write("للتواصل والدعم الفني: **0998449697**")
