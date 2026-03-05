import streamlit as st
import math

# إعدادات الصفحة والختم المهني
st.set_page_config(page_title="مكتب المهندس بيلان - برج دمشق", layout="wide")

# الختم الخاص بك (دراسات-اشراف-تعهدات)
st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 10px; border-radius: 10px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold; color: #ef4444;">0998449697</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ معطيات التصميم (المتغيرة)")
    L = st.number_input("طول أكبر مجاز L (cm):", value=530, step=10)
    n_floors = st.slider("عدد الطوابق الإجمالي:", 1, 15, 11)
    st.divider()
    st.info("الحسابات مرتبطة ديناميكياً بالمجاز L")

st.title("🏗️ النظام الإنشائي المتكامل (نسخة برج دمشق)")

# --- 1. حسابات البلاطات (مرتبطة بـ L) ---
# بلاطة القبو (مصمتة): المحيط / 140 أو L/35 حسب الملف
h_solid = max(12, math.ceil((L / 35))) 
# بلاطة الهوردي: L/20 للمستمر من طرفين
h_ribbed = max(30, math.ceil((L / 20)))

# --- 2. حسابات الجوائز (مرتبطة بـ L) ---
# ساقطة (L/14) + 10سم أمان كما في الملف
h_drop = math.ceil((L / 14) + 10)
# مخفية (عرض L/4 للوسطي)
b_hidden = max(105, math.ceil(L / 4))

# --- 3. حسابات الأعمدة (واقعية ومرتبطة بـ L و n) ---
# حمولة تقديرية: مساحة تحميل (L*L) * وزن طابقي 1.2 طن * عدد طوابق
load_area = (L/100) * (L/100)
p_total = load_area * 1.2 * n_floors
# المقطع (العرض ثابت 30): الطول = الحمل / (إجهاد البيتون والحديد)
col_len = max(50, math.ceil((p_total * 1000) / (0.35 * 250 + 0.67 * 0.01 * 4000) / 30 / 10) * 10)

# --- عرض النتائج ---
tab1, tab2 = st.tabs(["📊 جداول الأبعاد والحديد", "📐 لوحات الرسم الإنشائي"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📍 الأبعاد البيتونية (مرتبطة بـ L)")
        st.write(f"• **سماكة بلاطة القبو (L/35):** {h_solid} cm")
        st.write(f"• **ارتفاع الجائز الساقط (L/14+10):** {h_drop} cm")
        st.write(f"• **عرض الجائز المخفي (L/4):** {b_hidden} cm")
        st.write(f"• **بعد عمود القبو (30xL):** 30 × {col_len} cm")
    
    with c2:
        st.subheader("📍 حسابات التسليح (T16/T14)")
        # حسابات تقريبية لعدد القضبان
        n_bars_col = math.ceil((0.01 * 30 * col_len) / 2.01) * 2 # T16
        st.write(f"• **تسليح العمود:** {n_bars_col} T 16")
        st.write(f"• **حديد الجائز السفلي:** 4 T 16")
        st.write(f"• **حديد الشابويات (إضافي علوي):** 3 T 16")

with tab2:
    st.subheader("📐 الرسم الهندسي التفصيلي")
    
    st.markdown("### 1. تسليح الجائز (شابويات وكانات)")
    
    st.write(f"الشابويات تمتد مسافة {L/4:.0f} cm من وجه العمود.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 2. أجر البطة (Base Hook)")
        
        st.write("ثني الأشاير داخل القاعدة (أجر البطة) بطول 40 سم.")

    with col_b:
        st.markdown("### 3. مقص الدرج (Scissor)")
        
        st.write(f"سماكة الشاحط (L_stair/20): 15 cm")

    st.markdown("### 4. كراسي الحصيرة (Chairs)")
    
    st.write(f"ارتفاع الكرسي: {max(90, math.ceil(L/6))-15} cm")

st.divider()
st.caption(f"تم ربط كافة الحسابات بالمجاز {L} cm وفق دراسة الدكتور فادي نقرش")
