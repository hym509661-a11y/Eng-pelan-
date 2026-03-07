import streamlit as st
import math

# إعداد الهوية المهنية للمهندس بيلان
st.set_page_config(page_title="مكتب م. بيلان - التصميم الإنشائي", layout="wide")

st.sidebar.markdown("""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold; color: #ef4444;">0998449697</p>
    <p style="margin: 5px 0; font-size: 0.85em;">الجمهورية العربية السورية - برج دمشق</p>
</div>
""", unsafe_allow_html=True)

# مدخلات يدوية دقيقة لضمان عدم حدوث أخطاء برمجية
with st.sidebar:
    st.header("⚙️ مدخلات المخطط")
    L = st.number_input("أطول مجاز صافي L (cm):", value=530)
    n_floors = st.number_input("عدد الطوابق الإجمالي:", value=11)
    st.divider()
    st.info("بلاطة القبو: مصمتة دائماً\nبلاطة المتكرر: هوردي دائماً")

st.title("🏗️ نظام توليد المخططات التنفيذية وتفريد الحديد")

# --- الحسابات الإنشائية (الكود العربي السوري) ---

# 1. سماكة البلاطات
h_solid_qabo = max(15, math.ceil(L / 35))  # بلاطة القبو المصمتة (شرط السهم)
h_horidi = 30  # بلاطة الهوردي (24 بلوكة + 6 تغطية) كما في الصورة

# 2. تسليح الجوائز (مطابق لصورك: 4 T 16 سفلي / 2 T 12 علوي)
h_beam = math.ceil(L / 12)
b_beam = 30

# 3. تدرج الأعمدة (كل 3 طوابق)
col_qabo = max(50, math.ceil((((L/100)**2) * 1.25 * n_floors * 1000) / (0.35*250 + 0.67*0.01*4000) / 30 / 10) * 10)

# --- عرض المخططات والرسومات ---
tab1, tab2, tab3 = st.tabs(["📐 رسم البلاطات", "🛠️ تفريد الجوائز والأعمدة", "📝 المذكرة الحسابية"])

with tab1:
    st.subheader("📍 لوحة سقف المتكرر (بلاطة هوردي)")
    st.write(f"**اتجاه الأعصاب:** باتجاه المجاز الأصغر ({L} cm).")
        
    st.subheader("📍 قطاع تفصيلي في بلاطة الهوردي (مثل صورتك المرفقة)")
        st.markdown(f"""
    - **سماكة البلاطة:** {h_horidi} cm.
    - **تسليح العصب:** 2 T 14 (سفلي) + T 12 (علوي).
    - **بلاطة التغطية:** شبكة T 8 كل 20 سم.
    """)
    
    st.divider()
    st.subheader("📍 لوحة سقف القبو (بلاطة مصمتة)")
    st.write(f"**سماكة البلاطة:** {h_solid_qabo} cm")
        st.write("**التسليح:** شبكتين T 10 كل 15 سم (فرش وغطاء).")

with tab2:
    st.header("🛠️ تفريد الحديد (Shop Drawings)")
    
    # تفريد الجوائز (مطابق تماماً لصورتك)
    st.subheader("1️⃣ تفريد حديد الجائز الساقط (4 T 16 / 2 T 12)")
    col_a, col_b = st.columns(2)
    with col_a:
                st.write(f"مقطع الجائز: {b_beam} × {h_beam} cm")
    with col_b:
                st.write(f"طول الشابويه: {L/4:.0f} cm من وجه المسند.")

    # تفريد الأعمدة وتفصيلة أجر البطة
    st.subheader("2️⃣ تدرج الأعمدة وأشاير التأسيس")
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**عمود القبو:** 30 × {col_qabo} cm")
        st.write(f"**تدرج العمود:** ينقص 10 سم كل 3 طوابق.")
            with c2:
        st.write("**تفصيلة أجر البطة**")
                st.write("عكفة الأشاير 40 سم داخل الحصيرة.")

    st.subheader("3️⃣ تفصيلة مقص الدرج")
        st.write("تسليح المقص: T 12 كل 15 سم.")

with tab3:
    st.subheader("📝 جداول الكميات والأبعاد النهائية")
    st.table({
        "العنصر": ["بلاطة القبو", "بلاطة المتكرر", "الجائز الرئيسي", "عمود القبو"],
        "الأبعاد (cm)": [h_solid_qabo, h_horidi, f"{b_beam}x{h_beam}", f"30x{col_qabo}"],
        "التسليح (العدد والقطر)": ["T 10 @ 15cm", "2 T 14 / عصب", "4 T 16 سفلي + 2 T 12 علوي", f"{math.ceil(col_qabo/12)*2} T 16"]
    })

st.divider()
st.button("💾 تحميل المخططات والمذكرة الحسابية بصيغة PDF")
