import streamlit as st
import math
import plotly.graph_objects as go

# إعدادات الصفحة والختم
st.set_page_config(page_title="المصمم الآلي الشامل", layout="wide")
st.sidebar.title("🏗️ نظام التصميم الذكي")
st.sidebar.info("تطوير وتدقيق: 0998449697")

# --- مدخلات المشروع المعمارية ---
st.header("1. المعطيات المعمارية للمبنى")
with st.container():
    col1, col2, col3 = st.columns(3)
    num_floors = col1.number_input("عدد الطوابق", min_value=1, value=1)
    apartments_per_floor = col2.selectbox("عدد الشقق في الطابق", [1, 2, 3, 4])
    rooms_per_apt = col3.number_input("عدد الغرف في الشقة", min_value=1, value=3)

    c4, c5 = st.columns(2)
    room_w = c4.number_input("متوسط عرض الغرفة (m)", value=4.0)
    room_l = c5.number_input("متوسط طول الغرفة (m)", value=5.0)

# --- محرك الحسابات التلقائي (Logic Engine) ---
# حساب عدد الأعمدة والجوائز افتراضياً (بناءً على شبكة الغرف)
total_rooms = apartments_per_floor * rooms_per_apt
num_columns = (total_rooms * 2) + 4  # تقدير أولي لشبكة الأعمدة
total_area = total_rooms * room_w * room_l

# الحمولات من الكود السوري (تلقائياً)
dead_load = 4.5  # kN/m2 (بلاطة + تغطية + قواطع)
live_load = 2.0  # kN/m2 (سكن)
qu = (1.4 * dead_load) + (1.7 * live_load) # الحمل المصعد

# --- عرض النتائج المتسلسلة ---
st.markdown("---")
st.header("2. تحليل نقل الأحمال التلقائي")

# 1. البلاطات
st.subheader("🔹 المرحلة 1: البلاطات")
st.write(f"الحمل التصميمي المعتمد تلقائياً: **{qu:.2f} kN/m²**")

# 2. الجوائز
st.subheader("🔹 المرحلة 2: الجوائز (Beams)")
w_beam = (qu * room_w) / 2 # حمل شبه منحرف مكافئ على الجائز
st.write(f"يتم الآن نقل الأحمال لـ {num_columns * 1.5:.0f} جائزاً برابط مستمر.")
st.info(f"الحمل الوسطي على الجائز الواحد: {w_beam:.2f} kN/m")

# 3. الأعمدة
st.subheader("🔹 المرحلة 3: الأعمدة (Columns)")
# تجميع الحمل التراكمي للطوابق
axial_load_per_floor = w_beam * room_l * 1.2 # تقريبي
total_axial_load = axial_load_per_floor * num_floors
st.write(f"الحمل المحوري الإجمالي على العمود الأوسط بالقاعدة: **{total_axial_load:.2f} kN**")

# 4. الأساسات
st.subheader("🔹 المرحلة 4: الأساسات (Foundations)")
q_allow = 200 # kN/m2
area_f = (total_axial_load * 1.1) / q_allow
side_f = math.sqrt(area_f)
st.success(f"النتيجة: تم تصميم أساس منفصل لكل عمود بأبعاد: {side_f:.2f} x {side_f:.2f} m")

# --- المنظور ثلاثي الأبعاد الشامل ---
st.markdown("---")
if st.button("توليد المخططات والمنظور 3D للمبنى"):
    fig = go.Figure()
    # رسم الطوابق برمجياً
    for f in range(num_floors):
        z_level = f * 3
        # رسم البلاطة لكل طابق
        fig.add_trace(go.Mesh3d(
            x=[0, room_w*2, room_w*2, 0, 0, room_w*2, room_w*2, 0],
            y=[0, 0, room_l*2, room_l*2, 0, 0, room_l*2, room_l*2],
            z=[z_level, z_level, z_level, z_level, z_level+0.2, z_level+0.2, z_level+0.2, z_level+0.2],
            color='blue', opacity=0.3
        ))
    
    fig.update_layout(title=f"منظور مبنى من {num_floors} طوابق")
    st.plotly_chart(fig)

st.markdown(f"--- \n **تم الربط الآلي الشامل وفق الكود السوري | 📞 0998449697**")
