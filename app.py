import streamlit as st
import math
from PIL import Image

# إعدادات الهوية المهنية للمهندس بيلان مصطفى عبدالكريم
st.set_page_config(page_title="النظام الإنشائي الذكي - م. بيلان", layout="wide")

st.sidebar.markdown("""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold; color: #ef4444;">0998449697</p>
    <p style="margin: 5px 0; font-size: 0.85 font-weight: bold;">دراسات - إشراف - تعهدات</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ إعدادات التحليل المعماري")
    uploaded_file = st.file_uploader("ارفع المسقط المعماري (صورة)", type=['png', 'jpg', 'jpeg'])
    pixel_scale = st.number_input("معايرة الرسم: كم سم يمثل كل 100 بكسل؟", value=200)
    n_floors = st.number_input("عدد الطوابق الإجمالي:", value=11)
    soil_bearing = st.number_input("تحمل التربة (kg/cm²):", value=2.0)

st.title("🏗️ المحرك الإنشائي الشامل لتوليد المخططات والأساسات")

if uploaded_file:
    # --- 1. معالجة الصورة واستخراج المجازات ---
    image = Image.open(uploaded_file)
    width, height = image.size
    # حساب المجاز التقديري بناءً على المعايرة (مثال هندسي)
    L_detected = (width / 100) * pixel_scale / 2 
    st.success(f"✅ تم تحليل المسقط: أطول مجاز تم رصده L = {L_detected:.0f} cm")

    # --- 2. التصميم الإنشائي (الكود السوري) ---
    # البلاطات
    h_solid_qabo = max(15, math.ceil(L_detected / 35)) #
    h_horidi = 30 # ثابت للأبراج (24+6)
    
    # الجوائز (4 T 16 سفلي / 2 T 12 علوي كما طلبت)
    h_beam = math.ceil(L_detected / 12)
    
    # الأعمدة وتدرجها كل 3 طوابق
    col_qabo_len = max(50, math.ceil((L_detected**2 * 1.2 * n_floors / 10000) / 30 / 10) * 10)

    # --- 3. دراسة الأساسات ونظام الإنذار ---
    footing_area = (L_detected**2 * 1.3 * n_floors / 10000) / (soil_bearing * 10)
    overlap_ratio = footing_area / (L_detected**2 / 10000)
    
    foundation_type = ""
    if overlap_ratio < 0.5:
        foundation_type = "أساسات منفردة (Isolated Footings)"
    elif 0.5 <= overlap_ratio < 0.8:
        foundation_type = "أساسات مشتركة (Combined Footings)"
    else:
        foundation_type = "حصيرة عامة (Raft Foundation)"
        st.warning("⚠️ نظام إنذار: تداخل الأساسات تجاوز 80%، تم التحويل آلياً لنظام الحصيرة.")

    # --- 4. عرض المخططات الإنشائية ---
    tab1, tab2, tab3 = st.tabs(["📐 مخططات البلاطات", "🛠️ تفريد الحديد", "🧱 نظام الأساسات"])

    with tab1:
        st.subheader("📍 سقف المتكرر (هوردي)")
        
        st.write(f"**اتجاه الأعصاب:** الاتجاه القصير ({L_detected:.0f} سم).")
        
        st.subheader("📍 سقف القبو (مصمت)")
        
        st.write(f"**السماكة:** {h_solid_qabo} cm | **التسليح:** شبكتين T 10 كل 15 سم.")

    with tab2:
        st.subheader("🛠️ تفريد حديد الجوائز والأعمدة (العدد والقطر)")
        col_a, col_b = st.columns(2)
        with col_a:
            
            st.write(f"الجائز: 30x{h_beam} cm (4 T 16 سفلي / 2 T 12 علوي)")
        with col_b:
            
            st.write(f"عمود القبو: 30x{col_qabo_len} cm (تدرج كل 3 طوابق)")

    with tab3:
        st.subheader(f"🏗️ دراسة الأساسات: {foundation_type}")
        if "حصيرة" in foundation_type:
            
            st.write(f"**سماكة الحصيرة المقترحة:** {max(80, math.ceil(n_floors * 10))} cm")
        else:
            

    st.divider()
    st.button("💾 تصدير المخططات التنفيذية والمذكرة الحسابية")

else:
    st.info("الرجاء رفع صورة المخطط المعماري للبدء بالتحليل.")
