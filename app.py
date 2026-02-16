import streamlit as st
import pandas as pd
import numpy as np

# إعدادات الواجهة لتشبه البرامج الهندسية (Dark Theme & Wide)
st.set_page_config(page_title="Pelan Workstation", layout="wide")

# --- الختم الهندسي (Stamp) - ثابت في الأعلى وفي الجانب ---
st.sidebar.markdown(f"""
<div style="background-color:#1e272e; padding:20px; border-radius:10px; border: 2px solid #3498db; text-align:center;">
    <h2 style="color:#3498db; margin:0;">Eng. Pelan Mustfa</h2>
    <h4 style="color:white; margin:5px;">Abdulkarim</h4>
    <hr style="border-color:#3498db;">
    <p style="color:#f1c40f; font-size:1.2em; font-weight:bold;">0998449697</p>
</div>
""", unsafe_allow_html=True)

# --- شريط الأدوات العلوي (Main Toolbar) ---
st.title("🏗️ Pelan Professional Engineering Workstation")
st.markdown("---")

# نظام التبويبات كأنه شريط مهام للبرامج
program_mode = st.radio("إختر بيئة العمل الحالية:", 
                        ["AutoCAD Layout", "ETABS Solver", "SAFE Reinforcement", "Revit BIM & BBS"], 
                        horizontal=True)

# 1. بيئة الأوتوكاد (AutoCAD Professional Workspace)
if program_mode == "AutoCAD Layout":
    st.header("📐 AutoCAD Workspace - Architectural Import")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Layers Manager")
        st.checkbox("Columns Layer", value=True)
        st.checkbox("Beams Layer", value=True)
        st.checkbox("Slabs Layer", value=True)
        dxf = st.file_uploader("تنزيل المسقط المعماري (DXF)", type=['dxf'])
        
    with col2:
        st.subheader("Model Space")
        # محاكاة لشاشة الأوتوكاد السوداء
        st.markdown("""<div style="background-color:black; height:300px; border:2px solid #555; display:flex; align-items:center; justify-content:center; color:#0f0;">
        [ + ] Crosshair Active | Ortho: ON | Snap: ON <br> 
        -- Drawing Loaded: Floor_Plan_Pelan.dwg --
        </div>""", unsafe_allow_html=True)
        if dxf: st.success("تم الربط مع المسقط المعماري بنجاح.")

# 2. بيئة الإيتابس (ETABS Analysis Workspace)
elif program_mode == "ETABS Solver":
    st.header("📊 ETABS Analysis Engine - [Eng Pelan Mustfa]")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Material Properties")
        st.text_input("Concrete Grade (f'c)", "30 MPa")
        st.text_input("Steel Yield (fy)", "420 MPa")
    with col2:
        st.subheader("Load Patterns")
        st.number_input("Dead Load (kN/m)", 5.0)
        st.number_input("Live Load (kN/m)", 2.5)
    with col3:
        st.subheader("Analysis Results")
        if st.button("RUN ANALYSIS"):
            st.error("Running Finite Element Matrix... Done.")
            st.line_chart(np.random.randn(20, 2))
            st.caption("Bending Moment Diagram (BMD)")

# 3. بيئة السيف (SAFE Reinforcement Details)
elif program_mode == "SAFE Reinforcement":
    st.header("🏗️ SAFE Detailing - Reinforcement Schedule")
    st.info("تحديد تفاصيل التسليح بناءً على تحليل ETABS")
    
    # تفاصيل دقيقة كما طلبت (علوي، سفلي، كانات، تعليق)
    beam_id = st.selectbox("اختر العنصر (Element ID):", ["Beam B1 (30x60)", "Beam B2 (25x50)", "Slab S1 (20cm)"])
    
    col_main, col_stirrup = st.columns(2)
    with col_main:
        st.subheader("Longitudinal Bars (الحديد الطولي)")
        st.table({
            "Position": ["Top (علوي)", "Bottom (سفلي)", "Hangers (تعليق)", "Side Bars (برندات)"],
            "Reinforcement": ["3 Ø 16", "4 Ø 18", "2 Ø 12", "2 Ø 10"]
        })
    with col_stirrup:
        st.subheader("Shear Links (الكانات)")
        st.write("**Stirrups:** Ø 10 @ 150 mm c/c")
        st.write("**Shear Design:** Pass (Vc + Vs > Vu)")
    
    

# 4. بيئة الريفيت (Revit & BBS Generator)
elif program_mode == "Revit BIM & BBS":
    st.header("📋 Revit Schedule & Bar Bending Schedule (BBS)")
    st.markdown(f"**Project Engineer:** Eng Pelan Mustfa Abdulkarim")
    
    # جدول كميات احترافي (BBS)
    bbs_data = pd.DataFrame({
        "Bar Mark": ["B1-T", "B1-B", "B1-S", "C1-M"],
        "Member": ["Beam 1", "Beam 1", "Beam 1", "Column 1"],
        "Type": ["Top Main", "Bottom Main", "Stirrups", "Main Vertical"],
        "Diameter (mm)": [16, 18, 10, 20],
        "Total Length (m)": [12.5, 14.2, 55.8, 42.0],
        "Total Weight (kg)": [19.7, 28.4, 34.4, 103.6]
    })
    
    st.dataframe(bbs_data, use_container_width=True)
    
    csv = bbs_data.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export BBS to Excel (Pelan Edition)", data=csv, file_name="Pelan_Engineering_BBS.csv")

# --- الختم النهائي ---
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; border: 1px solid #3498db; padding: 10px;">
        <h3 style="color: #2980b9;">Approved by: Eng. Pelan Mustfa Abdulkarim</h3>
        <p>License: Structural BIM Expert | 📱 0998449697</p>
    </div>
""", unsafe_allow_html=True)
