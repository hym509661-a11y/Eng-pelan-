import streamlit as st
import math
import matplotlib.pyplot as plt

# إعدادات الواجهة والختم المهني
st.set_page_config(page_title="مكتب المهندس بيلان", layout="wide")
st.title("برنامج حساب تسليح البلاطات المصمتة (One-Way) 🏗️")

# --- مدخلات المهندس ---
with st.sidebar:
    st.header("إدخال المعطيات")
    Ly = st.number_input("طول البلاطة Ly (m)", value=27.0)
    Lx = st.number_input("عرض البلاطة Lx (m)", value=2.0)
    h_input = st.number_input("سماكة البلاطة المدخلة h (cm)", value=12)
    main_dia = st.selectbox("قطر الحديد الرئيسي (mm)", [8, 10, 12, 14, 16], index=2)
    live_load = st.number_input("الحمولة الحية (kg/m²)", value=200)

# --- الحسابات الإنشائية التلقائية ---
# 1. حساب الأحمال Wu
dead_load = (h_input/100) * 2500 + 150 # وزن ذاتي + تغطية
wu = 1.2 * dead_load + 1.6 * live_load

# 2. حساب العزم والتسليح السفلي
mu = (wu * (Lx**2)) / 8
d = h_input - 2.5 # الارتفاع الفعال
as_req = mu / (0.9 * 4000 * 0.9 * d) # مساحة الحديد المطلوبة cm2/m
bar_area = (math.pi * (main_dia/10)**2) / 4
num_bars_bot = math.ceil(as_req / bar_area)
if num_bars_bot < 5: num_bars_bot = 5

# 3. حساب التسليح العلوي والتعليق (حسب الكود)
num_bars_top = math.ceil(num_bars_bot * 0.75) # تقديراً للعزم السالب
if num_bars_top < 5: num_bars_top = 5
num_dist_bars = 5 # حديد توزيع/تعليق ثابت 5 في المتر

# --- رسم المقطع الإنشائي ---
fig, ax = plt.subplots(figsize=(10, 4))
# رسم البلاطة
ax.add_patch(plt.Rectangle((0, 0), 10, h_input/2, color='lightgrey', alpha=0.3))
# رسم الحديد السفلي (أحمر)
ax.plot([0.2, 9.8], [1, 1], color='red', linewidth=3, label='Bottom Steel')
# رسم الحديد العلوي (أزرق)
ax.plot([0.2, 2.5], [h_input/2 - 1, h_input/2 - 1], color='blue', linewidth=2.5)
ax.plot([7.5, 9.8], [h_input/2 - 1, h_input/2 - 1], color='blue', linewidth=2.5, label='Top Steel')
# رسم حديد التعليق (أخضر)
ax.plot([2.5, 7.5], [h_input/2 - 1.5, h_input/2 - 1.5], color='green', linestyle='--', label='Distribution')

# نصوص توضيحية على الرسم
ax.text(5, h_input/4, f"h = {h_input} cm", ha='center', weight='bold')
ax.text(5, 0.2, f"السفلي: {num_bars_bot}Φ{main_dia}/m'", ha='center', color='red')
ax.text(1.2, h_input/2 + 0.5, f"العلوي: {num_bars_top}Φ{main_dia}/m'", ha='center', color='blue')

ax.set_xlim(-0.5, 10.5)
ax.set_ylim(-2, h_input/2 + 3)
ax.axis('off')
st.pyplot(fig)

# --- عرض الكميات والنتائج ---
col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"**الحديد السفلي:**\n\n {num_bars_bot} Φ {main_dia} لكل متر")
with col2:
    st.info(f"**الحديد العلوي:**\n\n {num_bars_top} Φ {main_dia} لكل متر")
with col3:
    st.info(f"**حديد التعليق:**\n\n {num_dist_bars} Φ 8 لكل متر")

st.divider()
c1, c2 = st.columns(2)
c1.warning(f"📦 **حجم البيتون الكلي:** {(Lx * Ly * h_input/100):.2f} m³")
c2.warning(f"⚖️ **وزن الحديد التقريبي:** {((num_bars_bot + num_bars_top) * Lx * (main_dia**2/162) * Ly):.1f} kg")

# --- الختم المهني المعتمد ---
st.markdown("<br><center><b>المهندس المدني بيلان مصطفى عبدالكريم</b></center>", unsafe_allow_html=True)
st.markdown("<center>دراسات - اشراف - تعهدات | 0998449697</center>", unsafe_allow_html=True)
