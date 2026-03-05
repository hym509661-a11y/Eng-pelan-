import streamlit as st
import math

# الهوية المهنية حسب الختم المطلوب
st.set_page_config(page_title="مكتب المهندس بيلان مصطفى عبدالكريم", layout="wide")

st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0;">دراسات - إشراف - تعهدات</p>
    <p style="margin: 5px 0; color: #ef4444; font-weight: bold; font-size: 1.2em;">0998449697</p>
</div>
""", unsafe_allow_html=True)

# مدخلات المذكرة الحسابية
with st.sidebar:
    st.header("⚙️ معطيات التصميم")
    L = st.number_input("المجاز التصميمي L (cm):", value=530, step=10)
    n_floors = st.number_input("عدد الطوابق الإجمالي:", value=11)
    st.divider()
    st.caption("كافة النتائج أدناه مستخرجة وفق اشتراطات الكود العربي السوري")

st.title("🏗️ النظام المتكامل لتصميم وتفريد حديد برج دمشق")

# --- الحسابات الهندسية الدقيقة ---
# 1. البلاطات
h_qabo = max(15, math.ceil(L / 32)) # بلاطة القبو المصمتة
h_horidi = 30 # سماكة الهوردي المعتمدة في الأبراج للمجازات المتوسطة
h_shelter = 20 # بلاطة الملجأ (ثابت كودي)

# 2. الجوائز (مرتبطة بـ L)
h_drop = math.ceil(L / 12) # الجائز الساقط لمقاومة السهم
b_hidden = max(100, math.ceil(L / 4)) # عرض الجائز المخفي الوسطي

# 3. الأعمدة (تدرج 30xL مع تخفيض الأحمال)
# مساحة تحميل وسطية 25م2 | حمل تراكمي مخفض للقبو
p_total = 25 * 1.15 * n_floors 
col_length = max(50, math.ceil((p_total * 1000) / (0.35*250 + 0.67*0.01*4000) / 30 / 10) * 10)

# --- عرض النتائج المعتمدة في المذكرة ---
tab1, tab2 = st.tabs(["📊 المذكرة الحسابية (أبعاد)", "📐 لوحات الرسم (تسليح)"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📍 الأبعاد الخرسانية (Concrete)")
        st.info(f"• سماكة بلاطة القبو (L/32): **{h_qabo} cm**")
        st.info(f"• سماكة بلاطة الهوردي: **{h_horidi} cm**")
        st.info(f"• مقطع الجائز الساقط: **30 × {h_drop} cm**")
        st.info(f"• عرض الجائز المخفي: **{b_hidden} cm**")
    with col2:
        st.subheader("📍 تدرج الأعمدة (Columns)")
        st.warning(f"• عمود القبو: **30 × {col_length} cm**")
        st.warning(f"• عمود الطابق الخامس: **30 × {max(50, col_length-20)} cm**")
        st.warning(f"• عمود الأخير: **30 × 50 cm**")

with tab2:
    st.subheader("📐 تفريد الحديد (Shop Drawings)")
    
    # 1. تفصيل الجائز
    st.markdown("### 1️⃣ تسليح الجوائز والشابويات")
    
    st.write(f"• الحديد الإضافي العلوي (الشابوه): يمتد مسافة **{L/4:.0f} cm** من وجه المسند.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 2️⃣ أجر البطة (Base Hook)")
        
        st.write("تفصيلة تشريك العمود مع الحصيرة بعكفة L بطول 40 سم.")
    
    with col_b:
        st.markdown("### 3️⃣ مقص الدرج (Scissor Joint)")
        
        st.write("يتم تنفيذ المقص عند البسطة لمنع تشقق البيتون.")

    st.markdown("### 4️⃣ كراسي الحصيرة (Chairs)")
    
    st.write(f"ارتفاع الكراسي: **{max(90, math.ceil(L/6))-15} cm** لحمل الشبكة العلوية.")

st.divider()
st.caption("تمت المطابقة الفنية مع ملف الشرح - م. بيلان مصطفى")
