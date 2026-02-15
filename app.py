import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- واجهة المهندس بيلان عبد الكريم ---
st.set_page_config(page_title="Bilan-Engineering Pro", layout="wide")

st.markdown("""
    <div style="background-color:#002b5c;padding:20px;border-radius:15px;text-align:center;">
        <h1 style="color:white;margin:0;">Bilan-Engineering Suite v11.0</h1>
        <p style="color:#00d1ff;font-size:22px;">تصميم وإشراف: المهندس بيلان عبدالكريم</p>
    </div>
""", unsafe_allow_html=True)

# --- القائمة الجانبية للمدخلات ---
with st.sidebar:
    st.header("⚙️ المدخلات الهندسية")
    choice = st.selectbox("العنصر المطلوب:", ["جائز (Beam)", "بلاطة مصمتة", "بلاطة هوردي", "أساس منفرد", "عمود"])
    
    st.divider()
    fcu = st.number_input("إجهاد الخرسانة fcu (kg/cm2):", 150, 500, 250)
    fy = st.number_input("إجهاد الحديد fy (kg/cm2):", 2400, 5000, 4000)
    
    st.divider()
    L = st.number_input("الطول L (m):", 0.5, 20.0, 5.0)
    B = st.number_input("العرض B (cm):", 10.0, 500.0, 30.0)
    h = st.number_input("السماكة h (cm):", 10.0, 200.0, 60.0)
    
    support = "بسيط"
    if "Beam" in choice:
        support = st.selectbox("نوع المساند:", ["بسيط", "كابولي", "وثاقة"])
    
    wu = st.number_input("الحمل Wu (t/m):", 0.1, 100.0, 2.5)
    phi = st.selectbox("قطر التسليح (mm):", [8, 10, 12, 14, 16, 20, 25])

# --- محرك الحسابات والمخططات ---
d = h - 5
m_c, v_c, d_c = 0.125, 0.5, 5/384
if support == "كابولي": m_c, v_c, d_c = 0.5, 1.0, 1/8
elif support == "وثاقة": m_c, v_c, d_c = 1/12, 0.5, 1/384

Mu = wu * (L**2) * m_c
Vu = wu * L * v_c
As = (abs(Mu) * 10**5) / (0.87 * fy * d)
Ec = 15000 * np.sqrt(fcu) * 10
Ig = (B * h**3) / (12 * 10**8)
delta = (d_c * wu * L**4 / (Ec * Ig)) * 1000 if Ig > 0 else 0

# --- عرض النتائج والمذكرة الحسابية ---
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📑 المذكرة الحسابية التفصيلية")
    st.latex(r"M_u = \alpha \cdot W_u \cdot L^2 = " + f"{Mu:.2f} \text{{ t.m}}")
    st.latex(r"V_u = \beta \cdot W_u \cdot L = " + f"{Vu:.2f} \text{{ t}}")
    st.latex(r"A_s = \frac{M_u}{0.87 \cdot f_y \cdot d} = " + f"{As:.2f} \text{{ cm}}^2")
    
    bar_area = (np.pi * (phi/10)**2) / 4
    n_bars = int(np.ceil(As/bar_area))
    st.success(f"النتيجة النهائية: {max(n_bars, 2)} T{phi}")
    
    st.write("### تدقيق السهم (Deflection):")
    st.latex(r"\delta_{act} = " + f"{delta:.2f} \text{{ mm}} \leq \delta_{{all}} = {(L*1000/250):.2f} \text{{ mm}}")

with col2:
    st.subheader("📊 مخططات القوى (B.M.D & S.F.D)")
    # رسم المخططات
    x_plot = np.linspace(0, L, 100)
    if support == "بسيط": m_plot = (wu*x_plot/2)*(L-x_plot); v_plot = wu*(L/2 - x_plot)
    elif support == "كابولي": m_plot = -(wu*(L-x_plot)**2)/2; v_plot = wu*(L-x_plot)
    else: m_plot = (wu*L*x_plot/2) - (wu*x_plot**2/2) - (wu*L**2/12); v_plot = wu*(L/2 - x_plot)
    
    fig, ax = plt.subplots(2, 1, figsize=(5, 5))
    ax[0].plot(x_plot, m_plot, 'r'); ax[0].fill_between(x_plot, m_plot, color='r', alpha=0.1); ax[0].set_title("Moment")
    ax[1].plot(x_plot, v_plot, 'b'); ax[1].fill_between(x_plot, v_plot, color='b', alpha=0.1); ax[1].set_title("Shear")
    st.pyplot(fig)

st.divider()
st.subheader("🎨 المخطط الإنشائي")
if "Beam" in choice:
    elif "مصمتة" in choice:
    elif "هوردي" in choice:
    elif "أساس" in choice:
    elif "عمود" in choice:
    
st.caption("إعداد المهندس بيلان عبد الكريم - 2026")
