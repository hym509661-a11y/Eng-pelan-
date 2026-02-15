import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# إعداد واجهة المهندس بيلان عبد الكريم
st.set_page_config(page_title="Bilan-Engineering Pro", layout="wide")

st.markdown("""
    <div style="background-color:#003366;padding:20px;border-radius:15px;text-align:center;">
        <h1 style="color:white;margin:0;">Bilan-Engineering Suite v7.0</h1>
        <p style="color:#00d1ff;font-size:22px;">تصميم: المهندس بيلان عبدالكريم</p>
    </div>
""", unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.header("📂 اختيار العنصر")
    choice = st.selectbox("العنصر المطلوب:", 
        ["جائز (Beam)", "بلاطة مصمتة (Solid)", "بلاطة هوردي (Ribbed)", "أساس (Footing)", "عمود (Column)"])
    
    L = st.number_input("الطول L (m):", 0.5, 20.0, 5.0)
    B = st.number_input("العرض B (cm):", 10.0, 500.0, 30.0)
    h_tot = st.number_input("الارتفاع h (cm):", 10.0, 200.0, 60.0)
    
    if choice == "جائز (Beam)":
        support = st.selectbox("نوع المسند:", ["بسيط", "كابولي", "وثاقة طرفين"])
    
    wu = st.number_input("الحمل Wu (t/m أو t/m2):", 0.1, 1000.0, 2.5)
    phi = st.selectbox("قطر السيخ (mm):", [8, 10, 12, 14, 16, 20, 25])

# المحرك الإنشائي (تم ضبط الإزاحات يدوياً لضمان العمل)
def compute_design():
    fcu, fy = 250, 4000
    d = h_tot - 5
    # الحالة 1: الجوائز والبلاطات
    if choice == "جائز (Beam)" or "Solid" in choice or "Ribbed" in choice:
        if choice == "جائز (Beam)":
            if support == "بسيط": coef, c_def = 1/8, 5/384
            elif support == "كابولي": coef, c_def = 1/2, 1/8
            else: coef, c_def = 1/12, 1/384
        else:
            coef, c_def = 1/8, 5/384
        Mu = wu * (L**2) * coef
        As_req = (abs(Mu) * 10**5) / (0.87 * fy * d)
        Ec = 15000 * np.sqrt(fcu) * 10
        Ig = ( (B/100) * (h_tot/100)**3 ) / 12
        delta = (c_def * wu * L**4 / (Ec * Ig)) * 1000
        delta_max = (L * 1000) / 250
        return Mu, As_req, delta, delta_max
    # الحالة 2: الأساسات
    elif "Footing" in choice:
        Area_f = (wu / 20) * 1.1
        return wu, Area_f, np.sqrt(Area_f), 0
    # الحالة 3: الأعمدة
    elif "Column" in choice:
        area_sq = B * h_tot
        P_cap = (0.35 * fcu * area_sq + 0.67 * fy * (0.01 * area_sq)) / 1000
        return wu, P_cap, area_sq, 0
    return 0, 0, 0, 0

results = compute_design()

# عرض النتائج
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("📑 تقرير النتائج")
    if choice == "جائز (Beam)" or "Solid" in choice or "Ribbed" in choice:
        st.metric("العزم Mu", f"{abs(results[0]):.2f} t.m")
        n_bars = int(np.ceil(results[1] / (np.pi*(phi/10)**2/4)))
        st.success(f"التسليح المقترح: {max(n_bars, 2)} T{phi}")
        st.write(f"**السهم:** {results[2]:.2f} mm / المسموح: {results[3]:.2f} mm")
        if results[2] <= results[3]: st.info("✅ السهم محقق")
        else: st.error("🚨 السهم غير محقق")
    elif "Footing" in choice:
        st.metric("المساحة المطلوبة", f"{results[1]:.2f} m2")
        st.info(f"الأبعاد: {results[2]:.2f} x {results[2]:.2f} m")
    elif "Column" in choice:
        st.metric("تحمل العمود", f"{results[1]:.1f} Ton")

with c2:
    st.subheader("🎨 مخططات هندسية")
    if "Beam" in choice:
        
    elif "Solid" in choice:
        
    elif "Ribbed" in choice:
        
    elif "Footing" in choice:
        
    elif "Column" in choice:
        

st.divider()
st.write(f"📝 المذكرة الحسابية - المهندس بيلان عبدالكريم")
