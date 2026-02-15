import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. إعدادات الصفحة والجمالية
st.set_page_config(page_title="Bilan-Eng Pro Suite", layout="wide")

# تصميم الخلفية والترويسة
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stApp {
        background: linear-gradient(135deg, #001f3f 0%, #0074D9 100%);
        color: white;
    }
    .result-card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #00d1ff;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style="text-align:center; padding:10px;">
        <h1 style="color:#00d1ff; margin-bottom:0;">Bilan Engineering Pro Suite 2026</h1>
        <p style="font-size:20px; color:white;">المكتب الهندسي المتطور | المهندس بيلان عبدالكريم</p>
    </div>
    """, unsafe_allow_html=True)

# 2. القائمة الجانبية: المدخلات
with st.sidebar:
    st.header("📐 المدخلات الهندسية")
    choice = st.selectbox("العنصر الإنشائي:", ["جائز (Beam)", "بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)"])
    
    st.divider()
    L = st.number_input("طول البحر L (m):", 1.0, 20.0, 5.0)
    h = st.number_input("السماكة h (cm):", 10, 150, 60)
    B = st.number_input("العرض B (cm):", 10, 500, 30)
    wu = st.number_input("الحمل Wu (t/m):", 0.1, 100.0, 2.5)
    
    st.divider()
    st.subheader("🧪 المواد والمساند")
    fcu = st.number_input("fcu (kg/cm2):", 150, 500, 250)
    fy = st.number_input("fy (kg/cm2):", 2400, 5000, 4000)
    phi = st.select_slider("اختر قطر السيخ (mm):", options=[8, 10, 12, 14, 16, 18, 20, 25], value=14)
    support_type = st.radio("نوع المساند:", ["بسيط (طرفين)", "وثاقة (طرفين)", "كابولي"])

# 3. المحرك الحسابي
d = h - 5
# معاملات التصميم بناء على المساند
if support_type == "بسيط (طرفين)":
    m_c, v_c, k_d = 0.125, 0.5, 5/384
elif support_type == "وثاقة (طرفين)":
    m_c, v_c, k_d = 1/12, 0.5, 1/384
else: # كابولي
    m_c, v_c, k_d = 0.5, 1.0, 1/8

Mu = wu * (L**2) * m_c
Vu = wu * L * v_c
As_req = (abs(Mu) * 10**5) / (0.87 * fy * d)

# حساب عدد القضبان
area_single_bar = (np.pi * (phi/10)**2) / 4
num_bars = int(np.ceil(As_req / area_single_bar))
if num_bars < 2: num_bars = 2

# 4. عرض النتائج والمخططات
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.subheader("📑 المذكرة الحسابية التفصيلية")
    
    st.write("### أولاً: تحليل القوى (LaTeX)")
    st.latex(r"M_u = \alpha \cdot w_u \cdot L^2 = " + f"{Mu:.2f} " + r"\text{ t.m}")
    st.latex(r"V_u = \beta \cdot w_u \cdot L = " + f"{Vu:.2f} " + r"\text{ t}")
    
    st.write("### ثانياً: تصميم التسليح والفرش")
    st.latex(r"A_s = \frac{M_u}{0.87 \cdot f_y \cdot d} = " + f"{As_req:.2f} " + r"\text{ cm}^2")
    st.info(f"النتيجة: استخدام {num_bars} قضبان بقطر {phi} مم (أي {num_bars} T{phi})")
    
    # رسم مخططات العزم والقص
    st.write("### ثالثاً: مخططات القوى القصوى")
    x = np.linspace(0, L, 100)
    if support_type == "بسيط (طرفين)":
        m_plot = (wu*x/2)*(L-x); v_plot = wu*(L/2 - x)
    elif support_type == "وثاقة (طرفين)":
        m_plot = (wu*L*x/2) - (wu*x**2/2) - (wu*L**2/12); v_plot = wu*(L/2 - x)
    else:
        m_plot = -(wu*(L-x)**2)/2; v_plot = wu*(L-x)

    fig, ax = plt.subplots(2, 1, figsize=(6, 5))
    plt.subplots_adjust(hspace=0.5)
    ax[0].plot(x, m_plot, color='red', lw=2)
    ax[0].fill_between(x, m_plot, color='red', alpha=0.2)
    ax[0].set_title("Bending Moment Diagram (B.M.D)")
    
    ax[1].plot(x, v_plot, color='cyan', lw=2)
    ax[1].fill_between(x, v_plot, color='cyan', alpha=0.2)
    ax[1].set_title("Shear Force Diagram (S.F.D)")
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.subheader("🎨 مخطط توضيح الحديد")
    if "Beam" in choice:
        
        st.write(f"**توزيع حديد الجائز:** {num_bars} T{phi}")
    elif "Solid" in choice:
        
        st.write(f"**تسليح البلاطة (الفرش):** {num_bars} T{phi} للمتر الطولي")
    else:
        
        st.write(f"**تسليح العصب:** {num_bars} T{phi}")

    st.divider()
    st.subheader("📍 وضعية المساند")
    if support_type == "بسيط (طرفين)":
        
    elif support_type == "وثاقة (طرفين)":
        
    else:
        

st.divider()
st.write(f"✅ **Bilan Engineering Suite - تم التدقيق والمراجعة من قبل المهندس بيلان عبد الكريم**")
