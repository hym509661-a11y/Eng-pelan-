import streamlit as st
import math

# إعداد الصفحة والختم المهني
st.set_page_config(page_title="مكتب المهندس بيلان - التصميم المتكامل", layout="wide")

st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 10px; border-radius: 10px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold; color: #ef4444;">0998449697</p>
</div>
""", unsafe_allow_html=True)

# مدخلات التحكم (المحرك الأساسي للحسابات)
with st.sidebar:
    st.header("⚙️ متغيرات التصميم")
    L = st.number_input("طول المجاز L (cm):", value=530, step=10)
    n_floors = st.slider("عدد الطوابق:", 1, 15, 11)
    st.divider()
    fy = 400  # MPa
    fc = 25   # MPa

st.title("🏗️ النظام الديناميكي لتصميم ورسم المنشآت")
st.info(f"تم ربط جميع العناصر بالمجاز الحالي: {L} cm")

# --- الحسابات المرتبطة كلياً بالمجاز L ---

# 1. بلاطة القبو (تتغير الآن مع L)
# الكود: المحيط / 140 أو L/35 للبلاطات المصمتة باتجاهين
h_qabo = max(12, math.ceil((L / 35) / 2) * 2)
h_shelter = 20 # ثابتة للملاجئ حسب الكود

# 2. الجوائز (ساقطة ومخفية)
h_drop = math.ceil((L / 14 + 10) / 5) * 5
b_hidden = max(105, math.ceil((L / 4) / 5) * 5)

# 3. الأعمدة (مساحة التحميل مرتبطة بـ L)
load_area = (L/100)**2
total_p = load_area * 1.15 * n_floors # طن
col_len = max(50, math.ceil(((total_p * 1000) / (0.35*fc + 0.67*0.01*fy)) / 30 / 10) * 10)

# 4. حسابات الحديد (تتغير مع الأبعاد)
# فرضاً للجائز الساقط
steel_bott = math.ceil((0.005 * 30 * h_drop) / 2.01) # T16
steel_top = math.ceil(steel_bott * 0.75)
stirrups = "T10 @ 10cm" # تكثيف

# --- العرض المرئي ---
tab1, tab2 = st.tabs(["📊 الحسابات الديناميكية", "📐 لوحات التسليح التفصيلية"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📍 البلاطات والجوائز")
        st.success(f"• سماكة بلاطة القبو (L/35): {h_qabo} cm")
        st.success(f"• ارتفاع الجائز الساقط (L/14): {h_drop} cm")
        st.success(f"• عرض الجائز المخفي (L/4): {b_hidden} cm")
    with c2:
        st.subheader("📍 الأعمدة والأساسات")
        st.warning(f"• عمود القبو (L_load): 30 × {col_len} cm")
        st.warning(f"• سماكة الحصيرة (L/6): {max(90, math.ceil((L/6)/10)*10)} cm")

with tab2:
    st.header("📐 لوحة تفريد الحديد (BBS)")
    
    # تفصيل الجائز
    st.markdown("### 1️⃣ تسليح الجوائز (ساقطة ومخفية)")
    
    st.table({
        "نوع التسليح": ["سفلي مستمر", "علوي مستمر", "إضافي علوي (شابوه)", "كانات (Stirrups)"],
        "العدد/القطر": [f"{steel_bott} T 16", f"{steel_top} T 14", f"{steel_top} T 16", stirrups],
        "طول التوضع": ["كامل الجائز", "كامل الجائز", f"يمتد {L/4:.0f} cm من وجه العمود", "تكثيف عند المساند"]
    })

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 2️⃣ تفصيلة أجر البطة (العمود)")
        
        st.write(f"ثني الأشاير داخل القاعدة بطول لا يقل عن 40 cm.")

    with col_b:
        st.markdown("### 3️⃣ مقص الدرج")
        
        st.write(f"سماكة الشاحط: {max(15, math.ceil((290/20)))} cm")

    st.markdown("### 4️⃣ تسليح البلاطة المصمتة (علوي وسفلي)")
    
    st.write(f"شبكة سفلية 5 T 10 / m | إضافي علوي فوق الجوائز (شابويات) {L/4:.0f} cm.")

st.divider()
st.caption(f"تحديث: تم ربط بلاطة القبو والأعمدة بالمجاز {L} cm - م. بيلان")
