import streamlit as st
import numpy as np
import ezdxf
import io

# 1. Professional UI Configuration
st.set_page_config(page_title="Pelan Pro v77", layout="wide")

# Custom CSS for Professional Dark Gold Theme
st.markdown("""
<style>
    .reportview-container { background: #0e1117; }
    .main-card { background: #1a1c23; border: 1px solid #d4af37; border-radius: 10px; padding: 25px; color: white; }
    .metric-box { background: #262730; border-left: 5px solid #d4af37; padding: 15px; border-radius: 5px; margin: 10px 0; }
    .stButton>button { background-color: #d4af37; color: black; width: 100%; border-radius: 5px; font-weight: bold; }
    h1, h2, h3 { color: #d4af37 !important; }
</style>
""", unsafe_allow_html=True)

# 2. Engineering Engine (Independent Functions)
def calc_concrete(elem, B, H, L, P, phi, meth):
    area_bar = (np.pi * phi**2) / 4
    if elem == "Beam":
        M = (P * L**2) / 8 if meth == "Ultimate" else (P * L**2) / 10
        As = (M * 1e6) / (0.87 * 420 * (H-5) * 10)
        n = max(2, int(np.ceil(As / area_bar)))
        return {"Moment (kNm)": round(M, 2), "Steel": f"{n} T {phi}"}, f"{n} T {phi}"
    elif elem == "Column":
        Ag = B * H * 100
        As_col = ((P*1000) - (0.35 * 25 * Ag)) / (0.67 * 420)
        n = max(4, int(np.ceil(max(As_col, 0.01*Ag) / area_bar)))
        return {"Axial Load (kN)": P, "Reinforcement": f"{n} T {phi}"}, f"{n} T {phi}"
    return {}, "Φ16"

def calc_tank(H, L, phi):
    area_bar = (np.pi * phi**2) / 4
    Mt = (10 * (H/100) * L**2) / 12
    nt = max(7, int(np.ceil(((Mt * 1e6) / (0.87 * 420 * (H-5) * 10)) / area_bar)))
    return {"Wall Moment": round(Mt, 2), "Wall Steel": f"{nt} T {phi} /m'"}, f"{nt} T {phi} /m'"

# 3. Sidebar Inputs
st.sidebar.header("📂 Project Manager")
domain = st.sidebar.selectbox("Design Domain", ["Concrete Structure", "Water Tanks", "Seismic Analysis"])
meth = st.sidebar.radio("Methodology", ["Ultimate", "Elastic"])

st.sidebar.header("📏 Dimensions & Loads")
B = st.sidebar.number_input("Width B (cm)", 20, 500, 30)
H = st.sidebar.number_input("Height H (cm)", 10, 500, 60)
L = st.sidebar.number_input("Length L (m)", 1.0, 50.0, 5.0)
P = st.sidebar.number_input("Design Load (kN)", 1.0, 100000.0, 150.0)
phi = st.sidebar.selectbox("Bar Diameter (mm)", [12, 14, 16, 18, 20, 25, 32], index=2)

# 4. Main Interface Logic
st.markdown("<div class='main-card' style='text-align:center;'><h1>🏗️ Pelan Professional Suite v77</h1><p>Integrated Engineering Design Solution | 2026</p></div>", unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📊 Engineering Analysis")
    results, bar_desc = {}, "Φ16"
    
    if domain == "Concrete Structure":
        elem = st.selectbox("Select Element", ["Beam", "Column"])
        results, bar_desc = calc_concrete(elem, B, H, L, P, phi, meth)
        
    
    elif domain == "Water Tanks":
        results, bar_desc = calc_tank(H, L, phi)
        
        
    elif domain == "Seismic Analysis":
        vb = 0.15 * P
        results = {"Base Shear (Vb)": f"{vb:.2f} kN", "Seismic Zone": "Zone 2B"}
        bar_desc = "Capped Bars"

    for k, v in results.items():
        st.markdown(f"<div class='metric-box'><b>{k}:</b> {v}</div>", unsafe_allow_html=True)

with col2:
    st.subheader("🖋️ Detailing & BBS")
    st.markdown(f"""
    <div style='background:#132a2a; border:2px dashed #d4af37; border-radius:15px; padding:40px; text-align:center;'>
        <h1 style='color:#50c878; margin:0;'>{bar_desc}</h1>
        <small style='color:#d4af37;'>Design Description</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    if st.button("🚀 Export AutoCAD (DXF)"):
        doc = ezdxf.new(setup=True)
        doc.modelspace().add_text(f"PELAN PRO v77 - {domain}", dxfattribs={'height': 7})
        buf = io.StringIO()
        doc.write(buf)
        st.download_button("📥 Download Drawing", buf.getvalue(), "Pelan_Pro.dxf")

st.markdown("<p style='text-align:center; color:gray;'>Professional Edition © 2026 Eng. Pelan Abdulkarim</p>", unsafe_allow_html=True)
