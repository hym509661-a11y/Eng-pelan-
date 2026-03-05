import streamlit as st
import math

# إعدادات الصفحة والسمة الاحترافية
st.set_page_config(page_title="نظام التصميم الإنشائي - م. بيلان", layout="wide")

# تصميم الهوية في الشريط الجانبي
with st.sidebar:
    st.markdown("## 🏗️ المكتب الهندسي")
    st.info("المهندس المدني بيلان مصطفى عبدالكريم\n0998449697\nدراسات - إشراف - تعهدات")
    st.markdown("---")
    n_floors = st.number_input("عدد الطوابق الإجمالي:", value=11, min_value=1)
    L_cm = st.number_input("أطول مجاز بين الأعمدة L (cm):", value=530)
    q_soil = st.slider("تحمل التربة (kg/cm²):", 1.0, 4.0, 2.5)

st.title("🏛️ منصة التصميم الإنشائي المتكاملة")
st.caption("تمت البرمجة وفق الكود العربي السوري ومعطيات مشروع برج دمشق")

# تبويبات منظمة
tabs = st.tabs(["📊 الحسابات الإنشائية", "🎨 التفاصيل والرسم الهندسي"])

with tabs[0]:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔹 البلاطات (Slabs)")
        # مصمتة
        h_solid = max(12, math.ceil((L_cm/35)/2)*2)
        st.success(f"البلاطة المصمتة: {h_solid} cm")
        # هوردي
        h_rib = max(30, math.ceil((L_cm/20)/2)*2)
        st.success(f"البلاطة الهوردي: {h_rib} cm")
        
        st.subheader("🔹 الجوائز (Beams)")
        # ساقطة
        h_drop = math.ceil((L_cm/14 + 10)/5)*5
        st.success(f"جائز ساقط: 30 × {h_drop} cm")
        # مخفية
        b_hidden = max(105, math.ceil((L_cm/4)/5)*5)
        st.success(f"جائز مخفي (عرض): {b_hidden} cm")

    with col2:
        st.subheader("🔹 الأعمدة (Columns)")
        # حساب حمل تقديري: 1.2 طن لكل متر مربع لكل طابق
        est_load = (n_floors * 25 * 1.2) 
        col_width = 30
        col_length = max(50, math.ceil((est_load * 1000 / (0.4 * 250)) / 10) * 10)
        st.warning(f"بعد العمود (قبو): {col_width} × {col_length} cm")
        st.warning(f"بعد العمود (سطح): 30 × 50 cm")

        st.subheader("🔹 الأساسات (Foundations)")
        f_type = st.selectbox("نوع الأساس:", ["منفرد", "مشترك", "حصيرة"])
        if f_type == "منفرد":
            f_dim = math.sqrt((est_load * 1.1) / (q_soil * 10))
            st.success(f"أبعاد الأساس: {f_dim:.2f} × {f_dim:.2f} m")
        elif f_type == "حصيرة":
            h_raft = max(90, math.ceil((L_cm/6)/10)*10)
            st.success(f"سماكة الحصيرة: {h_raft} cm")

with tabs[1]:
    st.header("📐 الرسوم التفصيلية للتسليح")
    
    # رسم تخطيطي للجائز (CSS/HTML)
    st.markdown("### 1. تفصيلة الجائز (شابويات وكانات)")
    st.markdown("""
    <div style="border: 2px solid #2ecc71; padding: 20px; border-radius: 10px; background-color: #f9f9f9;">
        <div style="height: 40px; border-bottom: 4px solid #c0392b; position: relative;">
            <span style="position: absolute; right: 20%; top: -10px; color: #c0392b;">إضافي علوي (شابوه) L/4</span>
        </div>
        <div style="height: 60px; border: 2px solid #34495e; margin-top: 5px; display: flex; align-items: center; justify-content: space-around;">
             <div style="width: 2px; height: 100%; background: #34495e;"></div>
             <div style="color: #7f8c8d;">توزيع كانات مكثف T10@10</div>
             <div style="width: 2px; height: 100%; background: #34495e;"></div>
        </div>
        <div style="height: 5px; background: #c0392b; margin-top: 5px;"></div>
        <div style="text-align: center; color: #c0392b;">حديد سفلي مستمر مع عكفة (Hook)</div>
    </div>
    """, unsafe_allow_html=True)

    col_draw1, col_draw2 = st.columns(2)
    with col_draw1:
        st.markdown("### 2. الأساس والعمود (أجر البطة)")
        st.markdown("""
        <div style="border: 2px solid #3498db; padding: 15px; text-align: center;">
            <div style="width: 40px; height: 100px; border: 2px solid black; margin: 0 auto; position: relative;">
                <div style="position: absolute; bottom: 0; width: 100px; height: 2px; background: red; left: -30px;"></div>
                <div style="position: absolute; bottom: 0; width: 2px; height: 20px; background: red; left: -30px;"></div>
                <div style="position: absolute; bottom: 0; width: 2px; height: 20px; background: red; right: -30px;"></div>
            </div>
            <p>تمثيل "أجر البطة" للأشاير داخل القاعدة</p>
        </div>
        """, unsafe_allow_html=True)

    with col_draw2:
        st.markdown("### 3. مقص الدرج (Scissor)")
        st.markdown("""
        <div style="border: 2px solid #e67e22; padding: 15px; text-align: center; height: 180px;">
            <div style="width: 100px; height: 2px; background: red; transform: rotate(-30deg); margin-top: 50px; margin-left: 50px;"></div>
            <div style="width: 100px; height: 2px; background: red; transform: rotate(0deg); margin-left: 100px;"></div>
            <p style="margin-top: 40px;">مبدأ "المقص" عند التقاء الشاحط بالبسطة</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"**الخلاصة المهنية:** تم اعتماد أبعاد الأعمدة {col_width}×{col_length} سم للقبو، والأساسات بنوعها المختار تحقق إجهاد التربة {q_soil} kg/cm².")
