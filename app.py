import streamlit as st
import math

# إعدادات الواجهة المهنية
st.set_page_config(page_title="مكتب المهندس بيلان - التصميم المتكامل", layout="wide")

# الهوية البصرية في الشريط الجانبي
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🏗️ المكتب الهندسي</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'><b>المهندس بيلان مصطفى عبدالكريم</b><br>0998449697</p>", unsafe_allow_html=True)
    st.markdown("---")
    n_floors = st.number_input("عدد الطوابق الإجمالي (بما فيه القبو):", value=11, min_value=1)
    L_cm = st.number_input("أكبر مجاز بين الأعمدة L (cm):", value=530)
    q_soil = st.slider("قدرة تحمل التربة (kg/cm²):", 1.0, 4.0, 2.5)
    st.markdown("---")
    st.caption("تم التطوير وفق الكود العربي السوري ومعطيات دمشق UBC97")

st.markdown("<h1 style='color: #1E3A8A;'>المنصة الذكية للتصميم ورسم التسليح</h1>", unsafe_allow_html=True)

# تبويبات النظام
tab_calc, tab_draw = st.tabs(["📊 جداول البيانات والحسابات", "📐 التفاصيل الإنشائية والرسم"])

# --- الحسابات المنطقية ---
# حساب حمل العمود التقريبي (مساحة تحميل 25 م2 * وزن 1.2 طن/م2 * عدد الطوابق)
P_ton = 25 * 1.2 * n_floors 
# أبعاد العمود (العرض ثابت 30سم كما طلبت المعماري)
# القانون: P = 0.35 * f'c * Ac + 0.67 * fy * As | مع فرض نسبة تسليح 1%
col_width = 30
col_length_req = (P_ton * 1000) / (0.35 * 250 + 0.67 * 0.01 * 4000)
col_length = max(50, math.ceil(col_length_req / 10) * 10) # تقريب لأقرب 10 سم

# الجوائز
h_drop = math.ceil((L_cm / 14 + 10) / 5) * 5
b_hidden = max(105, math.ceil((L_cm / 4) / 5) * 5)

with tab_calc:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("### 🏢 الأعمدة (Columns)")
        st.metric("بُعد عمود القبو (cm)", f"{col_width} × {col_length}")
        st.metric("بُعد عمود الأخير (cm)", "30 × 50")
        st.write(f"الحمولة التقديرية: {P_ton:.1f} Ton")

    with c2:
        st.success("### 📏 الجوائز (Beams)")
        st.write(f"**ساقط:** {col_width} × {h_drop} cm")
        st.write(f"**مخفي (عرض):** {b_hidden} cm")
        st.write(f"**سماكة الهوردي:** 30 cm")

    with c3:
        st.warning("### 🧱 الأساسات")
        if n_floors > 8:
            st.write("**الخيار المفضل:** حصيرة (Raft)")
            st.write(f"**السماكة:** {max(90, math.ceil((L_cm/6)/10)*10)} cm")
        else:
            dim_f = math.sqrt((P_ton * 1.1) / (q_soil * 10))
            st.write(f"**أساس منفرد:** {dim_f:.2f} × {dim_f:.2f} m")

with tab_draw:
    st.subheader("🎨 لوحات تفاصيل التسليح (Shop Drawings)")
    
    # 1. رسم تفصيلة الجائز والشابويات
    st.markdown("#### أولاً: تسليح الجوائز المستمرة (الشابويات)")
    st.markdown(f"""
    <div style="background-color: #f1f5f9; padding: 20px; border-radius: 15px; border-left: 10px solid #1E3A8A;">
        <div style="height: 10px; width: 30%; background: #ef4444; margin-left: auto; margin-right: auto; border-radius: 5px;"></div>
        <p style="text-align: center; color: #ef4444; font-size: 12px;">حديد إضافي علوي (شابوه) يمتد {L_cm/4:.0f} cm</p>
        <div style="height: 80px; width: 90%; border: 3px solid #1e293b; margin: 10px auto; display: flex; align-items: center; justify-content: space-between;">
            <div style="width: 5px; height: 100%; background: #1e293b;"></div>
            <div style="flex-grow: 1; border-right: 1px dashed #94a3b8; height: 80%; text-align: center; line-height: 60px;">كانات مكثفة T10@10</div>
            <div style="width: 5px; height: 100%; background: #1e293b;"></div>
        </div>
        <div style="height: 5px; width: 95%; background: #ef4444; margin: 0 auto;"></div>
        <p style="text-align: center; color: #ef4444; font-size: 12px;">حديد سفلي مستمر مع عكفة 90 درجة</p>
    </div>
    """, unsafe_allow_html=True)
    

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### ثانياً: أجر البطة (الأساسات)")
        st.markdown("""
        <div style="text-align: center; padding: 20px; border: 2px solid #3b82f6; border-radius: 10px;">
            <div style="width: 30px; height: 120px; border: 2px solid #1e293b; margin: 0 auto; position: relative;">
                <div style="position: absolute; bottom: 0; width: 80px; height: 4px; background: #ef4444; left: -25px;"></div>
                <div style="position: absolute; bottom: 0; width: 4px; height: 20px; background: #ef4444; left: -25px;"></div>
            </div>
            <p style="color: #1e3a8a;">تفصيلة أشاير العمود مع القاعدة</p>
        </div>
        """, unsafe_allow_html=True)
        

    with col_b:
        st.markdown("#### ثالثاً: مقص الدرج (Scissor Joint)")
        st.markdown("""
        <div style="text-align: center; padding: 20px; border: 2px solid #f59e0b; border-radius: 10px; height: 200px;">
            <svg width="200" height="100">
                <line x1="10" y1="80" x2="100" y2="20" style="stroke:red;stroke-width:4" />
                <line x1="100" y1="20" x2="190" y2="20" style="stroke:red;stroke-width:4" />
                <line x1="10" y1="60" x2="110" y2="60" style="stroke:blue;stroke-width:3" />
                <line x1="110" y1="60" x2="190" y2="10" style="stroke:blue;stroke-width:3" />
            </svg>
            <p style="color: #1e3a8a;">تداخل الحديد (المقص) عند البسطة</p>
        </div>
        """, unsafe_allow_html=True)
        

st.markdown("---")
st.markdown(f"**ملاحظة مكتبية:** أبعاد الأعمدة {col_width}×{col_length} سم للقبو هي أبعاد اقتصادية تحقق متطلبات الكود السوري لمبنى من {n_floors} طابقاً.")
