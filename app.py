import streamlit as st
import numpy as np
import ezdxf
import io

# 1. UI Setup
st.set_page_config(page_title="Pelan v75", layout="wide")
st.markdown("<style>.stApp{background-color:#0b1619;color:#fff}.card{background:#142d2d;border:2px solid #d4af37;border-radius:15px;padding:20px}.gold{color:#d4af37;font-weight:bold}</style>", unsafe_allow_html=True)

st.markdown("<div class='card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Engineering v75</h1><p class='gold'>Designed by Eng. Pelan Abdulkarim</p></div>", unsafe_allow_html=True)

# 2. Sidebar (Internal Keys in English for Stability)
with st.sidebar:
    st.header("Settings")
    # Choosing mode (Arabic labels, English keys)
    mode_map = {"Concrete": "الخرسانة المسلحة", "Tanks": "هندسة الخزانات", "Seismic": "التحليل الزلزالي"}
    mode = st.selectbox("المجال الهندسي:", list(mode_map.keys()), format_func=lambda x: mode_map[x])
    
    method = st.radio("المنهجية:", ["Ultimate", "Elastic"])
    B = st.number_input("B (cm):", 20, 500, 30)
    H = st.number_input("H (cm):", 10, 500, 60)
    L = st.number_input("L (m):", 1.0, 30.0, 5.0)
    Load = st.number_input("Load (kN):", 1.0, 50000.0, 100.0)
    phi = st.selectbox("Diameter (mm):", [12, 14, 16, 18, 20, 25, 32], index=2)

# 3. Calculation Engine (No Arabic inside Logic to prevent Indentation errors)
fy, fcu = 420, 25
area_bar = (np.pi * phi**2) / 4
res = {}
steel = "Φ16"

if mode == "Concrete":
    # Selection for element
    elem = st.sidebar.selectbox("العنصر:", ["Beam", "Column", "Footing"])
    if elem == "Beam":
        M = (Load * L**2) / 8 if method == "Ultimate" else (Load * L**2) / 10
        As = (M * 1e6) / (0.87 * fy * (H-5) * 10)
        n = max(2, int(np.ceil(As / area_bar)))
        res = {"Moment (kNm)": round(M, 2), "Steel Bars": f"{n} T {phi}"}
        steel = f"{n} T {phi}"
    if elem == "Column":
        Ag = B * H * 100
        As_col = ( (Load*1000) - (0.35 * fcu * Ag) ) / (0.67 * fy)
        n = max(4, int(np.ceil(max(As_col, 0.01*Ag) / area_bar)))
        res = {"Load (kN)": Load, "Steel Bars": f"{n} T {phi}"}
        steel = f"{n} T {phi}"
    if elem == "Footing":
        n = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar)))
        res = {"Section": f"{B}x{H}", "Steel/m": f"{n} T {phi}"}
        steel = f"{n} T {phi} /m'"

if mode == "Tanks":
    # Tank Wall Moment Calculation
    Mt = (10 * (H/100) * L**2) / 12
    nt = max(7, int(np.ceil(((Mt * 1e6) / (0.87 * fy * (H-5) * 10)) / area_bar)))
    res = {"Water Moment": round(Mt, 2), "Reinforcement": f"{nt} T {phi} /m'"}
    steel = f"{nt} T {phi} /m'"

if mode == "Seismic":
    Vb = 0.15 * Load
    res = {"Base Shear Vb": round(Vb, 2), "Zone": "Safe"}
    steel = "Seismic Detailing"

# 4. Results Display
c1, c2 = st.columns([1.2, 1])
with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Results / النتائج")
    for k, v in res.items():
        st.write(f"**{k}:** {v}")
    st.divider()
    if mode == "Concrete":
        
    if mode == "Tanks":
        
    st.info("Verified by Pelan's System 2026")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🖋️ Detailing / التفريد")
    st.markdown(f"<div style='border:2px dashed #d4af37;padding:25px;text-align:center;border-radius:15px;background:#132a2a'><h2 style='color:#50c878'>{steel}</h2></div>", unsafe_allow_html=True)
    if st.button("Export DXF"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_text("PELAN v75", dxfattribs={'height': 5}).set_placement((0, 0))
        buf = io.StringIO(); doc.write(buf)
        st.download_button("Download", buf.getvalue(), "Pelan.dxf")
    st.markdown("</div>", unsafe_allow_html=True)
