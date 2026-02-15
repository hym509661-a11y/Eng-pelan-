import streamlit as st
import numpy as np

# 1. التنسيق الجمالي (الخلفية الملكية)
st.set_page_config(page_title="Bilan Engineering Pro", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #051937, #004d7a, #008793, #00bf72, #a8eb12);
        color: white;
    }
    .main-card {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #a8eb12;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#a8eb12;'>Bilan Engineering Ultimate v18</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>إشراف المهندس: بيلان عبد الكريم</h3>", unsafe_allow_html=True)

# 2. القائمة الجانبية
with st.sidebar:
    st.header("📋 المدخلات")
    type_choice = st.selectbox("العنصر:", ["جائز (Beam)", "بلاطة مصمتة", "بلاطة هوردي"])
    support = st.radio("نوع المساند:", ["بسيط (طرفين)", "وثاقة (طرفين)", "كابولي"])
    
    st.divider()
    L = st.number_input("الطول L (m):", 1.0, 20.0, 5.0)
    h = st.number_input("السماكة h (cm):", 10, 150, 60)
    B = st.number_input("العرض B (cm):", 10, 500, 30)
    wu = st.number_input("الحمل Wu (t/m):", 0.1, 50.0, 2.5)
    
    st.divider()
    phi = st.selectbox("القطر (mm):", [12, 14, 16, 20, 25])
    fcu = st.number_input("fcu:", 150, 500, 250)
    fy = st.number_input("fy:", 2400, 5000, 4000)

# 3. الحسابات الهندسية
d = h - 5
m_c = 0.125 if "بسيط" in support else 0.0833 if "وثاقة" in support else 0.5
v_c = 0.5 if "بسيط" in support or "وثاقة" in support else 1.0

Mu = wu * (L**2) * m_c
Vu = wu * L * v_c
As = (abs(Mu) * 10**5) / (0.87 * fy * d)
n_bars = int(np.ceil(As / (3.1415 * (phi/10)**2 / 4)))

# 4. عرض النتائج (بدون مكتبات خارجية معقدة لضمان التشغيل)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader("📑 المذكرة الحسابية")
    st.latex(r"M_u = \alpha \cdot w_u \cdot L^2 = " + f"{Mu:.2f} " + r"\text{ t.m}")
    st.latex(r"V_u = \beta \cdot w_u \cdot L = " + f"{Vu:.2f} " + r"\text{ t}")
    st.latex(r"A_s = \frac{M_u}{0.87 \cdot f_y \cdot d} = " + f"{As:.2f} " + r"\text{ cm}^2")
    st.success(f"النتيجة: استخدام {max(n_bars, 2)} T{phi}")
    
    # عرض المخططات كصور ثابتة (أكثر أماناً للتشغيل)
    st.write("### مخططات القوى (النظرية):")
    if "بسيط" in support:
        
    elif "وثاقة" in support:
        
    else:
        
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.subheader("📍 تفاصيل المساند")
    if "بسيط" in support:
        
    elif "وثاقة" in support:
        
