import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# إعدادات الواجهة
st.set_page_config(page_title="Bilan Engineering Pro", layout="wide")
st.markdown("<h1 style='text-align: center; color: #0047AB;'>Bilan Engineering Pro</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>المهندس بيلان عبد الكريم</h3>", unsafe_allow_html=True)

# قائمة المدخلات
with st.sidebar:
    st.header("⚙️ المدخلات")
    choice = st.selectbox("العنصر الإنشائي:", ["جائز (Beam)", "بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)", "أساس (Footing)", "عمود (Column)"])
    L = st.number_input("الطول L (m):", 1.0, 15.0, 5.0)
    h = st.number_input("الارتفاع/السماكة h (cm):", 10, 150, 60)
    wu = st.number_input("الحمل Wu (t/m):", 0.1, 10.0, 2.0)
    phi = st.selectbox("قطر السيخ (mm):", [12, 14, 16, 20])
    
    # اختيار المساند فقط في حال كان العنصر جائزاً
    support_type = "بسيط"
    if choice == "جائز (Beam)":
        support_type = st.radio("نوع المساند:", ["بسيط", "كابولي", "وثاقة طرفين"])

# المحرك الحسابي (مُعالج ضد أخطاء الإزاحة)
def run_design():
    fcu, fy = 250, 4000
    d = h - 5
    # حساب العزوم بناء على النوع
    if choice == "جائز (Beam)":
        if support_type == "بسيط": m_coef, d_coef = 1/8, 5/384
        elif support_type == "كابولي": m_coef, d_coef = 1/2, 1/8
        else: m_coef, d_coef = 1/12, 1/384
        
        Mu = wu * (L**2) * m_coef
        As = (Mu * 10**5) / (0.87 * fy * d)
        # حساب السهم
        Ec = 15000 * np.sqrt(fcu) * 10
        Ig = (30 * h**3) / 12 / 10**8 # m4
        delta = (d_coef * wu * L**4 / (Ec * Ig)) * 1000
        return Mu, As, delta, (L*1000/250)

    if "Slab" in choice:
        Mu = (wu * L**2) / 8
        As = (Mu * 10**5) / (0.87 * fy * d)
        return Mu, As, 0, 0

    if choice == "أساس (Footing)":
        Area = (wu / 2.0) * 1.1 # تربة 2 كغ/سم2
        return wu, Area, np.sqrt(Area), 0

    if choice == "عمود (Column)":
        Cap = (0.35 * fcu * 30 * h + 0.67 * fy * 0.01 * 30 * h) / 1000
        return wu, Cap, 0, 0
    
    return 0, 0, 0, 0

# استخراج النتائج
res1, res2, res3, res4 = run_design()

# العرض المنسق
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 نتائج التصميم")
    if choice in ["جائز (Beam)", "بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)"]:
        st.metric("العزم الأعظمي", f"{res1:.2f} t.m")
        bar_area = (np.pi * (phi/10)**2) / 4
        n_bars = int(np.ceil(res2 / bar_area))
        st.success(f"التسليح: {max(n_bars, 2)} T{phi}")
        if res3 > 0:
            st.write(f"**السهم الفعلي:** {res3:.2f} mm")
            st.write(f"**السهم المسموح:** {res4:.2f} mm")
            if res3 <= res4: st.info("✅ السهم محقق")
            else: st.error("🚨 السهم غير محقق")
    elif choice == "أساس (Footing)":
        st.metric("المساحة المطلوبة", f"{res2:.2f} m2")
        st.write(f"الأبعاد المقترحة: {res3:.2f} x {res3:.2f} m")
    elif choice == "عمود (Column)":
        st.metric("قدرة تحمل العمود", f"{res2:.1f} Ton")

with col2:
    st.subheader("🖼️ تفاصيل التسليح")
    if "Beam" in choice:
            elif "Solid" in choice:
            elif "Footing" in choice:
            elif "Column" in choice:
            elif "Ribbed" in choice:
        
st.divider()
st.write(f"**مذكرة حسابية معتمدة - المهندس بيلان عبد الكريم - 2026**")
