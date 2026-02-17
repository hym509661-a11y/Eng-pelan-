import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Jawad Structural Suite", layout="wide")

class JawadEngine:
    @staticmethod
    def design_beam(mu, vu, b, h, fc, fy):
        d = h - 50
        rn = (mu * 10**6) / (0.9 * b * d**2)
        rho = (0.85 * fc / fy) * (1 - np.sqrt(1 - (2 * rn / (0.85 * fc))))
        as_req = max(rho * b * d, 0.0033 * b * d)
        vc = 0.17 * np.sqrt(fc) * b * d / 1000
        vs = (vu / 0.75) - vc
        spacing = min(d/2, 300) if vs <= 0 else min((2 * 78.5 * fy * d) / (vs * 1000), d/2, 300)
        return int(as_req), int(spacing)

    @staticmethod
    def design_column(pu, b, h, fc, fy):
        ac = b * h
        as_req = (pu * 1000 - 0.35 * fc * ac) / (0.67 * fy)
        return int(max(as_req, 0.01 * ac))

    @staticmethod
    def design_wall(h_w, gamma, phi):
        ka = (1 - np.sin(np.radians(phi))) / (1 + np.sin(np.radians(phi)))
        pa = 0.5 * ka * gamma * h_w**2
        ma = pa * (h_w / 3)
        return round(ka, 3), round(pa, 2), round(ma, 2)

    @staticmethod
    def design_raft(p_total, lx, ly, q_allow):
        sigma = p_total / (lx * ly)
        status = "✅ Safe" if sigma <= q_allow else "❌ Overload"
        return round(sigma, 2), status

st.title("🏗️ Jawad Structural Software - Syrian Code Edition")

tabs = st.tabs(["الجسور", "الأعمدة", "الجدران", "اللبشة", "الأدراج"])

with tabs[0]:
    c1, c2 = st.columns(2)
    mu = c1.number_input("العزم Mu (kNm)", value=150.0)
    vu = c1.number_input("القص Vu (kN)", value=100.0)
    b = c1.number_input("العرض b (mm)", value=300)
    h = c1.number_input("الارتفاع h (mm)", value=600)
    as_main, stirrup = JawadEngine.design_beam(mu, vu, b, h, 25, 400)
    c2.metric("التسليح الرئيسي (mm²)", as_main)
    c2.metric("تباعد الأساور (mm)", f"Φ8 @ {int(stirrup)}")
    

with tabs[1]:
    c1, c2 = st.columns(2)
    pu = c1.number_input("الحمل Pu (kN)", value=2000)
    bc = c1.number_input("عرض العمود (mm)", value=400)
    hc = c1.number_input("عمق العمود (mm)", value=400)
    as_col = JawadEngine.design_column(pu, bc, hc, 25, 400)
    c2.metric("تسليح العمود (mm²)", as_col)
    

with tabs[2]:
    c1, c2 = st.columns(2)
    hw = c1.number_input("ارتفاع الجدار (m)", value=4.0)
    gamma = c1.number_input("وزن التربة", value=18)
    phi = c1.number_input("زاوية الاحتكاك", value=30)
    ka, pa, ma = JawadEngine.design_wall(hw, gamma, phi)
    c2.write(f"Ka: {ka} | Pa: {pa} kN | Ma: {ma} kNm")
    

with tabs[3]:
    c1, c2 = st.columns(2)
    pt = c1.number_input("الحمل الكلي (kN)", value=15000)
    lx = c1.number_input("الطول X (m)", value=20.0)
    ly = c1.number_input("العرض Y (m)", value=15.0)
    qa = c1.number_input("إجهاد التربة", value=200)
    sig, stat = JawadEngine.design_raft(pt, lx, ly, qa)
    c2.metric("إجهاد التربة الفعلي", sig)
    c2.write(f"الحالة: {stat}")
    

with tabs[4]:
    st.write("تطابق وحدة الأدراج مع شروط السهم الكود السوري L/20")
    l_h = st.number_input("الطول الأفقي (m)", value=4.0)
    st.write(f"السماكة المقترحة: {round(l_h*1000/20)} mm")
    

st.markdown("---")
st.write("للتواصل والدعم الفني: **0998449697**")
