import streamlit as st
import math
import matplotlib.pyplot as plt

# إعدادات الواجهة والختم المهني (Personalized with your info)
st.set_page_config(page_title="مكتب المهندس بيلان", layout="wide")
st.title("البرنامج الذكي لتسليح البلاطات والكميات 🏗️")

# --- مدخلات المهندس ---
with st.sidebar:
    st.header("إدخال المعطيات")
    Ly = st.number_input("طول البلاطة Ly (m)", value=27.0)
    Lx = st.number_input("عرض البلاطة Lx (m)", value=2.0)
    h_input = st.number_input("سماكة البلاطة المدخلة h (cm)", value=12)
    mesh_type = st.radio("نظام التسليح:", ("شبكة واحدة + برانيط", "شبكتين كاملتين"))
    live_load = st.number_input("الحمولة الحية (kg/m²)", value=200)

# --- الحسابات الإنشائية التلقائية ---
# 1. حساب الأحمال (Wu)
dead_load = (h_input/100) * 2500 + 150 
wu = 1.2 * dead_load + 1.6 * live_load
mu = (wu * (Lx**2)) / 8
d = h_input - 2.5 

# 2. حساب مساحة الحديد واختيار القطر (تلقائياً)
as_req = mu / (0.9 * 4000 * 0.9 * d) 
available_diameters = [8, 10, 12, 14, 16]
chosen_dia = 10
chosen_num = 5

for dia in available_diameters:
    area_one_bar = (math.pi * (dia/10)**2) / 4
    num = math.ceil(as_req / area_one_bar)
    if 5 <= num <= 10:
        chosen_dia = dia
        chosen_num = num
        break

# 3. منطق حساب الأوزان بناءً على نوع الشبكة
weight_per_m = (chosen_dia**2 / 162)
dist_weight = (8**2 / 162) * 5 # وزن حديد التوزيع (5T8)

if mesh_type == "شبكة واحدة + برانيط":
    # سفلي كامل + علوي جزئي (برانيط 25% من البحر) + توزيع سفلي
    total_weight_per_m2 = (chosen_num * weight_per_m) + (chosen_num * weight_per_m * 0.5) + dist_weight
    top_label = f"برانيط: {chosen_num} Φ {chosen_dia} / m'"
    multiplier = 1.05 # زيادة 5% فضلات
else:
    # سفلي كامل + علوي كامل + توزيع سفلي + توزيع علوي + كراسي
    total_weight_per_m2 = (chosen_num * weight_per_m * 2) + (dist_weight * 2)
    top_label = f"شبكة علوية: {chosen_num} Φ {chosen_dia} / m'"
    multiplier = 1.15 # زيادة 15% (كراسي + فضلات + تربيط)

total_steel_kg = total_weight_per_m2 * Lx * Ly * multiplier

# --- الرسم الإنشائي ---
fig, ax = plt.subplots(figsize=(10, 4))
ax.add_patch(plt.Rectangle((0, 0), 10, h_input/2, color='lightgrey', alpha=0.3))
# السفلي
ax.plot([0.2, 9.8], [1, 1], color='red', linewidth=3, label='Main Bottom')

if mesh_type == "شبكة واحدة + برانيط":
    ax.plot([0.2, 2.5], [h_input/2 - 1, h_input/2 - 1], color='blue', linewidth=2.5)
    ax.plot([7.5, 9.8], [h_input/2 - 1, h_input/2 - 1], color='blue', linewidth=2.5, label='Top Bars')
else:
    ax.plot([0.2, 9.8], [h_input/2 - 1, h_input/2 - 1], color='blue', linewidth=2.5, label='Full Top Mesh')

ax.set_ylim(-1, h_input/2 + 2)
ax.axis('off')
st.pyplot(fig)

# --- عرض النتائج النهائية والختم ---
st.subheader("النتائج النهائية للكميات:")
col1, col2, col3 = st.columns(3)
col1.metric("الحديد السفلي (حسابي)", f"{chosen_num} Φ {chosen_dia}")
col2.metric("الحديد العلوي", top_label)
col3.metric("حديد التوزيع", "5 Φ 8")

st.divider()
res1, res2 = st.columns(2)
res1.success(f"📦 حجم الخرسانة: {(Lx * Ly * h_input/100):.2f} m³")
res2.error(f"⚖️ إجمالي وزن الحديد (+الزيادة): {total_steel_kg:.1f} kg")

st.markdown(f"<br><hr><center><b>المهندس المدني بيلان مصطفى عبدالكريم</b><br>دراسات - اشراف - تعهدات<br><b>0998449697</b></center>", unsafe_allow_html=True)
