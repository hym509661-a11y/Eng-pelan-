import streamlit as st
import math

# إعدادات الصفحة وهوية المكتب
st.set_page_config(page_title="مكتب المهندس بيلان - التصميم المتكامل", layout="wide")

# الختم المهني (تأكد من النسخ الكامل)
st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 10px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold;">0998449697</p>
    <p style="margin: 0; font-size: 0.8em;">دراسات - إشراف - تعهدات</p>
</div>
""", unsafe_allow_html=True)

# مدخلات التحكم في الشريط الجانبي (تغير الحسابات لحظياً)
with st.sidebar:
    st.header("⚙️ معطيات التحكم")
    n_floors = st.slider("عدد الطوابق الإجمالي:", 1, 15, 11)
    L = st.number_input("أطول مجاز L (cm):", value=530, step=10)
    st.divider()
    q_soil = st.slider("تحمل التربة (kg/cm²):", 1.0, 4.0, 2.5)

st.title("🏗️ الحاسبة الإنشائية الديناميكية المرتبطة بالمجاز")
st.caption("تم الربط البرمجي بين المجاز L والأبعاد الإنشائية وفق الكود السوري")

# --- العمليات الحسابية المرتبطة بالمجاز L وعدد الطوابق ---

# 1. الجوائز الساقطة: الارتفاع مرتبط بالمجاز (L/14) + 10 سم أمان
h_beam_drop = math.ceil((L / 14 + 10) / 5) * 5
# 2. الجوائز المخفية: العرض مرتبط بالمجاز (L/4)
b_hidden = max(105, math.ceil((L / 4) / 5) * 5)
# 3. البلاطة الهوردي: السماكة مرتبطة بالمجاز (L/20)
h_ribbed = max(30, math.ceil((L / 20) / 2) * 2)
# 4. الحصيرة: السماكة مرتبطة بالمجاز (L/6) وفق الكود السوري
h_raft = max(90, math.ceil((L / 6) / 10) * 10)

# 5. الأعمدة: مرتبطة بعدد الطوابق ومساحة التحميل (مساحة التحميل مرتبطة بالمجاز L^2)
area_load = (L/100) * (L/100) # مساحة التحميل التقريبية بالامتار المربعة
P_total = area_load * 1.1 * n_floors # الحمولة الكلية بالطن
area_req = (P_total * 1000) / (0.35 * 250 + 0.67 * 0.01 * 4000)
col_length = max(50, math.ceil(area_req / 30 / 10) * 10) # الطول (العرض ثابت 30)

# --- عرض النتائج ---
tab1, tab2 = st.tabs(["📊 نتائج الحسابات المرتبطة", "📐 تفاصيل الرسم الهندسي"])

with tab1:
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.subheader("📍 العناصر الخطية (جوائز وأعمدة)")
        st.write(f"**الجائز الساقط (L/14+10):** 30 × {h_beam_drop} cm")
        st.write(f"**الجائز المخفي (L/4):** عرض {b_hidden} cm")
        st.write(f"**عمود القبو (30xL):** 30 × {col_length} cm")
        st.info(f"حمولة العمود المحسوبة: {P_total:.1f} Ton")

    with col_res2:
        st.subheader("📍 البلاطات والأساسات")
        st.write(f"**بلاطة الهوردي (L/20):** {h_ribbed} cm")
        st.write(f"**الحصيرة (L/6):** {h_raft} cm")
        st.write(f"**بلاطة القبو المصمتة:** 12 cm")
        st.write(f"**بلاطة الملجأ:** 20 cm")

with tab2:
    st.header("📐 لوحات التسليح التفصيلية")
    
    # تفصيلة الجائز والشابويات
    st.subheader("1. تسليح الجوائز (الشابويات والكانات)")
    
    st.markdown(f"**ملاحظة:** الشابويات تمتد لمسافة **{L/4:.0f} cm** من وجه العمود.")

    # تفصيلة أجر البطة
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.subheader("2. أجر البطة (أشاير الأعمدة)")
        
        st.write("تثبيت الأشاير داخل القاعدة بشكل حرف L بطول 40 سم.")
    
    with col_d2:
        st.subheader("3. مقص الدرج (Scissor)")
        
        st.write("يتم عمل المقص عند البسطة لمنع انفصال الخرسانة.")

st.divider()
st.caption(f"تم تحديث كافة الحسابات بناءً على المجاز المتغير {L} cm - م. بيلان")
