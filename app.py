import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ترويسة المهندس بيلان
st.set_page_config(page_title="Bilan-Eng Suite", layout="wide")

st.markdown("<h1 style='text-align:center; color:#0047AB;'>Bilan Engineering Pro v15</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>المصمم الإنشائي: م. بيلان عبد الكريم</h3>", unsafe_allow_html=True)

# المدخلات في الجانب
with st.sidebar:
    st.header("📋 معطيات التصميم")
    choice = st.selectbox("العنصر:", ["جائز (Beam)", "بلاطة (Slab)", "أساس (Footing)", "عمود (Column)"])
    L = st.number_input("الطول L (m):", 0.5, 15.0, 5.0)
    h = st.number_input("السماكة h (cm):", 10, 150, 60)
    wu = st.number_input("الحمل Wu (t/m):", 0.1, 50.0, 2.5)
    
    st.divider()
    fcu = st.number_input("fcu (kg/cm2):", 150, 500, 250)
    fy = st.number_input("fy (kg/cm2):", 2400, 5000, 4000)

# الحسابات
d = h - 5
Mu = (wu * L**2) / 8
As = (abs(Mu) * 10**5) / (0.87 * fy * d)

# العرض
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📑 المذكرة الحسابية")
    st.write(f"العنصر المختار: **{choice}**")
    st.latex(r"M_u = \frac{w_u \cdot L^2}{8} = " + f"{Mu:.2f} " + r"\text{ t.m}")
    st.latex(r"A_s = \frac{M_u}{0.87 \cdot f_y \cdot d} = " + f"{As:.2f} " + r"\text{ cm}^2")
    
    # مخطط العزم والقص
    st.write("#### مخططات القوى:")
    x = np.linspace(0, L, 100)
    m_plot = (wu * x / 2) * (L - x)
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.plot(x, m_plot, color='red')
    ax.fill_between(x, m_plot, color='red', alpha=0.1)
    ax.set_title("Bending Moment Diagram")
    st.pyplot(fig)
    

with col2:
    st.subheader("🎨 التفاصيل الإنشائية")
    if "Beam" in choice:
        st.write("**تفريد حديد الجائز:**")
        
    elif "Slab" in choice:
        st.write("**تسليح البلاطة:**")
        
    elif "Footing" in choice:
        st.write("**تسليح القاعدة:**")
        
    else:
        st.write("**تسليح العمود:**")
        

st.divider()
st.caption("✅ تم التصميم وفق الكود العربي السوري - م. بيلان عبد الكريم")
