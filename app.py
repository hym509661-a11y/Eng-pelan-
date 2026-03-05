import streamlit as st
import math

# إعداد الهوية المهنية
st.set_page_config(page_title="مكتب المهندس بيلان مصطفى", layout="wide")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/609/609034.png", width=100)
st.sidebar.markdown(f"### المهندس المدني: بيلان مصطفى\n0998449697")

# --- مدخلات التحكم (تغير كل الحسابات) ---
with st.sidebar:
    st.header("⚙️ معطيات التصميم")
    n_floors = st.slider("عدد الطوابق:", 1, 15, 11)
    L = st.number_input("أكبر مجاز L (cm):", value=530)
    st.divider()
    f_type = st.radio("نوع الأساس للمقارنة:", ["منفرد", "مشترك", "حصيرة"])

st.title("🏗️ نظام التصميم الإنشائي المتكامل - برج دمشق")
st.markdown("---")

# تبويبات العناصر الإنشائية
t1, t2, t3, t4, t5 = st.tabs(["البلاطات (مصمتة/هوردي)", "الجوائز (ساقطة/مخفية)", "الأعمدة", "الأساسات", "تفاصيل التسليح"])

# --- 1. البلاطات ---
with t1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🍀 البلاطة المصمتة (سقف القبو)")
        h_solid = max(12, math.ceil((L/35)/2)*2)
        st.success(f"السماكة المعتمدة: {h_solid} cm")
        st.write(f"الحديد: الشبكة الأساسية 5 T 10 / m")
    with col2:
        st.subheader("🏗️ البلاطة الهوردي (المتكرر)")
        h_rib = max(30, math.ceil((L/20)/2)*2)
        st.success(f"السماكة المعتمدة: {h_rib} cm")
        st.write(f"الأعصاب: 2 T 14 سفلي | 1 T 12 علوي")

# --- 2. الجوائز ---
with t2:
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("📏 الجوائز الساقطة")
        h_drop = math.ceil((L/14 + 10)/5)*5
        st.success(f"الأبعاد: 30 × {h_drop} cm")
        st.write("الحديد: 4 T 16 سفلي | 3 T 14 علوي")
    with col4:
        st.subheader("📏 الجوائز المخفية")
        b_hidden = max(105, math.ceil((L/4)/5)*5)
        st.success(f"العرض المعتمد: {b_hidden} cm")
        st.write(f"السماكة: نفس سماكة الهوردي ({h_rib} cm)")

# --- 3. الأعمدة ---
with t3:
    st.header("🗿 تدرج الأعمدة")
    # معادلة تقريبية لحمل العمود بناء على عدد الطوابق
    load = (n_floors * 25 * 1.2) # طن
    width = 30
    length = max(50, math.ceil((load * 1000 / (0.4 * 250)) / 5) * 5)
    st.info(f"حمل العمود التقديري للطابق الأرضي: {load:.1f} طن")
    st.success(f"أبعاد العمود المقترحة: {width} × {length} cm")

# --- 4. الأساسات ---
with t4:
    st.header("🧱 تصميم القواعد")
    if f_type == "منفرد":
        dim = math.sqrt((load * 1.1) / 25) # m
        st.success(f"أبعاد الأساس: {dim:.2f} × {dim:.2f} m | السماكة: 60 cm")
    elif f_type == "مشترك":
        st.success(f"أساس مشترك: {L/100 + 1:.1f} m طول × 2.0 m عرض")
    else:
        h_raft = max(90, math.ceil((L/6)/10)*10)
        st.success(f"سماكة الحصيرة المعتمدة: {h_raft} cm")

# --- 5. الرسم الدقيق للحديد (Visual Details) ---
with t5:
    st.header("🎨 تفاصيل تسليح العناصر")
    
    st.subheader("1. تسليح الجوائز والشابويات")
    st.markdown("""
    - **حديد سفلي:** مستمر مع عكفات (Hooks) عند الأعمدة.
    - **شابويات (علوي):** حديد إضافي فوق الأعمدة يمتد لـ $L/4$.
    - **كانات:** تكثيف (T10 @ 10cm) في أول متر من العمود.
    """)
    

    st.subheader("2. تسليح البلاطة المصمتة وأجر البطة")
    st.markdown("""
    - **التسليح:** شبكة سفلية تنتهي بـ "أجر بطة" (U-Bar) داخل الجائز الساقط لضمان التثبيت.
    - **الملجأ:** زيادة التسليح لـ 7 T 12 / m.
    """)
    

    st.subheader("3. تسليح الحصيرة والأساسات")
    st.markdown("""
    - **كراسي (Chairs):** بارتفاع الحصيرة لرفع الشبكة العلوية.
    - **أشاير الأعمدة:** تنزل لأسفل الأساس وتفرش "رجل بطة" بطول 30-40 سم.
    """)
    

    st.subheader("4. تسليح الدرج (المقص)")
    st.markdown("""
    - **المقص:** عند التقاء الشاحط مع البسطة لمنع انفصال الخرسانة.
    - **السماكة:** تتبع $L/20$ كما ورد في شرحك.
    """)
    

st.divider()
st.caption("برمجية المهندس بيلان مصطفى - دمشق 2026")
