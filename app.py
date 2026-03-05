import streamlit as st
import math

# إعداد الهوية الهندسية
st.set_page_config(page_title="برج دمشق - المكتب الهندسي", layout="wide")

# الختم المهني (دراسات-اشراف-تعهدات)
st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 10px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold; color: #ef4444;">0998449697</p>
    <hr>
    <p style="margin: 0; font-size: 0.9em;">دراسات - إشراف - تعهدات</p>
</div>
""", unsafe_allow_html=True)

# المدخلات الأساسية من المذكرة الحسابية
with st.sidebar:
    st.header("📋 مدخلات المشروع")
    L = st.number_input("أطول مجاز L (cm):", value=530, step=10)
    n_floors = st.number_input("عدد الطوابق الإجمالي:", value=11)
    st.divider()
    st.info("كافة التفاصيل أدناه محسوبة وفق الكود السوري للمجاز المختار.")

st.title("🏛️ المنصة المتكاملة لتصميم وتفريد حديد برج دمشق")

# --- 1. الحسابات الإنشائية (المرتبطة بالمجاز L) ---

# البلاطات (Slabs)
h_solid_qabo = max(15, math.ceil(L / 32))  # بلاطة القبو (مصمتة - شرط السهم)
h_horidi = max(30, math.ceil(L / 20))      # بلاطة المتكرر (هوردي - مستمرة)

# الجوائز (Beams)
h_drop = math.ceil(L / 12)                 # الجائز الساقط (L/12 للأبراج)
b_hidden = max(100, math.ceil(L / 4))      # الجائز المخفي (عرض L/4)

# الأعمدة (Columns) - تدرج منطقي 30xL
load_p = ((L/100)**2) * 1.2 * n_floors     # حمولة العمود التقديرية (طن)
col_len = max(50, math.ceil((load_p * 1000) / (0.35*250 + 0.67*0.01*4000) / 30 / 10) * 10)

# الحصيرة (Raft)
h_raft = max(90, math.ceil(L / 6))

# --- 2. عرض المذكرة الحسابية والتفاصيل ---
tab1, tab2 = st.tabs(["📝 المذكرة الحسابية (أبعاد وكميات)", "📐 لوحات التفصيل (Shop Drawings)"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📍 الأبعاد البيتونية (Concrete)")
        st.markdown(f"""
        - **سماكة بلاطة القبو:** `{h_solid_qabo} cm`
        - **سماكة بلاطة الهوردي:** `{h_horidi} cm`
        - **الجائز الساقط:** `30 × {h_drop} cm`
        - **الجائز المخفي (عرض):** `{b_hidden} cm`
        - **عمود القبو:** `30 × {col_len} cm`
        - **سماكة الحصيرة:** `{h_raft} cm`
        """)
    with col2:
        st.subheader("📍 تقدير حديد التسليح (Steel)")
        st.markdown(f"""
        - **حديد الجائز السفلي:** `4 T 16` (مستمر)
        - **الشابويات (إضافي علوي):** `3 T 16` (بطول `{L/4:.0f} cm`)
        - **تسليح الأعمدة:** `{math.ceil(col_len/10)*2} T 16`
        - **تسليح الحصيرة:** `7 T 20 / m` (شبكتين)
        """)

with tab2:
    st.header("📐 الرسوم التفصيلية المعتمدة")
    
    # 1. تفصيل الجائز والشابويات
    st.subheader("1️⃣ تفريد حديد الجوائز (شابويات)")
    st.write(f"يتم وضع الحديد الإضافي العلوي (الشابويه) فوق المساند ليمتد مسافة **{L/4:.0f} cm** من كل طرف.")
    

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("2️⃣ أجر البطة (Base Anchors)")
        st.write("تفصيلة تثبيت أشاير أعمدة القبو داخل الحصيرة بعكفة L.")
        

    with col_b:
        st.subheader("3️⃣ مقص الدرج (Scissor Joint)")
        st.write("تفصيلة المقص عند البسطة لمنع انفصال الخرسانة نتيجة محصلة القوى.")
        

    st.subheader("4️⃣ كراسي الحصيرة (Steel Chairs)")
    st.write(f"يتم تصنيع الكراسي بارتفاع **{h_raft-15} cm** لرفع الشبكة العلوية.")
    

st.divider()
st.caption(f"تم الربط البرمجي الكامل للمجاز L={L} وفق المذكرة الحسابية - م. بيلان مصطفى")
