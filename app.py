import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- إعداد واجهة المهندس بيلان عبد الكريم ---
st.set_page_config(page_title="Bilan-Engineering Pro Suite", layout="wide")

st.markdown("""
    <div style="background-color:#002b5c;padding:20px;border-radius:15px;text-align:center;">
        <h1 style="color:white;margin:0;">Bilan-Engineering Ultimate v10.0</h1>
        <p style="color:#00d1ff;font-size:22px;">المصمم الإنشائي المتكامل | المهندس بيلان عبدالكريم</p>
    </div>
""", unsafe_allow_html=True)

# --- القائمة الجانبية: المدخلات والمواد ---
with st.sidebar:
    st.header("📂 اختيار العنصر")
    choice = st.selectbox("العنصر المراد تصميمه:", 
        ["جائز (Beam)", "بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)", "أساس منفرد (Isolated Footing)", "عمود (Column)"])
    
    st.divider()
    st.header("🛠️ خصائص المواد")
    fcu = st.number_input("إجهاد كسر الخرسانة fcu (kg/cm2):", 150, 500, 250)
    fy = st.number_input("إجهاد خضوع الحديد fy (kg/cm2):", 2400, 5000, 4000)
    
    st.divider()
    st.header("📐 الأبعاد والمساند")
    L = st.number_input("طول البحر L (m):", 0.5, 20.0, 5.0)
    B = st.number_input("العرض B (cm):", 10.0, 500.0, 30.0)
    h = st.number_input("الارتفاع الكلي h (cm):", 10.0, 200.0, 60.0)
    
    if choice == "جائز (Beam)":
        support = st.selectbox("نوع الاستناد (Support):", ["بسيط", "كابولي", "وثاقة طرفين"])
    else:
        support = "بسيط"
    
    st.divider()
    wu = st.number_input("الحمل Wu (t/m أو t/m2):", 0.1, 1000.0, 2.5)
    phi = st.selectbox("قطر التسليح (mm):", [8, 10, 12, 14, 16, 20, 25])

# --- المحرك الحسابي ---
d = h - 5 # d effective

def run_design_calculations():
    # حساب العزوم والقص بناء على نوع العنصر والمسند
    m_coef, v_coef, d_coef = 0.125, 0.5, 5/384 # افتراضي للبسيط
    
    if support == "كابولي":
        m_coef, v_coef, d_coef = 0.5, 1.0, 1/8
    elif support == "وثاقة طرفين":
        m_coef, v_coef, d_coef = 1/12, 0.5, 1/384
        
    Mu = wu * (L**2) * m_coef
    Vu = wu * L * v_coef
    As = (abs(Mu) * 10**5) / (0.87 * fy * d)
    
    # السهم
    Ec = 15000 * np.sqrt(fcu) * 10
    Ig = ((B/100) * (h/100)**3) / 12
    delta = (d_coef * wu * L**4 / (Ec * Ig)) * 1000
    delta_max = (L * 1000) / 250
    
    return Mu, Vu, As, delta, delta_max

res = run_design_calculations()

# --- الرسوم التوضيحية (العزم والقص) ---
def plot_diagrams():
    x = np.linspace(0, L, 100)
    if support == "بسيط":
        moment = (wu * x / 2) * (L - x)
        shear = wu * (L/2 - x)
    elif support == "كابولي":
        moment = -(wu * (L - x)**2) / 2
        shear = wu * (L - x)
    else: # وثاقة
        moment = (wu * L * x / 2) - (wu * x**2 / 2) - (wu * L**2 / 12)
        shear = wu * (L/2 - x)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # رسم العزم
    ax1.plot(x, moment, color='red', label='Bending Moment')
    ax1.fill_between(x, moment, color='red', alpha=0.2)
    ax1.set_title("Bending Moment Diagram (B.M.D)")
    ax1.invert_yaxis()
    
    # رسم القص
    ax2.plot(x, shear, color='blue', label='Shear Force')
    ax2.fill_between(x, shear, color='blue', alpha=0.2)
    ax2.set_title("Shear Force Diagram (S.F.D)")
    
    st.pyplot(fig)

# --- عرض النتائج والمذكرة ---
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📑 المذكرة الحسابية التفصيلية")
    
    if choice in ["جائز (Beam)", "بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)"]:
        st.write("#### 1. تحليل القوى:")
        st.latex(r"M_u = \alpha \cdot W_u \cdot L^2 \rightarrow M_u = " + f"{res[0]:.2f} \text{{ t.m}}")
        st.latex(r"V_u = \beta \cdot W_u \cdot L \rightarrow V_u = " + f"{res[1]:.2f} \text{{ t}}")
        
        st.write("#### 2. حساب التسليح الطولي:")
        st.latex(r"A_s = \frac{M_u}{0.87 \cdot f_y \cdot d}")
        bar_area = (np.pi * (phi/10)**2) / 4
        n_bars = int(np.ceil(res[2] / bar_area))
        st.success(f"النتيجة: {max(n_bars, 2)} T{phi}")
        
        st.write("#### 3. التحقق من السهم التشغيلي:")
        st.latex(r"\delta = \frac{k \cdot W \cdot L^4}{E_c \cdot I_g}")
        st.info(f"الفـعلي: {res[3]:.2f} mm | المسموح: {res[4]:.2f} mm")
    
    elif choice == "أساس منفرد (Isolated Footing)":
        st.latex(r"A_{req} = \frac{P \cdot 1.1}{\sigma_{soil}} = " + f"{wu*1.1/2:.2f} \text{{ m}}^2")
    
    plot_diagrams()

with col2:
    st.subheader("🎨 المخططات الإنشائية")
    if choice == "جائز (Beam)":
        
    elif "Slab" in choice:
        
    elif "Footing" in choice:
        
    elif "Column" in choice:
        

st.divider()
st.write(f"✅ **Bilan-Engineering Suite - Verified by Eng. Bilan Abdulkarim**")
