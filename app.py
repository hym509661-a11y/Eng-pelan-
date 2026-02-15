import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. إعدادات الواجهة
st.set_page_config(page_title="Bilan-Engineering Pro", layout="wide")

st.markdown("""
    <div style="background-color:#002b5c;padding:20px;border-radius:15px;text-align:center;">
        <h1 style="color:white;margin:0;">Bilan-Engineering Pro Suite v11</h1>
        <p style="color:#00d1ff;font-size:20px;">تصميم وإشراف: المهندس بيلان عبدالكريم</p>
    </div>
""", unsafe_allow_html=True)

# 2. القائمة الجانبية للمدخلات
with st.sidebar:
    st.header("⚙️ المدخلات الأساسية")
    choice = st.selectbox("العنصر الإنشائي:", 
        ["جائز (Beam)", "بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)", "أساس منفرد (Isolated Footing)", "عمود (Column)"])
    
    st.divider()
    st.subheader("🧪 خصائص المواد")
    fcu = st.number_input("إجهاد الخرسانة fcu (kg/cm2):", 150, 500, 250)
    fy = st.number_input("إجهاد الحديد fy (kg/cm2):", 2400, 5000, 4000)
    
    st.divider()
    st.subheader("📐 الأبعاد والتحميل")
    L = st.number_input("طول البحر L (m):", 0.5, 20.0, 5.0)
    B = st.number_input("العرض B (cm):", 10.0, 500.0, 30.0)
    h = st.number_input("الارتفاع h (cm):", 10.0, 200.0, 60.0)
    
    support = "بسيط"
    if choice == "جائز (Beam)":
        support = st.selectbox("نوع الاستناد:", ["بسيط", "كابولي", "وثاقة طرفين"])
    
    wu = st.number_input("الحمل Wu (t/m):", 0.1, 1000.0, 2.5)
    phi = st.selectbox("قطر السيخ (mm):", [8, 10, 12, 14, 16, 20, 25])

# 3. المحرك الحسابي (مُعالج ضد أخطاء الإزاحة)
d = h - 5

def run_design():
    # الحسابات الافتراضية
    m_c, v_c, d_c = 0.125, 0.5, 5/384
    if support == "كابولي":
        m_c, v_c, d_c = 0.5, 1.0, 1/8
    elif support == "وثاقة طرفين":
        m_c, v_c, d_c = 1/12, 0.5, 1/384
    
    # النتائج
    Mu = wu * (L**2) * m_c
    Vu = wu * L * v_c
    As = (abs(Mu) * 10**5) / (0.87 * fy * d)
    Ec = 15000 * np.sqrt(fcu) * 10
    Ig = ((B/100) * (h/100)**3) / 12
    delta = (d_c * wu * L**4 / (Ec * Ig)) * 1000
    
    return Mu, Vu, As, delta, (L*1000/250)

res = run_design()

# 4. عرض النتائج والمخططات
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📑 المذكرة الحسابية التفصيلية")
    
    if choice in ["جائز (Beam)", "بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)"]:
        st.write("### أولاً: التحليل الإنشائي (LaTeX)")
        st.latex(r"M_u = \alpha \cdot W_u \cdot L^2 = " + f"{res[0]:.2f} \text{{ t.m}}")
        st.latex(r"V_u = \beta \cdot W_u \cdot L = " + f"{res[1]:.2f} \text{{ t}}")
        
        st.write("### ثانياً: تصميم التسليح الطولي")
        st.latex(r"A_s = \frac{M_u}{0.87 \cdot f_y \cdot d} = " + f"{res[2]:.2f} \text{{ cm}}^2")
        n_bars = int(np.ceil(res[2] / (np.pi*(phi/10)**2/4)))
        st.success(f"النتيجة: استخدام {max(n_bars, 2)} T{phi}")
        
        st.write("### ثالثاً: تدقيق السهم (Deflection)")
        st.latex(r"\delta_{act} = " + f"{res[3]:.2f} \text{{ mm}} \leq \delta_{{all}} = {res[4]:.2f} \text{{ mm}}")
        if res[3] <= res[4]: st.info("✅ السهم محقق وفق الكود")
        else: st.error("🚨 السهم غير محقق! زد السماكة")

    elif choice == "أساس منفرد (Isolated Footing)":
        st.latex(r"A_{footing} = \frac{P \cdot 1.1}{\sigma_{soil}}")
        st.success(f"المساحة المطلوبة: {wu*1.1/2:.2f} m2")

    elif choice == "عمود (Column)":
        cap = (0.35 * fcu * B * h + 0.67 * fy * (0.01 * B * h)) / 1000
        st.latex(r"P_u = 0.35 f_{cu} A_c + 0.67 f_y A_s")
        st.success(f"قدرة التحمل: {cap:.1f} Ton")

with col2:
    st.subheader("📊 مخططات العزم والقص")
    x = np.linspace(0, L, 100)
    # رسم مبسط للمخططات
    if support == "بسيط":
        m_plot = (wu*x/2)*(L-x)
        v_plot = wu*(L/2 - x)
    elif support == "كابولي":
        m_plot = -(wu*(L-x)**2)/2
        v_plot = wu*(L-x)
    else: # وثاقة
        m_plot = (wu*L*x/2) - (wu*x**2/2) - (wu*L**2/12)
        v_plot = wu*(L/2 - x)

    fig, ax = plt.subplots(2, 1, figsize=(6, 6))
    ax[0].plot(x, m_plot, color='r')
    ax[0].set_title("Bending Moment Diagram")
    ax[0].fill_between(x, m_plot, color='r', alpha=0.1)
    ax[1].plot(x, v_plot, color='b')
    ax[1].set_title("Shear Force Diagram")
    ax[1].fill_between(x, v_plot, color='b', alpha=0.1)
    st.pyplot(fig)

st.divider()
st.subheader("🎨 المخطط التوضيحي للتسليح")
if "Beam" in choice:
    elif "Solid" in choice:
    elif "Ribbed" in choice:
    elif "Footing" in choice:
    elif "Column" in choice:
    
st.write("✅ **جميع الحسابات تمت بموجب الكود العربي السوري - م. بيلان عبد الكريم**")
