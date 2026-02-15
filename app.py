import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- واجهة المهندس بيلان عبد الكريم ---
st.set_page_config(page_title="Bilan-Engineering Pro Suite", layout="wide")

st.markdown("""
    <div style="background-color:#002b5c;padding:20px;border-radius:15px;text-align:center;">
        <h1 style="color:white;margin:0;">Bilan-Engineering Pro Suite v5.0</h1>
        <p style="color:#00d1ff;font-size:22px;">المصمم الإنشائي الشامل | المهندس بيلان عبدالكريم</p>
    </div>
""", unsafe_allow_html=True)

# --- قائمة المدخلات ---
with st.sidebar:
    st.header("📂 اختيار العنصر")
    cat = st.selectbox("العنصر الإنشائي:", 
        ["جائز (Beam)", "بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)", "أساس منفرد (Isolated Footing)", "عمود (Column)"])
    
    st.divider()
    st.header("📐 الأبعاد والمساند")
    L = st.number_input("الطول L (m):", 0.5, 20.0, 5.0)
    B = st.number_input("العرض B (m):", 0.1, 10.0, 0.3)
    h_total = st.number_input("الارتفاع h (cm):", 10, 200, 60)
    
    if cat == "جائز (Beam)":
        sup = st.selectbox("نوع المساند:", ["بسيط", "كابولي", "وثاقة من الطرفين"])
    
    st.divider()
    wu = st.number_input("الحمل Wu (t/m أو t/m2):", 0.1, 1000.0, 2.0)
    phi = st.selectbox("قطر السيخ (mm):", [8, 10, 12, 14, 16, 18, 20, 25])

# --- المحرك الحسابي الموحد (تم ضبط الإزاحات بدقة) ---
def structural_engine():
    fcu = 250
    fy = 4000
    d = h_total - 5
    
    if cat == "جائز (Beam)" or "Slab" in cat:
        # حسابات العزوم والسهم
        if cat == "جائز (Beam)":
            if sup == "بسيط": coeff, c_def = 1/8, 5/384
            elif sup == "كابولي": coeff, c_def = 1/2, 1/8
            else: coeff, c_def = 1/12, 1/384
        else:
            coeff, c_def = 1/8, 5/384 # للبلاطات
            
        Mu = wu * (L**2) * coeff
        As = (abs(Mu) * 10**5) / (0.87 * fy * d)
        
        # حساب السهم الفعلي
        Ec = 15000 * np.sqrt(fcu) * 10
        Ig = (B * (h_total/100)**3) / 12
        delta = (c_def * wu * L**4 / (Ec * Ig)) * 1000
        delta_max = (L * 1000) / 250
        return Mu, As, delta, delta_max

    elif "Footing" in cat:
        # حسابات القواعد
        Area = (wu / 20) * 1.1 # تحمل تربة افتراضي 2 كغ/سم2
        return wu, Area, np.sqrt(Area), 0

    elif "Column" in cat:
        # حسابات الأعمدة
        area_cm2 = (B * 100) * h_total
        P_cap = (0.35 * fcu * area_cm2 + 0.67 * fy * (0.01 * area_cm2)) / 1000
        return wu, P_cap, area_cm2, 0

res = structural_engine()

# --- عرض النتائج والمخططات ---
c1, c2 = st.columns([1, 1.2])

with c1:
    st.subheader("📋 تقرير التصميم")
    if cat == "جائز (Beam)" or "Slab" in cat:
        st.metric("العزم Mu", f"{abs(res[0]):.2f} t.m")
        n = int(np.ceil(res[1] / (np.pi*(phi/10)**2/4)))
        st.success(f"التسليح: {max(n, 2)} T{phi}")
        st.divider()
        st.write(f"**السهم:** {res[2]:.2f} mm / المسموح: {res[3]:.2f} mm")
        if res[2] <= res[3]: st.info("✅ السهم محقق")
        else: st.error("🚨 السهم غير محقق! زد السماكة")

    elif "Footing" in cat:
        st.metric("المساحة المطلوبة", f"{res[1]:.2f} m2")
        st.success(f"الأبعاد: {res[2]:.2f} x {res[2]:.2f} m")

    elif "Column" in cat:
        st.metric("تحمل العمود", f"{res[1]:.1f} Ton")
        if res[2] < 900: st.error("🚨 مساحة العمود < 900 سم2 (مخالف)")

with c2:
    st.subheader("🎨 المخطط الإنشائي")
    if "Slab" in cat:
            elif "Footing" in cat:
            elif "Beam" in cat:
            elif "Column" in cat:
            elif "Ribbed" in cat:
        
st.divider()
st.write(f"### 📝 المذكرة الحسابية - م. بيلان عبدالكريم")
st.write(f"تم التدقيق الإنشائي لعنصر **{cat}** وفق الكود السوري المطور. النتائج تشمل التحقق من حالات الحدود القصوى (العزوم) والتشغيلية (السهم).")
