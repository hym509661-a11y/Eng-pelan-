import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

# إعداد واجهة التطبيق
st.set_page_config(page_title="المصمم الإنشائي الشامل", layout="wide")
st.title("🏗️ المصمم الإنشائي: تحليل، رسم، وتفريد حديد")

# القائمة الجانبية
with st.sidebar:
    st.header("📋 إعدادات المواد")
    fcu = st.number_input("إجهاد البيتون fcu (MPa)", value=25)
    fy = st.number_input("إجهاد الحديد fy (MPa)", value=400)
    st.divider()
    st.header("⚖️ أحمال البلاطة (kg/m²)")
    finishing = st.number_input("وزن التغطية", value=150)
    walls = st.number_input("وزن القواطع", value=100)
    live_load = st.selectbox("الحمولة الحية", [200, 300, 500])
    st.divider()
    bar_dia = st.selectbox("قطر قضيب التسليح (mm)", [8, 10, 12, 14, 16])

# المدخلات الأساسية
col1, col2 = st.columns(2)
with col1:
    L = st.number_input("المجاز الصافي L (m)", value=4.0, step=0.1)
    t_cm = st.number_input("سماكة البلاطة h (cm)", value=12)
with col2:
    condition = st.selectbox("حالة الاستناد", ["بسيطة", "مستمرة من طرف", "مستمرة من طرفين", "ظفر (كابول)"])

if st.button("تحليل ورسم وتفريد الحديد"):
    # 1. التحقق من السهم
    factors = {"بسيطة": 20, "مستمرة من طرف": 24, "مستمرة من طرفين": 28, "ظفر (كابول)": 10}
    alpha = 1.0 if fy == 400 else (0.4 + fy/700)
    min_t = (L * 100) / (factors[condition] * alpha)
    
    # 2. الحسابات الإنشائية
    dead_load = (t_cm/100 * 2.5) + (finishing/1000) + (walls/1000)
    wu = 1.4 * dead_load + 1.7 * (live_load/1000)
    Mu_max = (wu * L**2) / 8
    Vu_max = (wu * L) / 2

    # 3. حساب التسليح وعدد القضبان
    d = (t_cm - 2.5) * 10 
    Rn = (Mu_max * 10**7) / (1000 * d**2)
    m = fy / (0.85 * fcu)
    rho = (1/m) * (1 - math.sqrt(1 - (2 * m * Rn / fy))) if (1 - (2 * m * Rn / fy)) > 0 else 0.0018
    As_req = max(rho * 1000 * d, 0.0018 * 1000 * t_cm * 10) / 100 
    
    area_single_bar = (math.pi * bar_dia**2) / 400 # cm2
    num_bars = math.ceil(As_req / area_single_bar)
    if num_bars < 5: num_bars = 5 # الحد الأدنى في المتر حسب الكود
    spacing = 100 / num_bars

    # 4. رسم المخططات
    x = np.linspace(0, L, 100)
    moment = (wu * x / 2) * (L - x)
    shear = wu * (L/2 - x)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
    plt.subplots_adjust(hspace=0.6)

    ax1.fill_between(x, moment, color='skyblue', alpha=0.4)
    ax1.plot(x, moment, color='blue', linewidth=2)
    ax1.set_title(f"Bending Moment Diagram (Mu = {Mu_max:.2f} t.m)")
    ax1.invert_yaxis()

    ax2.fill_between(x, shear, color='salmon', alpha=0.4)
    ax2.plot(x, shear, color='red', linewidth=2)
    ax2.set_title(f"Shear Force Diagram (Vu = {Vu_max:.2f} t)")
    ax2.axhline(0, color='black', linewidth=1)
    
    st.pyplot(fig)

    # 5. عرض النتائج النهائية
    st.divider()
    if t_cm < min_t:
        st.error(f"⚠️ السهم غير محقق! الحد الأدنى للسماكة: {min_t:.1f} سم")
    else:
        st.success(f"✅ السماكة محققة للسهم (الحد الأدنى: {min_t:.1f} سم)")

    c1, c2, c3 = st.columns(3)
    c1.metric("التسليح المطلوب", f"{As_req:.2f} cm²/m")
    c2.metric("عدد القضبان", f"{num_bars} قضبان/م")
    c3.metric("المسافة (S)", f"{spacing:.1f} سم")

    st.warning(f"💡 النتيجة النهائية: استخدم **{num_bars} T{bar_dia}** لكل متر طولي (فرش).")
