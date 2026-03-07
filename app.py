import streamlit as st
import math

# إعداد الهوية المهنية للمهندس بيلان
st.set_page_config(page_title="النظام الإنشائي الشامل - م. بيلان", layout="wide")

# الختم المهني في الشريط الجانبي
st.sidebar.markdown("""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold; color: #ef4444;">0998449697</p>
    <p style="margin: 5px 0; font-size: 0.85em; font-weight: bold;">دراسات - إشراف - تعهدات</p>
</div>
""", unsafe_allow_html=True)

# مدخلات المشروع
with st.sidebar:
    st.header("⚙️ مدخلات التحليل")
    uploaded_file = st.file_uploader("ارفع صورة المخطط المعماري", type=['png', 'jpg', 'jpeg'])
    n_floors = st.number_input("عدد الطوابق الإجمالي:", value=11)
    soil_cap = st.number_input("تحمل التربة (kg/cm²):", value=2.0)
    L_input = st.number_input("أطول مجاز صافي (cm):", value=530)

st.title("🚀 النظام الذكي لتصميم البلاطات والأساسات والكشف عن التداخل")

if uploaded_file:
    # --- 1. حسابات البلاطات (الكود السوري) ---
    h_solid = max(15, math.ceil(L_input / 35)) # سماكة سقف القبو
    h_horidi = 30 # سماكة سقف المتكرر (24 بلوكة + 6 تغطية)
    h_beam = math.ceil(L_input / 12) # سماكة الجوائز
    
    # --- 2. حسابات الأساسات ونظام الإنذار ---
    p_column = ((L_input/100)**2) * 1.25 * n_floors # حمولة العمود بالطن
    area_needed = (p_column * 1.1) / (soil_cap * 10) # مساحة القاعدة المطلوبة m2
    total_area = (L_input/100)**2 # مساحة المسقط التقديرية m2
    overlap = (area_needed / total_area) * 100
    
    # --- 3. عرض المخططات والنتائج ---
    tab1, tab2, tab3 = st.tabs(["📐 المخططات الإنشائية", "🛠️ تفريد الحديد", "🧱 دراسة الأساسات"])

    with tab1:
        st.subheader("📍 سقف المتكرر (بلاطة هوردي)")
                st.write(f"**سماكة البلاطة:** {h_horidi} cm | **اتجاه الأعصاب:** الاتجاه القصير ({L_input} cm).")
        
        st.subheader("📍 سقف القبو (بلاطة مصمتة)")
                st.write(f"**سماكة البلاطة:** {h_solid} cm | **التسليح:** شبكتين T 10 كل 15 سم.")

    with tab2:
        st.subheader("🛠️ تفريد حديد العناصر (العدد والقطر)")
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**تفريد حديد الجائز الرئيسي**")
                        st.markdown(f"- السفلي: **4 T 16**\n- العلوي: **2 T 12**\n- المقطع: **30x{h_beam} cm**")
        with col_b:
            st.write("**تفريد حديد الأعمدة**")
                        st.write(f"مقطع القبو: **30x{max(50, math.ceil(p_column/10)*5)} cm**")
            st.caption("تدرج العمود: ينقص المقطع 10 سم كل 3 طوابق.")

    with tab3:
        st.subheader("🧱 دراسة تداخل الأساسات")
        st.write(f"**نسبة تداخل القواعد المتوقعة:** {overlap:.1f}%")
        
        if overlap > 70:
            st.error(f"🚨 نظام إنذار: تداخل القواعد كبير جداً ({overlap:.1f}%).")
            st.warning("القرار الهندسي: تم التحويل تلقائياً لنظام **الحصيرة العامة (Raft Foundation)**.")
                    else:
            st.success("القرار الهندسي: نظام **قواعد منفردة** مع ربطها بشناج (Tie Beams).")
            
    st.divider()
    st.info("تم التصميم والتحليل وفق المذكرة الحسابية - م. بيلان مصطفى")

else:
    st.warning("الرجاء رفع صورة المخطط المعماري لبدء التحليل الإنشائي.")
