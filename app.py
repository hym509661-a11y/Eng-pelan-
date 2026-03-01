import streamlit as st
import math

# إعدادات الصفحة
st.title("دراسة البلاطات المصمتة 🏗️")
st.subheader("إعداد المهندس: بيلان مصطفى عبدالكريم")

# --- مدخلات المستخدم ---
col1, col2 = st.columns(2)
with col1:
    Ly = st.number_input("طول البلاطة Ly (m)", value=5.0)
    main_dia = st.selectbox("قطر الحديد الرئيسي (mm)", [8, 10, 12, 14, 16], index=2)
with col2:
    Lx = st.number_input("عرض البلاطة Lx (m)", value=2.0)
    live_load = st.number_input("الحمولة الحية (kg/m²)", value=200)

# --- العمليات الحسابية ---
# 1. حساب السماكة h (تلقائياً حسب الكود)
h_cm = math.ceil((Lx * 100) / 24) 
if h_cm < 8: h_cm = 8 # الحد الأدنى للسماكة

# 2. حساب الحمولات
dead_load = (h_cm / 100) * 2500 + 150 # وزن ذاتي + تغطية
wu = 1.2 * dead_load + 1.6 * live_load

# 3. حساب التسليح (تبسيط هندسي للمجال المهني)
mu = (wu * (Lx**2)) / 8
d = h_cm - 2.5
as_req = mu / (0.9 * 4000 * 0.9 * d)
bar_area = (math.pi * (main_dia/10)**2) / 4
num_bars = math.ceil(as_req / bar_area)
if num_bars < 5: num_bars = 5

# 4. حساب الكميات
concrete_vol = Lx * Ly * (h_cm / 100)
weight_per_m = (main_dia**2) / 162
total_steel = num_bars * Lx * weight_per_m * Ly

# --- عرض النتائج ---
st.divider()
st.header("النتائج النهائية")

res_col1, res_col2 = st.columns(2)
with res_col1:
    st.success(f"**سماكة البلاطة:** {h_cm} cm")
    st.success(f"**التسليح السفلي:** {num_bars} Φ {main_dia} / m'")
    st.info(f"**حديد التعليق:** 5 Φ 8 / m'")

with res_col2:
    st.warning(f"**حجم البيتون:** {concrete_vol:.2f} m³")
    st.warning(f"**إجمالي وزن الحديد:** {total_steel:.1f} kg")

# --- الختم الخاص بك ---
st.markdown(f"---")
st.markdown(f"**المهندس المدني بيلان مصطفى عبدالكريم**")
st.markdown(f"**دراسات - اشراف - تعهدات | 0998449697**")
