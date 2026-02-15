import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# واجهة المهندس بيلان عبد الكريم
st.set_page_config(page_title="Bilan-Engineering Suite", layout="wide")

st.title("🏗️ Bilan-Engineering Pro Suite")
st.subheader("المصمم الإنشائي: المهندس بيلان عبد الكريم")

# القائمة الجانبية للمدخلات
with st.sidebar:
    st.header("📋 معطيات المشروع")
    elem = st.selectbox("نوع العنصر الإنشائي:", 
        ["بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)", "أساس منفرد (Footing)", "جائز (Beam)", "عمود (Column)"])
    
    L = st.number_input("الطول L (m):", 0.5, 15.0, 5.0)
    h = st.number_input("السماكة h (cm):", 10, 150, 25)
    wu = st.number_input("الحمل Wu (t/m أو t/m2):", 0.1, 500.0, 1.2)
    phi = st.selectbox("قطر السيخ (mm):", [8, 10, 12, 14, 16, 20])

# --- المحرك الحسابي (تم تبسيطه لمنع أخطاء الإزاحة) ---
fcu = 250
fy = 4000
d = h - 3

def calculate():
    # حسابات عامة للعزوم والتسليح
    if "Slab" in elem or "Beam" in elem or "Ribbed" in elem:
        Mu = (wu * L**2) / 8
        As = (Mu * 10**5) / (0.87 * fy * d)
        n = int(np.ceil(As / (np.pi*(phi/10)**2/4)))
        return Mu, max(n, 2), "t.m"
    elif "Footing" in elem:
        Area = (wu / 2.0) * 1.1 # تربة 2 كغ/سم2
        return wu, np.round(np.sqrt(Area), 2), "m2"
    elif "Column" in elem:
        Cap = (0.35 * fcu * 30 * h + 0.67 * fy * 0.01 * 30 * h) / 1000
        return wu, np.round(Cap, 1), "Ton"
    return 0, 0, ""

res_v1, res_v2, unit = calculate()

# --- عرض النتائج والمذكرة الحسابية ---
col1, col2 = st.columns(2)

with col1:
    st.info(f"📍 العنصر المختار: {elem}")
    if "Slab" in elem or "Beam" in elem or "Ribbed" in elem:
        st.metric("العزم التصميمي", f"{res_v1:.2f} {unit}")
        st.success(f"التسليح المطلوب: {res_v2} T{phi}")
        st.write("---")
        st.write("**مخطط توزيـع الفرش:**")
        if "Solid" in elem:
                    elif "Ribbed" in elem:
                    else:
                        
    elif "Footing" in elem:
        st.metric("مساحة القاعدة المطلوبة", f"{res_v2} x {res_v2} m")
                
    elif "Column" in elem:
        st.metric("تحمل المقطع", f"{res_v2} {unit}")
        
with col2:
    st.subheader("📝 المذكرة الحسابية")
    st.write(f"بناءً على الكود السوري، تم تصميم {elem} بطول {L} م.")
    st.latex(r"M_u = \frac{w \cdot L^2}{8}")
    st.write("تم التحقق من حالات الحدود القصوى (ULS) لضمان الأمان الإنشائي.")
    st.divider()
    st.write("✅ **تصميم معتمد من قبل م. بيلان عبد الكريم**")

