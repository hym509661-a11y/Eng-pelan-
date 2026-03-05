import streamlit as st
import math

# إعدادات الصفحة وهوية المكتب
st.set_page_config(page_title="مكتب المهندس بيلان - التصميم المتكامل", layout="wide")

# الختم الخاص بالمهندس (حسب التعليمات)
st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 10px; border-radius: 10px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0;">دراسات - إشراف - تعهدات</p>
    <p style="color: #ef4444; font-weight: bold; margin: 5px 0;">0998449697</p>
</div>
""", unsafe_allow_html=True)

# مدخلات التحكم في الشريط الجانبي
with st.sidebar:
    st.markdown("---")
    st.header("⚙️ معطيات المشروع")
    n_floors = st.number_input("عدد الطوابق الإجمالي:", value=11, min_value=1)
    L_cm = st.number_input("أكبر مجاز L (cm):", value=530)
    st.divider()
    fc = 25 # MPa
    fy = 400 # MPa

st.title("🏗️ المنصة الهندسية المتكاملة للتصميم والرسوم التفصيلية")

# --- العمليات الحسابية (المنطق الهندسي الصحيح) ---
# 1. حساب أبعاد العمود (قبو)
# مساحة التحميل 25م2، حمل المتر المربع التراكمي 1.1 طن (مع تخفيض الحي)
P_total = 25 * 1.1 * n_floors 
# الأبعاد (العرض ثابت 30سم)
area_req = (P_total * 1000) / (0.35 * fc + 0.67 * 0.01 * fy)
col_length = max(50, math.ceil(area_req / 30 / 10) * 10) # تقريب لأقرب 10 سم
rebar_count = math.ceil((0.01 * 30 * col_length) / 3.14) # عدد قضبان T20 تقريبي

# 2. الجوائز والبلاطات
h_drop = math.ceil((L_cm / 14 + 10) / 5) * 5
b_hidden = max(105, math.ceil((L_cm / 4) / 5) * 5)
h_raft = max(90, math.ceil((L_cm / 6) / 10) * 10)

# --- عرض النتائج في تبويبات ---
tab1, tab2 = st.tabs(["📊 جداول البيانات النهائية", "📐 لوحات التسليح التفصيلية"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📍 أبعاد الأعمدة والجوائز")
        st.table({
            "العنصر الإنشائي": ["عمود القبو", "عمود الطابق الأخير", "جائز ساقط (قبو)", "جائز مخفي (هوردي)", "سماكة الهوردي"],
            "الأبعاد المعتمدة (cm)": [f"30 × {col_length}", "30 × 50", f"30 × {h_drop}", f"{b_hidden} × 30", "30 cm"],
            "التسليح المقترح": [f"{rebar_count*2} T 16", "8 T 14", "4 T 16 سفلي", "6 T 16 سفلي", "2 T 14 / عصب"]
        })
    with c2:
        st.subheader("📍 البلاطات والأساسات")
        st.success(f"• سماكة الحصيرة المعتمدة: **{h_raft} cm**")
        st.success(f"• سماكة بلاطة الملجأ: **20 cm**")
        st.success(f"• سماكة البلاطة المصمتة: **12 cm**")
        st.info(f"• حمولة العمود التصميمية: {P_total:.1f} Ton")

with tab2:
    st.subheader("🔍 التفاصيل الإنشائية (Shop Drawings)")
    
    # تفصيلة 1: الجائز والشابويات
    st.markdown("### 1️⃣ تسليح الجائز المستمر (العلوي والسفلي)")
    
    st.markdown(f"""
    - **الشابويات (إضافي علوي):** تمتد لمسافة **{L_cm/4:.0f} cm** من وجه العمود.
    - **الكانات:** تكثيف أول متر T10 @ 10cm، والباقي T8 @ 15cm.
    """)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 2️⃣ أجر البطة (أشاير العمود)")
        
        st.write("يتم ثني الأشاير داخل القاعدة بطول **40 cm** لضمان التثبيت.")

    with col_b:
        st.markdown("### 3️⃣ مقص الدرج (Scissor Detail)")
        
        st.write("ضروري جداً عند التقاء الشاحط بالبسطة لمنع تشقق الخرسانة.")

    st.markdown("### 4️⃣ كراسي الحصيرة (Chairs)")
    
    st.write(f"توزع الكراسي بارتفاع **{h_raft-15} cm** لحمل الشبكة العلوية.")

st.divider()
st.caption(f"تمت الحسابات وفق الكود السوري - مكتب المهندس بيلان - عدد الطوابق: {n_floors}")
