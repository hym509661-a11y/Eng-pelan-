import streamlit as st
import math

# إعدادات المكتب والختم
st.set_page_config(page_title="المكتب الهندسي - م. بيلان", layout="wide")
st.sidebar.markdown(f"### المهندس المدني بيلان مصطفى عبدالكريم\nدراسات-اشراف-تعهدات\n0998449697")

st.title("🏗️ النظام المتكامل للتصميم ورسم التسليح")
st.write("الحسابات تعتمد على الكود السوري - مشروع برج دمشق 11 طابق")

# المدخلات الأساسية
with st.sidebar:
    st.header("⚙️ المدخلات العامة")
    L = st.number_input("أكبر مجاز للمشروع L (cm):", value=530)
    fy = st.sidebar.selectbox("إجهاد الخضوع للحديد (MPa):", [400, 280, 420], index=0)
    fc = st.sidebar.number_input("مقاومة البيتون f'c (MPa):", value=25)

tabs = st.tabs(["البلاطات (مصمتة/هوردي)", "الجوائز والأعمدة", "الأساسات (منفرد/حصيرة)", "تفاصيل التسليح (رسم)"])

# --- 1. البلاطات ---
with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🍀 البلاطة المصمتة (Solid)")
        h_solid = max(12, math.ceil((L/35)/2)*2)
        st.success(f"السماكة المعتمدة: {h_solid} cm")
        As_min = 0.0018 * 100 * h_solid
        st.write(f"التسليح الأدنى: {As_min:.2f} cm²/m")
        st.info(f"المقترح: 5 T 10 / m (فرش وغطاء)")

    with col2:
        st.subheader("🏗️ البلاطة الهوردي")
        h_rib = max(30, math.ceil((L/20)/2)*2)
        st.success(f"السماكة المعتمدة: {h_rib} cm")
        st.write("التسليح: 2 T 14 (سفلي للعصب)")

# --- 2. الجوائز والأعمدة ---
with tabs[1]:
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("📏 الجوائز (Beams)")
        h_beam = math.ceil((L/14 + 10)/5)*5
        st.success(f"جائز ساقط: 30 × {h_beam} cm")
        st.write(f"الكانات: T 8 @ 15 cm (تكثيف عند المساند)")
        
    with col4:
        st.subheader("🗿 الأعمدة (Columns)")
        st.write("تدرج الأعمدة (C1):")
        st.table({"الطابق": ["القبو", "المتكرر", "الأخير"], "الأبعاد": ["30x100", "30x70", "30x50"]})

# --- 3. الأساسات ---
with tabs[2]:
    st.header("🧱 القواعد والأساسات")
    f_type = st.selectbox("نوع الأساس:", ["أساس منفرد", "أساس مشترك", "حصيرة (Raft)"])
    
    if f_type == "حصيرة (Raft)":
        h_raft = max(90, math.ceil((L/6)/10)*10)
        st.success(f"سماكة الحصيرة المعتمدة: {h_raft} cm")
        st.write(f"التسليح: شبكتين (علوي وسفلي) 7 T 20 / m")
    else:
        st.write("يتم التصميم بناءً على قدرة تحمل التربة (2.5 kg/cm²)")

# --- 4. تفاصيل التسليح والرسم ---
with tabs[3]:
    st.header("🎨 مخططات التسليح الدقيقة")
    
    st.subheader("1. تفصيلة " + f_type)
    if f_type == "حصيرة (Raft)":
        st.markdown("""
        * **الشبكة السفلية:** حديد مستمر مع "رجل بطة" (U-Shape) عند النهايات بطول $L_d$.
        * **الشبكة العلوية:** حديد مستمر محمول على **كراسي (Chairs)** بارتفاع مناسب.
        * **الوصلات:** تراكب (Overlap) بمقدار $50\phi$ (حوالي 100 سم لقطر 20).
        """)
        
    
    st.subheader("2. تسليح الجوائز (الشابويات)")
    st.markdown(f"""
    * **تسليح سفلي:** 3 T 16 مستمر.
    * **تسليح علوي (شابويات):** إضافي عند المساند يمتد لـ $L/4$ من وجه العمود.
    * **الكانات:** مغلقة بزاوية 135 درجة (Anti-seismic hooks).
    """)
    

    st.subheader("3. تسليح الدرج (أجر البطة)")
    st.markdown("""
    * **التسليح الرئيسي:** يتم عمل "مقص" (Scissor junction) عند التقاء الشاحط بالميدة.
    * **أجر البطة:** نهايات الحديد تثبت داخل الجوائز الحاملة بطول ارتكاز كافٍ.
    """)
