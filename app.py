import streamlit as st
import math
import matplotlib.pyplot as plt

# إعدادات الواجهة
st.set_page_config(page_title="مكتب المهندس بيلان", layout="centered")
st.title("حساب وتسليح البلاطات المصمتة 🏗️")

# --- مدخلات المستخدم ---
with st.sidebar:
    st.header("المعطيات الإنشائية")
    Ly = st.number_input("طول البلاطة Ly (m)", value=27.0)
    Lx = st.number_input("عرض البلاطة Lx (m)", value=2.0)
    main_dia = st.selectbox("قطر الحديد الرئيسي (mm)", [8, 10, 12, 14, 16], index=2)
    live_load = st.number_input("الحمولة الحية (kg/m²)", value=200)

# --- العمليات الحسابية الإنشائية ---
# 1. حساب السماكة التلقائي (Lx/24)
h_cm = math.ceil((Lx * 100) / 24)
if h_cm < 10: h_cm = 10 # الحد الأدنى العملي

# 2. حساب التسليح
# معادلة تقريبية لحساب عدد القضبان بناءً على الأحمال والعزوم
wu = 1.2 * ((h_cm/100)*2500 + 150) + 1.6 * live_load
mu = (wu * (Lx**2)) / 8
as_req = mu / (0.9 * 4000 * 0.9 * (h_cm - 2.5))
bar_area = (math.pi * (main_dia/10)**2) / 4
num_bars = math.ceil(as_req / bar_area)
if num_bars < 5: num_bars = 5

# --- رسم المقطع الإنشائي (Drawing) ---
fig, ax = plt.subplots(figsize=(8, 3))
# رسم حدود البلاطة (الخرسانة)
ax.add_patch(plt.Rectangle((0, 0), 10, h_cm/2, color='lightgrey', alpha=0.5, label='Concrete'))
# رسم الحديد السفلي (خط أحمر)
ax.plot([0.5, 9.5], [1.5, 1.5], color='red', linewidth=3, label='Main Steel')
# رسم الحديد العلوي/التعليق (خط أزرق)
ax.plot([0.5, 3], [h_cm/2 - 1.5, h_cm/2 - 1.5], color='blue', linewidth=2)
ax.plot([7, 9.5], [h_cm/2 - 1.5, h_cm/2 - 1.5], color='blue', linewidth=2, label='Top Steel')

# إضافة النصوص على الرسم
ax.text(5, h_cm/4, f"h = {h_cm} cm", ha='center', fontweight='bold')
ax.text(5, 0.5, f"{num_bars}Φ{main_dia}/m'", ha='center', color='red')

ax.set_xlim(-1, 11)
ax.set_ylim(-2, h_cm/2 + 5)
ax.axis('off')
plt.title(f"تفصيلة تسليح البلاطة (One-Way)")

# --- عرض النتائج في التطبيق ---
st.pyplot(fig)

col1, col2 = st.columns(2)
with col1:
    st.metric("السماكة المحسوبة", f"{h_cm} cm")
    st.metric("التسليح الرئيسي", f"{num_bars} Φ {main_dia} / m'")
with col2:
    st.metric("حجم البيتون", f"{(Lx*Ly*h_cm/100):.2f} m³")
    st.metric("وزن الحديد التقريبي", f"{(num_bars * Lx * (main_dia**2/162) * Ly):.1f} kg")

# --- الختم الرسمي ---
st.markdown("---")
st.info("المهندس المدني بيلان مصطفى عبدالكريم\n\nدراسات - اشراف - تعهدات | 0998449697")
