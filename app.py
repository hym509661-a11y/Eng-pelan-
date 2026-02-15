import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# إعدادات واجهة المهندس بيلان
st.set_page_config(page_title="Bilan-Eng Pro", layout="wide")

# تصميم خلفية هندسية احترافية
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #010c1e 0%, #0047ab 100%);
        color: white;
    }
    .main-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #00d1ff;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#00d1ff;'>Bilan Engineering Pro v16</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>المصمم الإنشائي: م. بيلان عبد الكريم</h3>", unsafe_allow_html=True)

# القائمة الجانبية للمدخلات
with st.sidebar:
    st.header("📐 معطيات التصميم")
    choice = st.selectbox("العنصر:", ["جائز (Beam)", "بلاطة مصمتة", "بلاطة هوردي"])
    support = st.radio("نوع المساند:", ["بسيط (طرفين)", "وثاقة (طرفين)", "كابولي"])
    
    st.divider()
    L = st.number_input("الطول L (m):", 0.5, 20.0, 5.0)
    h = st.number_input("السماكة h (cm):", 10, 150, 60)
    B = st.number_input("العرض B (cm):", 10, 500, 30)
    wu = st.number_input("الحمل Wu (t/m):", 0.1, 50.0, 2.5)
    
    st.divider()
    fcu = st.number_input("fcu (kg/cm2):", 150, 500, 250)
    fy = st.number_input("fy (kg/cm2):", 2400, 5000, 4000)
    phi = st.select_slider("قطر السيخ (mm):", options=[8, 10, 12, 14, 16, 20, 25], value=14)

# المحرك الحسابي
d = h - 5
m_c, v_c = (0.125, 0.5) if "بسيط" in support else (1/12, 0.5) if "وثاقة" in support else (0.5, 1.0)

Mu = wu * (L**2) * m_c
Vu = wu * L * v_c
As = (abs(Mu) * 10**5) / (0.87 * fy * d)
n_bars = int(np.ceil(As / (np.pi*(phi/10)**2/4)))

# العرض والنتائج
col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    st.subheader("📑 المذكرة الحسابية التفصيلية")
    st.latex(r"M_u = \alpha \cdot w_u \cdot L^2 = " + f"{Mu:.2f} " + r"\text{ t.m}")
    st.latex(r"V_u = \beta \cdot w_u \cdot L = " + f"{Vu:.2f} " + r"\text{ t}")
    st.latex(r"A_s = \frac{M_u}{0.87 \cdot f_y \cdot d} = " + f"{As:.2f} " + r"\text{ cm}^2")
    st.success(f"القرار: استخدام {max(n_bars, 2)} T{phi}")
    
    # رسم المخططات
    x = np.linspace(0, L, 100)
    m_p = (wu*x/2)*(L-x) if "بسيط" in support else (wu*L*x/2)-(wu*x**2/2)-(wu*L**2/12) if "وثاقة" in support else -(wu*(L-x)**2)/2
    v_p = wu*(L/2 - x) if "بسيط" in support or "وثاقة" in support else wu*(L-x)

    fig, ax = plt.subplots(2, 1, figsize=(6, 4))
    plt.subplots_adjust(hspace=0.6)
    ax[0].plot(x, m_p, color='red'); ax[0].fill_between(x, m_p, color='red', alpha=0.1); ax[0].set_title("Bending Moment (M)")
    ax[1].plot(x, v_p, color='cyan'); ax[1].fill_between(x, v_p, color='cyan', alpha=0.1); ax[1].set_title("Shear Force (V)")
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.subheader("🎨 المخططات التوضيحية")
    if "Beam" in choice:
        
    elif "مصمتة" in choice:
        
    else:
        
    
    st.divider()
    st.subheader("📍 وضعية المساند")
    if "بسيط" in support:
        
    elif "وثاقة" in support:
        
    else:
        

st.divider()
st.write("✅ **Bilan Engineering Suite - م. بيلان عبد الكريم**")
