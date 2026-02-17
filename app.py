import streamlit as st
import plotly.graph_objects as go
import numpy as np

# إعدادات الواجهة
st.set_page_config(page_title="المصمم الإنشائي التفصيلي", layout="wide")
st.sidebar.title("🏗️ تفاصيل التسليح 3D")
st.sidebar.info("المهندس المسؤول: 0998449697")

def draw_detailed_structure():
    st.header("🔍 المنظور التفصيلي لحديد التسليح")
    
    # مدخلات المستخدم
    col1, col2 = st.columns(2)
    with col1:
        n_layers = st.number_input("عدد الطوابق", min_value=1, value=1)
        slab_rebar_phi = st.selectbox("قطر حديد البلاطة (mm)", [8, 10, 12, 14])
    with col2:
        col_rebar_count = st.number_input("عدد أسياخ العمود", min_value=4, step=2, value=8)
        col_rebar_phi = st.selectbox("قطر حديد العمود (mm)", [14, 16, 18, 20, 25])

    fig = go.Figure()

    # إحداثيات افتراضية للعنصر (عمود + بلاطة)
    c_x, c_y = 0.4, 0.4 # أبعاد العمود
    s_w, s_l = 4.0, 5.0 # أبعاد البلاطة

    for f in range(n_layers):
        z_base = f * 3.0
        
        # 1. رسم خرسانة العمود (شفافة)
        fig.add_trace(go.Mesh3d(
            x=[0, c_x, c_x, 0, 0, c_x, c_x, 0],
            y=[0, 0, c_y, c_y, 0, 0, c_y, c_y],
            z=[z_base, z_base, z_base, z_base, z_base+3, z_base+3, z_base+3, z_base+3],
            color='lightgrey', opacity=0.2, name=f'بيتون العمود - طابق {f+1}'
        ))

        # 2. رسم أسياخ حديد العمود (خطوط عمودية)
        rebar_pos = [(0.05, 0.05), (c_x-0.05, 0.05), (c_x-0.05, c_y-0.05), (0.05, c_y-0.05), (0.05, c_y/2), (c_x-0.05, c_y/2)]
        for i, (px, py) in enumerate(rebar_pos[:col_rebar_count]):
            fig.add_trace(go.Scatter3d(
                x=[px, px], y=[py, py], z=[z_base, z_base+3],
                mode='lines', line=dict(color='red', width=4),
                name=f'سيخ عمود T{col_rebar_phi}'
            ))
            # كتابة ملاحظة على السيخ الأول
            if i == 0:
                fig.add_trace(go.Scatter3d(x=[px], y=[py], z=[z_base+1.5], mode='text', text=[f"{col_rebar_count}T{col_rebar_phi}"]))

        # 3. رسم حديد البلاطة (شبكة)
        z_slab = z_base + 3.0
        for x_pos in np.linspace(-1, 1, 5): # أسياخ عرضية
            fig.add_trace(go.Scatter3d(
                x=[x_pos + c_x/2 - 1, x_pos + c_x/2 + 1], y=[c_y/2, c_y/2], z=[z_slab, z_slab],
                mode='lines', line=dict(color='blue', width=2), showlegend=False
            ))
        
    fig.update_layout(scene=dict(aspectmode='data'), margin=dict(l=0, r=0, b=0, t=40))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"--- \n **مخطط تفصيلي معتمد | للتواصل: 0998449697**")

draw_detailed_structure()
