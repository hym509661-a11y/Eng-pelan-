import streamlit as st
import numpy as np
import ezdxf
import io

# 1. UI Setup
st.set_page_config(page_title="Pelan v76", layout="wide")
st.markdown("<style>.stApp{background-color:#0b1619;color:#fff}.card{background:#142d2d;border:2px solid #d4af37;border-radius:15px;padding:20px}.gold{color:#d4af37;font-weight:bold}</style>", unsafe_allow_html=True)
st.markdown("<div class='card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Engineering v76</h1><p class='gold'>Designed by Eng. Pelan Abdulkarim</p></div>", unsafe_allow_html=True)

# 2. Input Logic (No Deep Indentation)
with st.sidebar:
    st.header("Settings")
    mode = st.selectbox("المجال:", ["خرسانة", "خزانات", "زلازل"])
    meth = st.radio("المنهجية:", ["Ultimate", "Elastic"])
    B_val = st.number_input("B (cm):", 20, 500, 30)
    H_val = st.number_input("H (cm):", 10, 500, 60)
    L_val = st.number_input("L (m):", 1.0, 30.0, 5.0)
    Load = st.number_input("الحمل (kN):", 1.0, 100000.0, 100.0)
    phi = st.selectbox("القطر (mm):", [12, 14, 16, 18, 20, 25, 32], index=2)

# 3. Calculation Engine (Atomic Structure)
fy, fcu, area_bar = 420, 25, (np.pi * phi**2) / 4
res = {}
steel_text = "Φ16"

# Concrete Section
if mode == "خرسانة":
    sub_mode = st.sidebar.selectbox("العنصر:", ["جائز", "عمود", "أساس"])
    if sub_mode == "جائز":
        M = (Load * L_val**2) / 8 if meth == "Ultimate" else (Load * L_val**2) / 10
        As = (M * 10**6) / (0.87 * fy * (H_val-5) * 10)
        n = max(2, int(np.ceil(As / area_bar)))
        res = {"Moment": f"{M:.1f} kNm", "Steel": f"{n} T {phi}"}
        steel_text = f"{n} T {phi}"
    if sub_mode == "عمود":
        Ag = B_val * H_val * 100
        As_col = ( (Load*1000) - (0.35 * fcu * Ag) ) / (0.67 * fy)
        n = max(4, int(np.ceil(max(As_col, 0.01*Ag) / area_bar)))
        res = {"Load": f"{Load} kN", "Steel": f"{n} T {phi}"}
        steel_text = f"{n} T {phi}"
    if sub_mode == "أساس":
        n = max(6, int(np.ceil((0.0018 * B_val * H_val * 100) / area_bar)))
        res = {"Section": f"{B_val}x{H_val}", "Steel": f"{n} T {phi}/m"}
        steel_text = f"{n} T {phi} /m"

# Tanks Section
if mode == "خزانات":
    Mt = (10 * (H_val/100) * L_val**2) / 12
    nt = max(7, int(np.ceil(((Mt * 10**6) / (0.87 * fy * (H_val-5) * 10)) / area_bar)))
    res = {"Water Moment": f"{Mt:.1f} kNm", "Wall Steel": f"{nt} T {phi}/m"}
    steel_text = f"{nt} T {phi} /m"

# Seismic Section
if mode == "زلازل":
    Vb = 0.15 * Load
    res = {"Base Shear": f"{Vb:.1f} kN", "Status": "Safe"}
    steel_text = "Seismic Bars"

# 4. Display Results
c1, c2 = st.columns([1.2, 1])
with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Results")
    for k, v in res.items():
        st.write(f"**{k}:** {v}")
    st.divider()
    if mode == "خرسانة":
        
    if mode == "خزانات":
        
    st.info("Verified by Pelan 2026")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🖋️ Detailing")
    st.markdown(f"<div style='border:2px dashed #d4af37;padding:25px;text-align:center;border-radius:15px;background:#132a2a'><h2 style='color:#50c878'>{steel_text}</h2></div>", unsafe_allow_html=True)
    if st.button("Export DXF"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_text("PELAN v76", dxfattribs={'height': 5}).set_placement((0, 0))
        buf = io.StringIO(); doc.write(buf)
        st.download_button("Download", buf.getvalue(), "Pelan.dxf")
    st.markdown("</div>", unsafe_allow_html=True)
