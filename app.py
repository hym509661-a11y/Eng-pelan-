import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. إعدادات الصفحة والجمالية (Dark Engineering Theme)
st.set_page_config(page_title="Bilan Engineering Suite", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #051937, #004d7a, #008793, #00bf72, #a8eb12);
        color: white;
    }
    .main-card {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #a8eb12;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#a8eb12;'>Bilan Engineering Ultimate v17</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:white;'>إشراف المهندس: بيلان عبد الكريم</h3>", unsafe_allow_html=True)

# 2. القائمة الجانبية للمدخلات
with st.sidebar:
    st.header("📋 مدخلات المشروع")
    type_choice = st.selectbox("العنصر الإنشائي:", ["جائز (Beam)", "بلاطة مصمتة", "بلاطة هوردي"])
    support = st.radio("نوع المساند:", ["بسيط (طرفين)", "وثاقة (طرفين)", "كابولي (طرف واحد)"])
    
    st.divider()
    L = st.number_input("طول البحر L (m):", 0.5, 20.0, 5.0)
    h = st.number_input("السماكة h (cm):", 10, 150, 60)
    B = st.number_input("العرض B (cm):", 10, 500, 30)
    wu = st.number_input("الحمل Wu (t/m):", 0.1, 50.0, 2.5)
    
    st.divider()
    phi = st.selectbox("قطر السيخ (mm):", [8, 10, 12, 14, 16, 20, 25])
    fcu = st.number_input("fcu (kg/cm2):", 150, 500, 250)
    fy = st.number_input("fy (kg/cm2):", 2400, 5000, 4000)

# 3. المحرك الحسابي
d = h - 5
# تحديد المعاملات بناء على المساند
if "بسيط" in support:
    m_c, v_c = 0.125, 0.5
elif "وثاقة" in support:
    m_c, v_c = 1/12, 0.5
else:
    m_c, v_c = 0.5, 1.0

Mu = wu * (L**2) * m_c
Vu = wu * L * v_c
As = (abs(Mu) * 10**5) / (0.87 * fy * d)

# حساب عدد القضبان
area_bar = (np.pi * (phi/10)**2) / 4
n_bars = int(np.ceil(As / area_bar))

# 4. عرض النتائج والمخططات
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader("📑 المذكرة الحسابية التفصيلية")
    st.latex(r"M_u = \alpha \cdot w_u \cdot L^2 = " + f"{Mu:.2f} " + r"\text{ t.m}")
    st.latex(r"V_u = \beta \cdot w_u \cdot L = " + f"{Vu:.2f} " + r"\text{ t}")
    st.latex(r"A_s = \frac{M_u}{0.87 \cdot f_y \cdot d} = " + f"{As:.2f} " + r"\text{ cm}^2")
    st.success(f"النتيجة: استخدام {max(n_bars, 2)} قضبان T{phi}")
    
    # رسم مخططات العزم والقص
    x = np.linspace(0, L, 100)
    if "بسيط" in support:
        m_p = (wu*x/2)*(L-x); v_p = wu*(L/2 - x)
    elif "وثاقة" in support:
        m_p = (wu*L*x/2)-(wu*x**2/2)-(wu*L**2/12); v_p = wu*(L/2 - x)
    else:
        m_p = -(wu*(L-x)**2)/2; v_p = wu*(L-x)

    fig, ax = plt.subplots(2, 1, figsize=(6, 4))
    plt.subplots_adjust(hspace=0.6)
    ax[0].plot(x, m_p, color='red', lw=2); ax[0].fill_between(x, m_p, color='red', alpha=0.2); ax[0].set_title("Moment (M)")
    ax[1].plot(x, v_p, color='lime', lw=2); ax[1].fill_between(x, v_p, color='lime', alpha=0.2); ax[1].set_title("Shear (V)")
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.subheader("📍 وضعية المساند")
    if "بسيط" in support:
        
    elif "وثاقة" in support:
        
    else:
        

    st.divider()
    st.subheader("🎨 مخطط التسليح التوضيحي")
    if "جائز" in type_choice:
        
    elif "مصمتة" in type_choice:
        
    else:
        

st.divider()
st.write("✅ **Bilan Engineering Suite - المصمم الإنشائي المهندس بيلان عبد الكريم**")
