import streamlit as st
import numpy as np

# إعداد واجهة المهندس بيلان عبد الكريم
st.set_page_config(page_title="Bilan Ultimate Design", layout="wide")

st.markdown("<h1 style='text-align: center; color: #0047AB;'>Bilan Engineering Ultimate v8.0</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>تصميم وإعداد: المهندس بيلان عبد الكريم</h3>", unsafe_allow_html=True)

# قائمة المدخلات في الجانب
with st.sidebar:
    st.header("⚙️ معطيات العنصر")
    choice = st.selectbox("اختر العنصر الإنشائي:", 
        ["جائز (Beam)", "بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)", "أساس (Footing)", "عمود (Column)"])
    
    L = st.number_input("الطول L (m):", 0.5, 15.0, 5.0)
    h = st.number_input("الارتفاع h (cm):", 10, 150, 60)
    wu = st.number_input("الحمل Wu (t/m):", 0.1, 10.0, 2.5)
    phi = st.selectbox("قطر التسليح (mm):", [12, 14, 16, 20])

# --- محرك الحسابات (تم تبسيطه لمنع أخطاء المسافات) ---
fcu = 250
fy = 4000
d = h - 5

def start_design():
    # حالة الجوائز والبلاطات
    if "Beam" in choice or "Slab" in choice:
        # حساب العزم (تبسيط للاستناد البسيط)
        Mu = (wu * L**2) / 8
        As = (Mu * 10**5) / (0.87 * fy * d)
        bar_area = (np.pi * (phi/10)**2) / 4
        n_bars = int(np.ceil(As / bar_area))
        
        # حساب السهم للجوائز فقط
        delta = 0
        if "Beam" in choice:
            Ec = 15000 * np.sqrt(fcu) * 10
            Ig = (30 * h**3) / 12 / 10**8
            delta = ( (5/384) * wu * L**4 / (Ec * Ig) ) * 1000
            
        return Mu, max(n_bars, 2), delta

    # حالة الأساسات
    if "Footing" in choice:
        Area = (wu / 2.0) * 1.1
        return wu, np.sqrt(Area), 0

    # حالة الأعمدة
    if "Column" in choice:
        Capacity = (0.35 * fcu * 30 * h + 0.67 * fy * 0.01 * 30 * h) / 1000
        return wu, Capacity, 0
    
    return 0, 0, 0

# استدعاء النتائج
res1, res2, res3 = start_design()

# --- عرض النتائج والمخططات ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("📋 نتائج التدقيق")
    if "Beam" in choice or "Slab" in choice:
        st.metric("العزم Mu", f"{res1:.2f} t.m")
        st.success(f"التسليح المقترح: {res2} T{phi}")
        if "Beam" in choice:
            st.write(f"**السهم الفعلي:** {res3:.2f} mm")
            st.write(f"**السهم المسموح (L/250):** {(L*1000/250):.2f} mm")
    elif "Footing" in choice:
        st.metric("مساحة القاعدة", f"{res1:.2f} m2")
        st.info(f"الأبعاد: {res2:.2f} x {res2:.2f} m")
    elif "Column" in choice:
        st.metric("قدرة التحمل", f"{res2:.1f} Ton")

with c2:
    st.subheader("🎨 مخطط التسليح")
    if "Beam" in choice:
            elif "Solid" in choice:
            elif "Ribbed" in choice:
            elif "Footing" in choice:
            elif "Column" in choice:
        
st.divider()
st.write(f"📝 **مذكرة حسابية مصممة بواسطة م. بيلان عبد الكريم وفق الكود السوري**")
