import streamlit as st
import math
import matplotlib.pyplot as plt
import pandas as pd

# --- إعدادات الهوية البصرية ---
st.set_page_config(page_title="مكتب المهندس بيلان - نظام التصميم الإنشائي", layout="wide")

# تصميم ترويسة احترافية
st.markdown(f"""
    <div style="background-color:#1E1E1E;padding:20px;border-radius:10px;border-left: 8px solid #FF4B4B;">
        <h1 style="color:white;margin:0;">نظام تصميم وحساب كميات البلاطات المصمتة</h1>
        <p style="color:#DDDDDD;">إعداد المهندس المدني: <b>بيلان مصطفى عبدالكريم</b> | دراسات - إشراف - تعهدات</p>
    </div>
    """, unsafe_allow_html=True)

# --- مدخلات المشروع ---
with st.sidebar:
    st.header("📋 معطيات المشروع")
    project_name = st.text_input("اسم المشروع", "فيلا سكنية")
    Ly = st.number_input("الطول الكلي Ly (m)", value=27.0, step=0.5)
    Lx = st.number_input("العرض الصافي Lx (m)", value=2.0, step=0.1)
    h_cm = st.number_input("السماكة المختارة h (cm)", value=12)
    
    st.divider()
    st.header("🏗️ خيارات التسليح")
    mesh_type = st.radio("نظام التسليح المطلوبة:", ("شبكة واحدة + برانيط", "شبكتين كاملتين"))
    f_y = st.number_input("إجهاد خضوع الحديد (kg/cm²)", value=4000)
    live_load = st.number_input("الحمولة الحية (kg/m²)", value=200)

# --- المحرك الحسابي (Structural Engine) ---
# 1. تحليل الأحمال
sw = (h_input / 100) * 2500 if 'h_input' in locals() else (h_cm/100)*2500
wu = 1.2 * (sw + 150) + 1.6 * live_load
mu = (wu * (Lx**2)) / 8
d = h_cm - 2.5

# 2. اختيار القطر والعدد تلقائياً
as_req = mu / (0.9 * f_y * 0.9 * d)
diameters = [8, 10, 12, 14, 16]
chosen_dia, chosen_num = 10, 5
for dia in diameters:
    area = (math.pi * (dia/10)**2) / 4
    num = math.ceil(as_req / area)
    if 5 <= num <= 10:
        chosen_dia, chosen_num = dia, num
        break

# 3. حساب الأطوال والكميات بدقة
bar_length = Lx + 0.20 # إضافة العكفات
weight_per_m = (chosen_dia**2 / 162)
dist_weight_m = (8**2 / 162) * 5 # حديد توزيع ثابت 5T8

if mesh_type == "شبكة واحدة + برانيط":
    total_steel_m2 = (chosen_num * weight_per_m * bar_length) + (chosen_num * weight_per_m * (Lx/3)) + (dist_weight_m * Lx)
    markup = 1.07 # 7% فضلات وتداخل
else:
    total_steel_m2 = (chosen_num * weight_per_m * bar_length * 2) + (dist_weight_m * Lx * 2)
    markup = 1.15 # 15% كراسي وفضلات

total_weight_kg = total_steel_m2 * Ly * markup
total_concrete = Lx * Ly * (h_cm/100)

# --- عرض النتائج ---
st.write("##")
col_res1, col_res2 = st.columns([2, 1])

with col_res1:
    st.subheader("📊 تفاصيل التسليح المحسوبة")
    res_df = pd.DataFrame({
        "النوع": ["الحديد الرئيسي (سفلي)", "الحديد العلوي", "حديد التوزيع", "الخرسانة"],
        "الوصف": [f"{chosen_num} Φ {chosen_dia} / m'", 
                  f"{chosen_num} Φ {chosen_dia} / m'" if mesh_type == "شبكتين كاملتين" else "برانيط عند المساند",
                  "5 Φ 8 / m'", "بيتون مسلح عيار 350"],
        "الطول التقديري": [f"{bar_length:.2f} m", "-", f"{Ly:.2f} m", "-"]
    })
    st.table(res_df)

with col_res2:
    st.subheader("💰 جدول الكميات (BOQ)")
    st.metric("إجمالي الحديد", f"{total_weight_kg:.0f} KG")
    st.metric("إجمالي الخرسانة", f"{total_concrete:.2f} M³")

# --- الرسم الهندسي المطور ---


fig, ax = plt.subplots(figsize=(10, 3))
ax.add_patch(plt.Rectangle((0, 0), 10, h_cm/2, color='#E0E0E0', ec='black'))
# رسم الأسياخ
ax.plot([0.1, 9.9], [0.8, 0.8], color='#C0392B', lw=3, label='Bottom') # سفلي
if mesh_type == "شبكتين كاملتين":
    ax.plot([0.1, 9.9], [h_cm/2-0.8, h_cm/2-0.8], color='#2980B9', lw=3) # علوي كامل
else:
    ax.plot([0.1, 2.5], [h_cm/2-0.8, h_cm/2-0.8], color='#2980B9', lw=3) # برانيط
    ax.plot([7.5, 9.9], [h_cm/2-0.8, h_cm/2-0.8], color='#2980B9', lw=3)

ax.axis('off')
st.pyplot(fig)

# --- تذييل البرنامج (الختم المهني) ---
st.markdown("---")
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.markdown(f"**المهندس المدني:** بيلان مصطفى عبدالكريم")
    st.markdown(f"📞 **للتواصل:** 0998449697")
with col_f2:
    st.markdown(f"📍 **الاختصاص:** دراسات - إشراف - تعهدات")
    if st.button("طباعة التقرير الفني 📄"):
        st.balloons()
        st.success("تم تجهيز التقرير للطباعة")
