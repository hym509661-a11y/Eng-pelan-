import streamlit as st
import pandas as pd
import numpy as np

# إعدادات الواجهة الهندسية الاحترافية
st.set_page_config(page_title="Eng. Pelan - Structural Station", layout="wide")

# --- الختم الهندسي الشخصي (التزام بالتعليمات الخاصة) ---
def pelan_stamp():
    st.sidebar.markdown(f"""
    <div style="background-color:#111827; padding:25px; border-radius:15px; border: 2px solid #38bdf8; text-align:center;">
        <h2 style="color:#38bdf8; margin:0; font-family:Arial;">المهندس بيلان مصطفى</h2>
        <h3 style="color:#f3f4f6; margin:5px 0;">عبدالكريم</h3>
        <p style="color:#60a5fa; font-size:0.9em;">Eng. Pelan Mustfa Abdulkarim</p>
        <hr style="border-color:#1f2937;">
        <p style="color:#fbbf24; font-size:1.3em; font-weight:bold;">0998449697</p>
        <p style="color:#9ca3af; font-size:0.7em;">Licensed Structural BIM Expert v2026</p>
    </div>
    """, unsafe_allow_html=True)

pelan_stamp()

# --- واجهة محاكي البرامج الهندسية ---
st.title("🚀 Pelan Integrated Engineering Hub")
st.info("نظام موحد يجمع AutoCAD, ETABS, SAFE, و Revit في بيئة عمل واحدة")

# ألسنة العمل (Workspaces)
tabs = st.tabs(["📐 AutoCAD Workspace", "📊 ETABS Analysis", "🏗️ SAFE Detailing", "🧱 Revit BIM", "📄 BBS & Reports"])

# 1. بيئة الأوتوكاد (AutoCAD Pro)
with tabs[0]:
    st.header("AutoCAD Professional Interface")
    col_tools, col_screen = st.columns([1, 3])
    with col_tools:
        st.subheader("Draw & Modify")
        st.button("Line (L)")
        st.button("Circle (C)")
        st.button("Match Properties (MA)")
        st.divider()
        st.selectbox("OSNAP Settings", ["Node", "Perpendicular", "Nearest"])
        st.file_uploader("Sync DWG from Desktop", type=['dxf'])
    with col_screen:
        st.markdown("""<div style="background-color:#000; height:400px; border:4px solid #333; color:#0f0; font-family:monospace; padding:15px;">
        AutoCAD 2026 Engine Ready... <br>
        [ Eng. Pelan ] - Initializing Master Grid... <br>
        Crosshair: (450.23, 120.55, 0.00) <br><br>
        <div style="border:1px solid #0f0; width:80%; height:200px; margin:auto; text-align:center;"><br><br> FLOOR PLAN VIEW </div>
        </div>""", unsafe_allow_html=True)

# 2. بيئة الإيتابس (ETABS - مع نظام التنبيهات)
with tabs[1]:
    st.header("ETABS: Structural FEA Solver")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Load Definition")
        dl = st.number_input("Dead Load", 4.0)
        ll = st.number_input("Live Load", 2.5)
    with c2:
        st.subheader("Safety Factors")
        phi = st.slider("Strength Reduction (Φ)", 0.65, 0.90, 0.90)
    with c3:
        st.subheader("Status")
        if st.button("RUN CALCULATION"):
            st.success("Finite Element Analysis Complete.")
            st.session_state['analysis'] = True

    if st.session_state.get('analysis'):
        st.write("**Moment & Shear Distribution (ETABS Results)**")
        st.line_chart(np.random.randn(30, 2))
        

# 3. بيئة السيف (SAFE - مخرجات تفصيلية ذكية)
with tabs[2]:
    st.header("SAFE Reinforcement Detailing")
    st.write(f"Design Check for: **Eng. Pelan Mustfa Abdulkarim**")
    
    # محاكاة لفحص الحديد (تنبيهات ذكية)
    as_req = st.number_input("Required Steel Area (As_req) mm²", 800)
    as_prov = st.number_input("Provided Steel Area (As_prov) mm²", 750)
    
    if as_prov < as_req:
        st.error(f"⚠️ WARNING: Reinforcement Deficiency! Need {as_req - as_prov} mm² more.")
    else:
        st.success("✅ Design Pass: Reinforcement meets code requirements.")

    st.subheader("Beam Reinforcement Schedule (30x70)")
    # تفاصيل دقيقة (علوي، سفلي، كانات، تعليق، برندات)
    st.table({
        "Type": ["Top (علوي)", "Bottom (سفلي)", "Stirrups (الكانات)", "Hangers (تعليق)", "Side Bars (برندات)"],
        "Details": ["4 Ø 16", "5 Ø 18", "Ø 10 @ 150mm", "2 Ø 12", "2 Ø 10"],
        "Role": ["Main Support", "Span Flexure", "Shear Resistance", "Cage Support", "Torsion/Skin"]
    })
    

# 4. بيئة الريفيت (Revit & BIM LOD 400)
with tabs[3]:
    st.header("Revit BIM - Model Coordination")
    st.markdown("---")
    col_rev1, col_rev2 = st.columns(2)
    with col_rev1:
        st.image("https://img.icons8.com/color/96/autodesk-revit.png", width=60)
        st.metric("Total Rebar Weight", "12.4 Tons", "+1.2T change")
        st.metric("Concrete Volume", "145 m³")
    with col_rev2:
        st.info("BIM Execution Plan (BEP) Active. All structural families are hosted by Eng. Pelan's custom template.")
        st.checkbox("Show 3D Rebar in View", True)

# 5. جدول الكميات (BBS Report)
with tabs[4]:
    st.header("Final Bar Bending Schedule (BBS)")
    st.write(f"Verified by: Eng. Pelan Mustfa Abdulkarim | 📱 0998449697")
    
    bbs_final = pd.DataFrame({
        "Bar Mark": ["B1-01", "B1-02", "B1-S1", "S1-M1"],
        "Type": ["Bottom Main", "Top Main", "Stirrups", "Slab Mesh"],
        "Diameter (mm)": [18, 16, 10, 12],
        "Count": [4, 4, 45, 150],
        "Total Weight (kg)": [62.4, 48.2, 41.7, 134.5]
    })
    st.dataframe(bbs_final, use_container_width=True)
    
    csv = bbs_final.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Project BBS (Excel)", data=csv, file_name="Pelan_Final_BBS.csv")

# --- التذييل النهائي (The Stamp) ---
st.markdown("---")
st.markdown(f"<h2 style='text-align: center; color: #38bdf8;'>Eng. Pelan Mustfa Abdulkarim</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>Structural BIM Integration | AutoCAD • ETABS • SAFE • Revit | 📞 0998449697</p>", unsafe_allow_html=True)
