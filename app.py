import streamlit as st
import math

# إعدادات الصفحة وهوية المهندس
st.set_page_config(page_title="مكتب المهندس بيلان", layout="wide")
st.sidebar.markdown(f"### المهندس المدني بيلان مصطفى عبدالكريم\n0998449697")

st.title("🏗️ نظام التصميم الإنشائي المتكامل (إصدار الأساسات)")

# --- الإعدادات العامة في الشريط الجانبي ---
with st.sidebar:
    st.header("⚙️ معطيات المشروع")
    n_floors = st.number_input("عدد الطوابق:", min_value=1, max_value=20, value=11)
    L = st.number_input("المجاز بين الأعمدة L (cm):", value=530)
    q_allow = st.slider("قدرة تحمل التربة (kg/cm²):", 1.0, 4.0, 2.5)
    st.divider()
    st.info("الحسابات تعتمد على حمولات تقديرية للطوابق وفق الكود السوري")

# تبويبات البرنامج
tabs = st.tabs(["البلاطات والجوائز", "الأعمدة", "الأساسات المنفردة والمشتركة", "تفاصيل الرسم والتسليح"])

# --- 1. البلاطات والجوائز ---
with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🍀 البلاطة المصمتة")
        h_solid = max(12, math.ceil((L/35)/2)*2)
        st.success(f"السماكة المعتمدة: {h_solid} cm")
        st.write(f"التسليح المقترح: 5 T 10 / m")
    with col2:
        st.subheader("📏 الجوائز الساقطة")
        h_beam = math.ceil((L/14 + 10)/5)*5
        st.success(f"الأبعاد: 30 × {h_beam} cm")

# --- 2. الأعمدة (تتغير مع عدد الطوابق) ---
with tabs[1]:
    st.header("🗿 تصميم الأعمدة")
    # تقدير حمولة العمود (مساحة تحميل 25 م2 مثلاً)
    load_per_floor = 25 * 1.2 # ton (ميتة + حية)
    total_load = load_per_floor * n_floors
    area_req = (total_load * 1000) / (0.35 * 250 + 0.67 * 0.01 * 4000) # تقريبي
    
    st.write(f"الحمولة التقديرية للعمود في الطابق الأرضي: **{total_load:.1f} Ton**")
    width = 30
    length = max(40, math.ceil((area_req / width)/5)*5)
    st.success(f"أبعاد العمود المقترحة للقبو: {width} × {length} cm")

# --- 3. الأساسات (منفرد ومشترك) ---
with tabs[2]:
    st.header("🧱 تصميم القواعد")
    f_type = st.radio("اختر نوع الأساس:", ["أساس منفرد (Isolated)", "أساس مشترك (Combined)", "حصيرة (Raft)"])
    
    if f_type == "أساس منفرد (Isolated)":
        area_f = (total_load * 1.1) / (q_allow * 10) # m2
        side = math.sqrt(area_f)
        h_f = max(50, math.ceil((side*100/4)/5)*5)
        st.success(f"أبعاد الأساس المنفرد: {side:.2f} × {side:.2f} m")
        st.write(f"السماكة (H): {h_f} cm")
        st.info("التسليح: شبكة سفلية بالاتجاهين مع أرجل بطة للأعمدة")

    elif f_type == "أساس مشترك (Combined)":
        st.write("يستخدم عند تداخل القواعد أو قرب جدار الجار")
        length_c = (L/100) + 1.5
        width_c = (total_load * 2.1) / (length_c * q_allow * 10)
        st.success(f"أبعاد الأساس المشترك: {length_c:.2f} m (طول) × {width_c:.2f} m (عرض)")
        st.write("التسليح: يتطلب حديد علوي لمقاومة العزم السالب بين العمودين")

    else: # حصيرة
        h_raft = max(90, math.ceil((L/6)/10)*10)
        st.success(f"سماكة الحصيرة المعتمدة: {h_raft} cm")

# --- 4. تفاصيل الرسم والتسليح ---
with tabs[3]:
    st.header("🎨 تفاصيل التسليح الإنشائي")
    
    if f_type == "أساس منفرد (Isolated)":
        st.subheader("رسم الأساس المنفرد")
        st.markdown("""
        - **الحديد السفلي:** يمتد على كامل القاعدة مع عكفة (Hook) للأعلى بمقدار 15 سم.
        - **أشاير الأعمدة:** تنزل لأسفل القاعدة وتفرش "أجر بطة" بطول لا يقل عن 30 سم.
        """)
        
        
    elif f_type == "أساس مشترك (Combined)":
        st.subheader("رسم الأساس المشترك")
        st.markdown("""
        - **حديد سفلي:** مستمر لمقاومة العزوم الموجبة تحت الأعمدة.
        - **حديد علوي (شابويات):** كثيف في المنطقة بين العمودين لمقاومة العزم السالب.
        - **كانات:** توضع كانات عرضية لتربيط الشبكتين.
        """)
        
        
    elif f_type == "حصيرة (Raft)":
        st.subheader("رسم الحصيرة")
        st.markdown("""
        - **الشبكة السفلية والعلوية:** حديد مستمر T20.
        - **الكراسي (Chairs):** توضع بارتفاع (H - 15cm) لحمل الشبكة العلوية.
        - **أجر البطة:** عند أطراف الحصيرة لربط الشبكتين معاً.
        """)
        

st.divider()
st.caption("برمجية المهندس بيلان - حسابات ديناميكية وفق الكود العربي السوري")
