import streamlit as st
import math

# الختم المهني المعتمد
st.set_page_config(page_title="مكتب المهندس بيلان مصطفى", layout="wide")

st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold; color: #ef4444;">0998449697</p>
    <p style="margin: 5px 0; font-size: 0.85em;">دراسات - إشراف - تعهدات</p>
</div>
""", unsafe_allow_html=True)

# المدخلات
with st.sidebar:
    st.header("⚙️ معطيات المذكرة الحسابية")
    L = st.number_input("أطول مجاز L (cm):", value=530)
    n_floors = st.number_input("عدد الطوابق الإجمالي:", value=11)
    st.info("الحسابات مطابقة للكود السوري - ملحق البلاطات والأعمدة")

st.title("🏗️ التصميم الإنشائي وتفريد التسليح الدقيق")

# --- الحسابات المصححة (الكود السوري) ---

# 1. بلاطة القبو (مصمتة مستمرة)
# h = L / 40 (للبلاطات المستمرة من طرفين)
h_solid = max(12, math.ceil(L / 42)) 

# 2. الجوائز الساقطة
h_drop = math.ceil(L / 14) + 5 # رشاقة أعلى حسب الكود
b_drop = 30

# 3. الأعمدة (حساب دقيق للحمل)
# مساحة التحميل 20م2، وزن المتر 1.1 طن، تخفيض أحمال 0.6 للطابق 11
p_total = 20 * 1.1 * (n_floors * 0.7) # حمل تشغيلي مقدر
col_len = max(50, math.ceil((p_total * 1000) / (0.35*250 + 0.67*0.01*4000) / 30 / 10) * 10)

# --- عرض النتائج الجدولي ---
st.subheader("📊 أبعاد العناصر الإنشائية")
st.table({
    "العنصر": ["بلاطة القبو", "جائز ساقط", "عمود القبو (30xL)"],
    "الحساب الحالي (cm)": [f"{h_solid} cm", f"30 × {h_drop} cm", f"30 × {col_len} cm"],
    "ملاحظات الكود": ["L/42 (مصمتة مستمرة)", "L/14 + 5", "P_total / Area"]
})

# --- الرسوم التفصيلية للحديد ---
st.header("📐 لوحات تفريد الحديد (Shop Drawings)")

# 1. الجائز الساقط
st.subheader("1️⃣ تفريد حديد الجائز الساقط")

st.markdown(f"""
- **سفلي مستمر:** 4 T 16
- **علوي تعليق:** 2 T 12
- **إضافي علوي (شابوه):** 3 T 16 (طول التوضع {L/4:.0f} cm من وجه العمود)
- **كانات:** T 10 (كل 10 cm عند المساند | كل 20 cm في المنتصف)
""")

# 2. العمود وتفصيلة أجر البطة
st.subheader("2️⃣ تسليح الأعمدة وأشاير التأسيس")
col_a, col_b = st.columns(2)
with col_a:
    
    st.write(f"مقطع العمود: 30 × {col_len} cm")
    st.write(f"التسليح: {math.ceil(col_len/12)*2} T 16")
with col_b:
    
    st.write("تفصيلة **أجر البطة**: ثني الأشاير بطول 40 cm داخل الحصيرة.")

# 3. الدرج وبلاطة القبو
st.subheader("3️⃣ تسليح بلاطة القبو ومقص الدرج")
col_c, col_d = st.columns(2)
with col_c:
    
    st.write(f"بلاطة القبو (h={h_solid} cm):")
    st.write("شبكة سفلية + علوية T 10 @ 15 cm")
with col_d:
    
    st.write("تفصيلة **المقص**: لمنع انفصال الخرسانة عند البسطة (T 12 @ 15 cm).")

st.divider()
st.caption("تم التحديث وفق اشتراطات الكود العربي السوري - م. بيلان مصطفى")
