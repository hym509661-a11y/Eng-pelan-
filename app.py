import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

# إعدادات الصفحة
st.set_page_config(page_title="المصمم الإنشائي الشامل", layout="wide")

# القائمة الجانبية لإعدادات المواد العامة
with st.sidebar:
    st.title("⚙️ الإعدادات العامة")
    fcu = st.number_input("إجهاد البيتون fcu (MPa)", value=25)
    fy = st.number_input("إجهاد الحديد fy (MPa)", value=400)
    st.divider()
    st.info("تمت البرمجة وفق متطلبات الكود العربي السوري")

# القائمة الرئيسية للاختيار بين العناصر
choice = st.selectbox("🏗️ اختر العنصر المراد تصميمه:", ["بلاطات مصمتة (Slabs)", "أعمدة محورية (Columns)"])

# ---------------------------------------------------------
# القسم الأول: البلاطات
# ---------------------------------------------------------
if choice == "بلاطات مصمتة (Slabs)":
    st.header("📊 تصميم البلاطات ورسم المخططات")
    
    col1, col2 = st.columns(2)
    with col1:
        L = st.number_input("المجاز الصافي L (m)", value=4.0)
        t_cm = st.number_input("سماكة البلاطة h (cm)", value=12)
        condition = st.selectbox("حالة الاستناد", ["بسيطة", "مستمرة من طرف", "مستمرة من طرفين", "ظفر (كابول)"])
    with col2:
        finishing = st.number_input("التغطية (kg/m²)", value=150)
        walls = st.number_input("القواطع (kg/m²)", value=100)
        live_load = st.number_input("الحمولة الحية (kg/m²)", value=200)
        bar_dia_slab = st.selectbox("قطر حديد البلاطة (mm)", [8, 10, 12, 14])

    if st.button("تحليل البلاطة"):
        # حساب السهم
        factors = {"بسيطة": 20, "مستمرة من طرف": 24, "مستمرة من طرفين": 28, "ظفر (كابول)": 10}
        min_t = (L * 100) / (factors[condition] * (1.0 if fy == 400 else (0.4 + fy/700)))
        
        # الأحمال والعزوم
        wu = 1.4 * ((t_cm/100 * 2.5) + (finishing/1000) + (walls/1000)) + 1.7 * (live_load/1000)
        Mu = (wu * L**2) / 8
        
        # التسليح
        d = (t_cm - 2.5) * 10
        Rn = (Mu * 10**7) / (1000 * d**2)
        m = fy / (0.85 * fcu)
        rho = (1/m) * (1 - math.sqrt(1 - (2 * m * Rn / fy))) if (1 - (2 * m * Rn / fy)) > 0 else 0.0018
        As_req = max(rho * 1000 * d, 0.0018 * 1000 * t_cm * 10) / 100
        num_bars = math.ceil(As_req / (math.pi * bar_dia_slab**2 / 400))
        num_bars = max(num_bars, 5)

        # الرسم
        x = np.linspace(0, L, 100)
        m_diag = (wu * x / 2) * (L - x)
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.fill_between(x, m_diag, color='skyblue', alpha=0.5)
        ax.invert_yaxis()
        ax.set_title("Bending Moment Diagram")
        st.pyplot(fig)

        if t_cm < min_t: st.error(f"⚠️ السهم غير محقق! المطلوب: {min_t:.1f} سم")
        else: st.success("✅ السماكة كافية للسهم")
        st.info(f"🔨 التسليح: {num_bars} T{bar_dia_slab} لكل متر طولي")

# ---------------------------------------------------------
# القسم الثاني: الأعمدة
# ---------------------------------------------------------
elif choice == "أعمدة محورية (Columns)":
    st.header("🏢 تصميم الأعمدة المحورية القصيرة")
    
    col_a, col_b = st.columns(2)
    with col_a:
        P_ton = st.number_input("الحمل المحوري التشغيلي (Ton)", value=100.0)
        b_cm = st.number_input("عرض العمود b (cm)", value=30)
        h_cm = st.number_input("طول العمود h (cm)", value=50)
    with col_b:
        bar_dia_col = st.selectbox("قطر حديد التسليح (mm)", [14, 16, 18, 20, 25])
        
    if st.button("تصميم العمود"):
        Pu = 1.5 * P_ton * 10000 # تحويل لنيوتن (تقريبي للتبسيط)
        Ag = b_cm * h_cm * 100 # ملم2
        
        # حساب الحديد المطلوب
        As_req = (Pu - 0.40 * fcu * Ag) / (0.67 * fy - 0.40 * fcu)
        As_min = 0.008 * Ag
        As_final = max(As_req, As_min)
        
        num_bars = math.ceil(As_final / (math.pi * bar_dia_col**2 / 4))
        if num_bars % 2 != 0: num_bars += 1 # تقريب لعدد زوجي
        
        st.subheader("✅ نتائج تصميم العمود")
        st.metric("مساحة الحديد المطلوبة", f"{As_final/100:.2f} cm²")
        st.success(f"🔨 التسليح المقترح: {num_bars} قضبان قطر {bar_dia_col} mm")
        
        # رسم مقطع العمود
        fig2, ax2 = plt.subplots(figsize=(4, 4))
        ax2.add_patch(plt.Rectangle((0, 0), b_cm, h_cm, color='lightgray'))
        ax2.set_title(f"Column Cross Section {b_cm}x{h_cm}")
        st.pyplot(fig2)
