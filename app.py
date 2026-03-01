import streamlit as st
import math
import matplotlib.pyplot as plt

# إعدادات الواجهة والختم المهني
st.set_page_config(page_title="مكتب المهندس بيلان", layout="wide")
st.title("البرنامج الذكي لتسليح البلاطات المصمتة 🏗️")

# --- مدخلات المهندس ---
with st.sidebar:
    st.header("إدخال المعطيات")
    Ly = st.number_input("طول البلاطة Ly (m)", value=27.0)
    Lx = st.number_input("عرض البلاطة Lx (m)", value=2.0)
    h_input = st.number_input("سماكة البلاطة المدخلة h (cm)", value=12)
    # خيار شبكة أو شبكتين
    mesh_type = st.radio("نظام التسليح:", ("شبكة واحدة", "شبكتين كاملتين"))
    live_load = st.number_input("الحمولة الحية (kg/m²)", value=200)

# --- الحسابات الإنشائية (حساب القطر والعدد تلقائياً) ---
# 1. حساب الأحمال Wu والعزم Mu
dead_load = (h_input/100) * 2500 + 150 
wu = 1.2 * dead_load + 1.6 * live_load
mu = (wu * (Lx**2)) / 8
d = h_input - 2.5 

# 2. حساب مساحة الحديد المطلوبة As (cm²/m)
as_req = mu / (0.9 * 4000 * 0.9 * d) 

# 3. اختيار القطر والعدد حسابياً (تلقائي)
# البرنامج يجرب الأقطار بدءاً من 8 مم حتى يجد العدد المناسب بين 5 و 10 قضبان في المتر
available_diameters = [8, 10, 12, 14, 16]
chosen_dia = 10 # افتراضي
chosen_num = 5  # افتراضي

for dia in available_diameters:
    area_one_bar = (math.pi * (dia/10)**2) / 4
    num = math.ceil(as_req / area_one_bar)
    if 5 <= num <= 10:
        chosen_dia = dia
        chosen_num = num
        break
    elif num > 10 and dia == 16: # إذا كان العدد كبيراً جداً حتى مع قطر 16
        chosen_dia = 16
        chosen_num = num

# --- تجهيز بيانات الرسم بناءً على نوع الشبكة ---
fig, ax = plt.subplots(figsize=(10, 4))
ax.add_patch(plt.Rectangle((0, 0), 10, h_input/2, color='lightgrey', alpha=0.3))

# الحديد السفلي ثابت في الحالتين
ax.plot([0.2, 9.8], [1, 1], color='red', linewidth=3, label='Main Bottom')

if mesh_type == "شبكة واحدة":
    # رسم برانيط علوية فقط
    ax.plot([0.2, 2.5], [h_input/2 - 1, h_input/2 - 1], color='blue', linewidth=2.5)
    ax.plot([7.5, 9.8], [h_input/2 - 1, h_input/2 - 1], color='blue', linewidth=2.5, label='Top Bars (Branteet)')
    num_top = chosen_num
    label_top = "علوي (برانيط)"
else:
    # رسم شبكة علوية كاملة
    ax.plot([0.2, 9.8], [h_input/2 - 1, h_input/2 - 1], color='blue', linewidth=2.5, label='Full Top Mesh')
    num_top = chosen_num 
    label_top = "شبكة علوية كاملة"

# إضافة النصوص
ax.text(5, h_input/4, f"h = {h_input} cm", ha='center', weight='bold')
ax.text(5, 0.2, f"السفلي الحسابي: {chosen_num}Φ{chosen_dia}/m'", ha='center', color='red')
ax.axis('off')
st.pyplot(fig)

# --- عرض النتائج والكميات ---
st.subheader("التقرير الفني الناتج:")
c1, c2, c3 = st.columns(3)
with c1:
    st.success(f"**الحديد السفلي:**\n\n {chosen_num} Φ {chosen_dia} / m'")
with c2:
    st.info(f"**{label_top}:**\n\n {num_top} Φ {chosen_dia} / m'")
with c3:
    st.warning(f"**حديد التوزيع:**\n\n 5 Φ 8 / m'")

# حساب الأوزان الإجمالية
total_bars_per_m = chosen_num + num_top + 5 # سفلي + علوي + توزيع
weight_total = total_bars_per_m * Lx * (chosen_dia**2/162) * Ly

st.divider()
col_a, col_b = st.columns(2)
col_a.metric("حجم البيتون الكلي", f"{(Lx*Ly*h_input/100):.2f} m³")
col_b.metric("إجمالي وزن الحديد", f"{weight_total:.1f} kg")

# --- الختم المهني ببياناتك المحفوظة ---
st.markdown("<br><hr><center><b>المهندس المدني بيلان مصطفى عبدالكريم</b><br>دراسات - اشراف - تعهدات<br><b>0998449697</b></center>", unsafe_allow_html=True)
