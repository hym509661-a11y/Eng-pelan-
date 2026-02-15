import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- إعدادات واجهة المهندس بيلان ---
st.set_page_config(page_title="Bilan-Engineering Suite", layout="wide")

st.markdown("""
    <div style="background-color:#002b5c;padding:20px;border-radius:15px;text-align:center;">
        <h1 style="color:white;margin:0;">Bilan-Engineering Pro v3.0</h1>
        <p style="color:#00d1ff;font-size:20px;">تصميم وتدقيق: المهندس بيلان عبدالكريم</p>
    </div>
""", unsafe_allow_html=True)

# --- المدخلات في القائمة الجانبية ---
with st.sidebar:
    st.header("⚙️ معطيات التحليل")
    support_type = st.selectbox("حالة الاستناد:", 
        ["بسيط (ثابت-متدحرج)", "وثاقة طرف واحد (كابولي)", "وثاقة من الطرفين"])
    
    L = st.number_input("طول البحر L (m):", 1.0, 15.0, 5.0)
    wu = st.number_input("الحمل الموزع Wu (t/m):", 0.1, 10.0, 2.0)
    
    st.divider()
    st.header("📏 المقطع الخرساني")
    b = st.number_input("العرض b (cm):", 20, 100, 30)
    h = st.number_input("الارتفاع h (cm):", 20, 150, 60)
    fcu = st.number_input("fcu (kg/cm2):", 200, 400, 250)
    
    st.divider()
    phi = st.selectbox("قطر التسليح (mm):", [12, 14, 16, 18, 20])

# --- المحرك الإنشائي والحسابات ---
def solve_all():
    # 1. حساب العزم والمؤشرات
    if support_type == "بسيط (ثابت-متدحرج)":
        M_max = (wu * L**2) / 8
        coef_def = 5/384
    elif support_type == "وثاقة طرف واحد (كابولي)":
        M_max = (wu * L**2) / 2
        coef_def = 1/8
    else: # وثاقة طرفين
        M_max = (wu * L**2) / 12
        coef_def = 1/384

    # 2. حساب التسليح
    d = h - 5
    As_req = (abs(M_max) * 10**5) / (0.87 * 4000 * d)
    bar_area = (np.pi * (phi/10)**2) / 4
    n_bars = int(np.ceil(As_req / bar_area))
    
    # 3. حساب السهم (Deflection)
    # E_c = 4700 * sqrt(fcu) -> تقريباً للتبسيط
    Ec = 15000 * np.sqrt(fcu) * 10 # t/m2
    I_gross = (b/100 * (h/100)**3) / 12 # m4
    delta = (coef_def * wu * L**4) / (Ec * I_gross) * 1000 # mm
    
    # حد السهم المسموح (L/250 وفق الكود السوري)
    delta_allow = (L * 1000) / 250
    
    return M_max, As_req, n_bars, delta, delta_allow

M_max, As, bars, delta, d_allow = solve_all()

# --- عرض النتائج ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 التحليل الهندسي والمخططات")
    x = np.linspace(0, L, 100)
    # رسم مبسط للجائز
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
    
    # رسم الجائز والمساند
    ax1.add_patch(patches.Rectangle((0, 0.4), L, 0.2, color='#cccccc'))
    if "وثاقة" in support_type:
        ax1.plot([0, 0], [0.2, 0.8], color='black', lw=5)
    ax1.set_title("Structural System")
    ax1.axis('off')

    # رسم السهم (الانحناء)
    y_def = -4 * (delta/10) * (x/L) * (1 - x/L) # تمثيل شكلي
    ax2.plot(x, y_def, color='blue', ls='--', label='Deflection Shape')
    ax2.set_title("Deflection Visualization")
    ax2.legend()
    st.pyplot(fig)

with col2:
    st.subheader("📑 تقرير التدقيق الإنشائي")
    st.metric("العزم M_u", f"{abs(M_max):.2f} t.m")
    st.metric("التسليح", f"{max(bars, 2)} T{phi}")
    
    st.divider()
    st.write("### ✅ تدقيق السهم (Deflection Check)")
    st.write(f"- السهم الفعلي: **{delta:.2f} mm**")
    st.write(f"- السهم المسموح (L/250): **{d_allow:.2f} mm**")
    
    if delta <= d_allow:
        st.success("الارتحام (السهم) محقق ضمن حدود الكود السوري.")
    else:
        st.error("🚨 السهم غير محقق! يرجى زيادة سماكة الجائز (h).")

st.divider()
st.subheader("📝 المذكرة الحسابية النهائية")
st.write(f"**المهندس المصمم:** بيلان عبدالكريم")
st.write(f"**العنصر:** جائز {support_type} بطول {L} متر.")
st.write("تم حساب العزم والتسليح والتحقق من الصلابة (EI) لضمان عدم حدوث تشققات في اللياسة أو العناصر غير الإنشائية.")
