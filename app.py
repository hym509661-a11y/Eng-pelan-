import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

# إعداد واجهة التطبيق
st.set_page_config(page_title="المصمم الإنشائي الشامل", layout="wide")
st.title("🏗️ المصمم الإنشائي: تحليل ورسم مخططات")

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

# المدخلات الأساسية
col1, col2 = st.columns(2)
with col1:
    L = st.number_input("المجاز الصافي L (m)", value=4.0, step=0.1)
    t_cm = st.number_input("سماكة البلاطة h (cm)", value=12)
with col2:
    condition = st.selectbox("حالة الاستناد", ["بسيطة", "مستمرة من طرف", "مستمرة من طرفين"])

if st.button("تحليل ورسم المخططات"):
    # 1. الحسابات الهندسية
    dead_load = (t_cm/100 * 2.5) + (finishing/1000) + (walls/1000)
    wu = 1.4 * dead_load + 1.7 * (live_load/1000)
    Mu_max = (wu * L**2) / 8
    Vu_max = (wu * L) / 2

    # 2. إنشاء بيانات المخططات
    x = np.linspace(0, L, 100)
    moment = (wu * x / 2) * (L - x)  # معادلة العزم لبلاطة بسيطة
    shear = wu * (L/2 - x)          # معادلة القص

    # 3. رسم المخططات باستخدام Matplotlib
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
    plt.subplots_adjust(hspace=0.5)

    # مخطط العزم (Moment Diagram)
    ax1.fill_between(x, moment, color='skyblue', alpha=0.4)
    ax1.plot(x, moment, color='blue', linewidth=2)
    ax1.set_title(f"Bending Moment Diagram (Max Mu = {Mu_max:.2f} t.m)")
    ax1.set_ylabel("Moment (t.m)")
    ax1.invert_yaxis()  # قلب المحور ليكون العزم لأسفل كما هو معتاد إنشائياً

    # مخطط القص (Shear Diagram)
    ax2.fill_between(x, shear, color='salmon', alpha=0.4)
    ax2.plot(x, shear, color='red', linewidth=2)
    ax2.set_title(f"Shear Force Diagram (Max Vu = {Vu_max:.2f} t)")
    ax2.set_ylabel("Shear (t)")
    ax2.axhline(0, color='black', linewidth=1)

    # عرض المخططات في Streamlit
    st.pyplot(fig)

    # 4. عرض النتائج الرقمية
    st.divider()
    res_c1, res_c2 = st.columns(2)
    res_c1.success(f"أقصى عزم تصميمي: {Mu_max:.2f} t.m")
    res_c2.warning(f"أقصى قوة قص: {Vu_max:.2f} t")
