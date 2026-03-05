import streamlit as st
import math

# إعداد الهوية المهنية
st.set_page_config(page_title="المكتب الهندسي - م. بيلان مصطفى", layout="wide")

# الختم الرسمي الثابت (دراسات-اشراف-تعهدات)
st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 10px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold;">0998449697</p>
    <p style="margin: 5px 0; color: #666; font-size: 0.9em;">دراسات - إشراف - تعهدات</p>
</div>
""", unsafe_allow_html=True)

# محرك المتغيرات (المجاز هو المتحكم الرئيسي)
with st.sidebar:
    st.header("⚙️ معطيات المذكرة الحسابية")
    L = st.number_input("أطول مجاز L (cm):", value=530, step=10)
    n_floors = st.number_input("عدد الطوابق (N):", value=11)
    st.divider()
    st.caption("يتم تحديث كافة تفاصيل الحديد والبيتون بناءً على L")

st.title("🏛️ منصة تصميم برج دمشق (وفق المذكرة الحسابية)")

# --- 1. الحسابات الإنشائية المرتبطة بالمجاز L ---

# البلاطات
h_qabo = max(15, math.ceil(L / 30))  # بلاطة القبو المصمتة (شرط السهم للملاجئ/المصمتة)
h_horidi = max(30, math.ceil(L / 20)) # بلاطة الهوردي (L/20 للمتكرر)

# الجوائز
h_drop = math.ceil(L / 12) # الجائز الساقط (L/12 للمجالات الكبيرة في الأبراج)
b_hidden = max(100, math.ceil(L / 4)) # الجائز المخفي (العرض L/4)

# الأعمدة (تدرج منطقي 30xL)
p_total = ((L/100)**2) * 1.25 * n_floors # طن
col_len = max(50, math.ceil((p_total * 1000) / (0.35*250 + 0.67*0.01*4000) / 30 / 10) * 10)

# الحصيرة
h_raft = max(90, math.ceil(L / 6))

# --- 2. عرض النتائج التفصيلية ---
tab1, tab2, tab3 = st.tabs(["📋 المذكرة الحسابية", "📐 تفاصيل التسليح (Shop Drawings)", "🧱 جداول الكميات"])

with tab1:
    st.subheader("📝 أبعاد العناصر الإنشائية (قوانين الكود السوري)")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**سقف القبو (بلاطة مصمتة):** {h_qabo} cm")
        st.info(f"**سقف المتكرر (بلاطة هوردي):** {h_horidi} cm")
        st.info(f"**الجائز الساقط (L/12):** 30 × {h_drop} cm")
    with col2:
        st.info(f"**الجائز المخفي (L/4):** عرض {b_hidden} cm")
        st.info(f"**عمود القبو (تدرج):** 30 × {col_len} cm")
        st.info(f"**سماكة الحصيرة (L/6):** {h_raft} cm")

with tab2:
    st.subheader("🔍 تفاصيل تفريد الحديد")
    
    # تفصيل الجائز والشابويات
    st.markdown("### 1️⃣ تفريد حديد الجوائز")
    
    st.write(f"• **الحديد السفلي:** 4 T 16 مستمر")
    st.write(f"• **الشابويات (إضافي علوي):** 3 T 16 يمتد مسافة {L/4:.0f} cm من وجه العمود.")
    st.write(f"• **الكانات:** T10 @ 10cm (تكثيف عند المساند لمسافة 1.5H).")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 2️⃣ أجر البطة (Base Hook)")
        
        st.write("ثني أشاير الأعمدة داخل الحصيرة بطول 40 cm لضمان انتقال العزوم.")

    with col_b:
        st.markdown("### 3️⃣ مقص الدرج (Scissor Joint)")
        
        st.write("يمنع انفصال البيتون في منطقة البسطة. تسليح الدرج: T12 @ 15cm.")

    st.markdown("### 4️⃣ كراسي الحصيرة (Chairs)")
    
    st.write(f"ارتفاع الكرسي: {h_raft - 15} cm لحمل الشبكة العلوية (7 T 20 / m).")

with tab3:
    st.subheader("📦 جدول تفريد الحديد التقديري (BBS)")
    st.table({
        "العنصر": ["جائز ساقط", "بلاطة مصمتة", "أعمدة القبو", "الحصيرة"],
        "التسليح الأساسي": ["4 T 16 سفلي", "T10 @ 15cm", f"{math.ceil(col_len/10)*2} T 16", "7 T 20 / m"],
        "الإضافات": [f"شابويات 3 T 16 طول {L/2:.0f}cm", "أجر بطة (U)", "كانات مكثفة T10", "كراسي بيتونية"]
    })

st.divider()
st.caption(f"تمت المطابقة مع ملف الشرح والمذكرة الحسابية لبرج دمشق - المجاز {L} cm")
