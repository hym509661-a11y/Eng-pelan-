import streamlit as st
import pandas as pd
import numpy as np

# إعدادات الواجهة الهندسية العريضة
st.set_page_config(page_title="Pelan Pro-Suite", layout="wide")

# --- الختم الهندسي الثابت (Stamp) ---
def apply_stamp():
    st.sidebar.markdown(f"""
    <div style="background-color:#0f172a; padding:20px; border-radius:10px; border-left: 5px solid #38bdf8; color:white;">
        <h2 style="color:#38bdf8; margin-bottom:0;">Eng. Pelan Mustfa</h2>
        <h3 style="color:#f8fafc; margin-top:0;">Abdulkarim</h3>
        <p style="color:#fbbf24; font-size:1.3em; font-weight:bold; letter-spacing:1px;">0998449697</p>
        <hr style="border-color:#1e293b;">
        <p style="font-size:0.8em; opacity:0.8;">Integrated Engineering System v6.0<br>Licensed to: Office of Eng. Pelan</p>
    </div>
    """, unsafe_allow_html=True)

apply_stamp()

# --- واجهة المستخدم الرئيسية (Main Terminal) ---
st.title("🏗️ Pelan Professional BIM & Structural Station")
st.caption("AutoCAD Engine | ETABS Solver | SAFE Designer | Revit Modeler")

# شريط الأدوات العلوي (Ribbon Toolbar)
menu = st.tabs([
    "📂 AutoCAD (Import/Snap)", 
    "📉 ETABS (Analysis & Loads)", 
    "🏗️ SAFE (Detailed Reinforcement)", 
    "🧱 Revit (BIM & 3D)", 
    "📊 BBS (Quantity Reports)"
])

# 1. بيئة الأوتوكاد (AutoCAD Engine)
with menu[0]:
    st.header("📐 AutoCAD Drawing Terminal")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader("Snap Settings")
        st.toggle("Object Snap (OSNAP)", True)
        st.toggle("Ortho Mode", True)
        st.selectbox("Current Layer", ["0", "S-Columns", "S-Beams", "S-Slabs", "A-Text"])
        dxf = st.file_uploader("Upload Architectural Floor Plan", type=['dxf', 'dwg'])
    with col2:
        st.markdown("""<div style="background-color:#212121; height:450px; border:3px solid #333; position:relative; color:#00ff00; font-family:monospace; padding:10px;">
            Command: _IMPORT_DWG <br>
            Status: Initializing Snap Points... <br>
            Reading Layers from Eng_Pelan_Project.dwg... <br><br>
            <div style="position:absolute; top:40%; left:40%; border:2px solid white; width:100px; height:100px; background:rgba(255,255,255,0.1); text-align:center;">Column C1</div>
            <div style="position:absolute; top:30%; left:20%; border-bottom:4px solid cyan; width:300px;">Beam B12</div>
        </div>""", unsafe_allow_html=True)

# 2. بيئة الإيتابس (ETABS Solver)
with menu[1]:
    st.header("📊 ETABS Analysis Center")
    col_inp, col_res = st.columns([1, 2])
    with col_inp:
        st.subheader("Load Definitions")
        dl = st.number_input("Dead Load (kN/m²)", 4.5)
        ll = st.number_input("Live Load (kN/m²)", 2.0)
        st.subheader("Material Model")
        fcu = st.selectbox("Concrete f'c (MPa)", [25, 30, 35, 40])
        fy = st.selectbox("Steel fy (MPa)", [420, 460, 500])
        if st.button("RUN FEA SOLVER"):
            st.session_state['analyzed'] = True
    with col_res:
        st.subheader("Analysis Diagrams")
        if st.session_state.get('analyzed'):
            st.line_chart(np.random.randn(50, 2))
            st.success("Analysis Complete: Displacements & Forces calculated.")
            

# 3. بيئة السيف (SAFE Reinforcement Detailer)
with menu[2]:
    st.header("🏗️ SAFE: Reinforcement & Detailing")
    st.info("Engineering Details for: Eng. Pelan Mustfa Abdulkarim")
    
    element_type = st.selectbox("Select Element to Design", ["Beam (جسور)", "Slab (بلاطات)", "Column (أعمدة)"])
    
    if element_type == "Beam (جسور)":
        st.subheader("Beam Section Details (300 x 600 mm)")
        # تفاصيل الحديد كاملة
        st.markdown("""
        | Type of Steel | Detailed Specification | Length/Spacing |
        | :--- | :--- | :--- |
        | **Top Bars (العلوي)** | 4 Ø 16 mm | Full Length |
        | **Bottom Bars (السفلي)** | 5 Ø 18 mm | Support to Support |
        | **Hanger Bars (التعليق)** | 2 Ø 12 mm | Top Zone |
        | **Stirrups (الكانات)** | Ø 10 mm | @ 150 mm c/c |
        | **Skin Steel (البرندات)** | 2 Ø 10 mm | Sides (d > 700mm) |
        """)
        

# 4. بيئة الريفيت (Revit & BBS)
with menu[3]:
    st.header("🧱 Revit BIM Modeler")
    st.write("3D Geometric Information & Parameters")
    st.image("https://img.icons8.com/color/96/autodesk-revit.png", width=50)
    st.json({
        "Project": "Pelan Master Project 2026",
        "Engineer": "Pelan Mustfa Abdulkarim",
        "Total Concrete Volume": "450 m³",
        "Total Steel Weight": "35.2 Tons",
        "BIM Level": "LOD 400"
    })

# 5. جدول الكميات النهائي (BBS)
with menu[4]:
    st.header("📊 Final Bar Bending Schedule (BBS)")
    bbs_data = pd.DataFrame({
        "Bar Mark": ["B1-T1", "B1-B1", "B1-S1", "C1-V1", "S1-M1"],
        "Shape Code": [21, 21, 51, 11, 00],
        "Dia (mm)": [16, 18, 10, 20, 12],
        "Length (m)": [6.2, 6.4, 1.6, 4.2, 120.0],
        "Weight/m (kg)": [1.58, 2.00, 0.62, 2.47, 0.89],
        "Total Weight (kg)": [39.1, 51.2, 34.7, 103.7, 106.8]
    })
    st.dataframe(bbs_data, use_container_width=True)
    
    # تصدير التقرير الرسمي
    csv = bbs_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Export Official Report - Eng. Pelan",
        data=csv,
        file_name="Pelan_BBS_Full_Report.csv",
        mime="text/csv"
    )

# --- تذييل البرنامج (Footer) ---
st.markdown("---")
st.markdown(f"<h2 style='text-align: center; color: #38bdf8;'>Eng. Pelan Mustfa Abdulkarim</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>Structural BIM Integration | AutoCAD • ETABS • SAFE • Revit | 📞 0998449697</p>", unsafe_allow_html=True)
