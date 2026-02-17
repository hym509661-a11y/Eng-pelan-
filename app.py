import streamlit as st
import plotly.graph_objects as go

def generate_3d_model(L_x, L_y, h_slab, h_beam, col_dim, foot_dim):
    fig = go.Figure()

    # 1. رسم الأساس (Footing) - قاعدة المبنى
    fig.add_trace(go.Mesh3d(
        x=[0, foot_dim, foot_dim, 0, 0, foot_dim, foot_dim, 0],
        y=[0, 0, foot_dim, foot_dim, 0, 0, foot_dim, foot_dim],
        z=[-0.5, -0.5, -0.5, -0.5, 0, 0, 0, 0],
        color='brown', opacity=0.8, name='الأساس'
    ))

    # 2. رسم العمود (Column)
    z_height = 3.0 # ارتفاع الطابق
    fig.add_trace(go.Mesh3d(
        x=[foot_dim/2-col_dim/2, foot_dim/2+col_dim/2, foot_dim/2+col_dim/2, foot_dim/2-col_dim/2, 
           foot_dim/2-col_dim/2, foot_dim/2+col_dim/2, foot_dim/2+col_dim/2, foot_dim/2-col_dim/2],
        y=[foot_dim/2-col_dim/2, foot_dim/2-col_dim/2, foot_dim/2+col_dim/2, foot_dim/2+col_dim/2, 
           foot_dim/2-col_dim/2, foot_dim/2-col_dim/2, foot_dim/2+col_dim/2, foot_dim/2+col_dim/2],
        z=[0, 0, 0, 0, z_height, z_height, z_height, z_height],
        color='grey', opacity=1, name='العمود'
    ))

    # 3. رسم البلاطة (Slab)
    fig.add_trace(go.Mesh3d(
        x=[-L_x/2+foot_dim/2, L_x/2+foot_dim/2, L_x/2+foot_dim/2, -L_x/2+foot_dim/2, 
           -L_x/2+foot_dim/2, L_x/2+foot_dim/2, L_x/2+foot_dim/2, -L_x/2+foot_dim/2],
        y=[-L_y/2+foot_dim/2, -L_y/2+foot_dim/2, L_y/2+foot_dim/2, L_y/2+foot_dim/2, 
           -L_y/2+foot_dim/2, -L_y/2+foot_dim/2, L_y/2+foot_dim/2, L_y/2+foot_dim/2],
        z=[z_height, z_height, z_height, z_height, z_height+0.2, z_height+0.2, z_height+0.2, z_height+0.2],
        color='blue', opacity=0.3, name='البلاطة'
    ))

    fig.update_layout(title="المنظور الإنشائي للمبنى", scene=dict(
        xaxis_title='X (m)', yaxis_title='Y (m)', zaxis_title='Z (m)'))
    
    st.plotly_chart(fig, use_container_width=True)

# استدعاء الدالة (بقيم افتراضية أو من المدخلات السابقة)
st.divider()
st.subheader("📊 العرض ثلاثي الأبعاد والتقرير النهائي")
if st.button("تحديث المنظور 3D"):
    generate_3d_model(L_x=5, L_y=6, h_slab=0.2, h_beam=0.6, col_dim=0.4, foot_dim=1.5)

st.markdown(f"--- \n **المصمم الإنشائي المتكامل | 📞 0998449697**")
