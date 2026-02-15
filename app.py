import streamlit as st
import numpy as np

# --- ترويسة المهندس بيلان ---
st.set_page_config(page_title="Bilan-Engineering Suite", layout="wide")
st.markdown("""
    <div style="background-color:#002b5c;padding:20px;border-radius:15px;text-align:center;">
        <h1 style="color:white;margin:0;">Bilan-Engineering Ultimate Pro</h1>
        <p style="color:#00d1ff;font-size:20px;">المصمم الإنشائي: المهندس بيلان عبدالكريم</p>
    </div>
""", unsafe_allow_html=True)

# --- القائمة الجانبية: المدخلات ---
with st.sidebar:
    st.header("📂 اختيار العنصر")
    choice = st.selectbox("العنصر المراد تصميمه:", 
        ["جائز (Beam)", "بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)", "أساس منفرد (Isolated Footing)", "عمود (Column)"])
    
    st.divider()
    L = st.number_input("طول البحر L (m):", 0.5, 20.0, 5.0)
    B = st.number_input("العرض B (cm):", 10.0, 500.0, 30.0)
    h = st.number_input("الارتفاع/السماكة h (cm):", 10.0, 200.0, 60.0)
    
    if choice == "جائز (Beam)":
        support = st.selectbox("نوع الاستناد (Support):", ["بسيط", "كابولي", "وثاقة من الطرفين"])
    
    st.divider()
    wu = st.number_input("الحمل Wu (t/m أو t/m2):", 0.1, 1000.0, 2.5)
    phi = st.selectbox("قطر التسليح (mm):", [8, 10, 12, 14, 16, 20, 25])

# --- المحرك الحسابي المطور (وفق الكود السوري) ---
fcu = 250
fy = 4000
d = h - 5  # الغطاء الخرساني

def run_engine():
    # 1. حالة الجوائز والبلاطات
    if choice in ["جائز (Beam)", "بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)"]:
        # تحديد معاملات العزم والسهم بناءً على الاستناد
        m_coef = 0.125 # 1/8 للبسيط والبلاطات
        d_coef = 5/384
        
        if choice == "جائز (Beam)":
            if support == "كابولي": 
                m_coef, d_coef = 0.5, 0.125
            elif support == "وثاقة من الطرفين": 
                m_coef, d_coef = 1/12, 1/384
        
        # حساب العزم والتسليح
        Mu = wu * (L**2) * m_coef
        As = (abs(Mu) * 10**5) / (0.87 * fy * d)
        
        # حساب السهم (Deflection)
        Ec = 15000 * np.sqrt(fcu) * 10
        Ig = ((B/100) * (h/100)**3) / 12
        delta = (d_coef * wu * L**4 / (Ec * Ig)) * 1000
        delta_max = (L * 1000) / 250
        
        return Mu, As, delta, delta_max

    # 2. حالة الأساسات
    if choice == "أساس منفرد (Isolated Footing)":
        Area_req = (wu / 2.0) * 1.1 # تربة 2 كغ/سم2
        side = np.sqrt(Area_req)
        return wu, Area_req, side, 0

    # 3. حالة الأعمدة
    if choice == "عمود (Column)":
        area_col = B * h
        capacity = (0.35 * fcu * area_col + 0.67 * fy * (0.01 * area_col)) / 1000
        return wu, capacity, area_col, 0

res = run_engine()

# --- عرض النتائج والمذكرة الحسابية ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📑 نتائج الحساب")
    if choice in ["جائز (Beam)", "بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)"]:
        st.metric("العزم التصميمي Mu", f"{res[0]:.2f} t.m")
        bar_area = (np.pi * (phi/10)**2) / 4
        n_bars = int(np.ceil(res[1] / bar_area))
        st.success(f"عدد الأسياخ المقترح: {max(n_bars, 2)} T{phi}")
        
        st.divider()
        st.write(f"**تدقيق السهم:** {res[2]:.2f} mm")
        st.write(f"**المسموح (L/250):** {res[3]:.2f} mm")
        if res[2] <= res[3]: st.info("✅ السهم محقق")
        else: st.error("🚨 السهم غير محقق! زد السماكة h")

    elif "Footing" in choice:
        st.metric("المساحة المطلوبة", f"{res[1]:.2f} m2")
        st.success(f"الأبعاد: {res[2]:.2f} x {res[2]:.2f} m")

    elif "Column" in choice:
        st.metric("قدرة تحمل العمود", f"{res[1]:.1f} Ton")
        if res[2] < 900: st.error("🚨 مساحة المقطع أقل من 900 سم2")

with col2:
    st.subheader("🎨 مخطط التسليح والفرش")
    if choice == "جائز (Beam)":
        
    elif choice == "بلاطة مصمتة (Solid Slab)":
        
    elif choice == "بلاطة هوردي (Ribbed Slab)":
        
    elif "Footing" in choice:
        
    elif "Column" in choice:
        

st.divider()
st.write(f"📝 **المذكرة الحسابية - المهندس بيلان عبد الكريم**")
st.caption("تم التصميم وفق معايير الكود العربي السوري لعام 2026")
