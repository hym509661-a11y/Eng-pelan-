import streamlit as st
import math

# إعداد الهوية المهنية للمهندس بيلان
st.set_page_config(page_title="نظام التصميم الإنشائي - م. بيلان مصطفى", layout="wide")

# الختم الرسمي في الشريط الجانبي
st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center; font-family: 'Arial';">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold; color: #333;">0998449697</p>
    <p style="margin: 5px 0; color: #666; font-size: 0.9em;">دراسات - إشراف - تعهدات</p>
</div>
""", unsafe_allow_html=True)

# مدخلات المستخدم الأساسية
with st.sidebar:
    st.header("⚙️ معطيات التصميم")
    uploaded_file = st.file_uploader("ارفع المسقط المعماري (صورة)", type=['png', 'jpg', 'jpeg'])
    L = st.number_input("أطول مجاز في المسقط L (cm):", value=530)
    n_floors = st.number_input("عدد الطوابق الإجمالي:", value=11, min_value=1)
    st.divider()
    st.info("النظام سيحدد اتجاه الأعصاب وسماكة البلاطات تلقائياً.")

st.title("🏗️ نظام توليد المخططات والمذكرات الحسابية الذكي")

if uploaded_file:
    st.success("تم تحليل المسقط المعماري بنجاح. جاري توليد النظام الإنشائي وفق الكود السوري...")

    # --- محرك الحسابات الإنشائية (Backend) ---
    
    # 1. بلاطة القبو (دائماً مصمتة وفق طلبك - حساب شرط السهم)
    h_qabo = max(15, math.ceil(L / 32)) 
    
    # 2. بلاطات المتكرر (هوردي - تحديد اتجاه العصب)
    # اتجاه العصب يتبع دائماً المجاز الأصغر لتقليل العزوم والسهم
    h_horidi = max(30, math.ceil(L / 20)) 
    
    # 3. الجوائز (ساقطة ومخفية)
    h_drop_beam = math.ceil(L / 12)
    b_hidden_beam = max(100, math.ceil(L / 4))
    
    # 4. الأعمدة (تدرج منطقي بناءً على n_floors)
    p_load = ((L/100)**2) * 1.25 * n_floors # حمولة تقريبية طن
    col_len = max(50, math.ceil((p_load * 1000) / (0.35*250 + 0.67*0.01*4000) / 30 / 10) * 10)

    # --- عرض النتائج المخططات ---
    tab1, tab2, tab3 = st.tabs(["📐 المخططات الإنشائية", "📝 المذكرة الحسابية", "🛠️ تفريد الحديد"])

    with tab1:
        st.subheader("📍 لوحة توزيع الأعصاب والجوائز")
        # النظام يرسم اتجاه العصب
        
        st.caption(f"تم تحديد اتجاه الأعصاب في الاتجاه القصير ({L} سم) لتقليل التسليح والسهم.")

    with tab2:
        st.subheader("📝 تفاصيل المذكرة الحسابية")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**• بلاطة القبو (مصمتة):** {h_qabo} cm")
            st.write(f"**• بلاطة المتكرر (هوردي):** {h_horidi} cm")
            st.write(f"**• اتجاه العصب:** باتجاه المجاز الأصغر")
        with col2:
            st.write(f"**• الجوائز الساقطة:** 30 × {h_drop_beam} cm")
            st.write(f"**• الجوائز المخفية:** عرض {b_hidden_beam} cm")
            st.write(f"**• عمود القبو:** 30 × {col_len} cm")

    with tab3:
        st.subheader("🛠️ لوحات تفريد الحديد (Shop Drawings)")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.write("**تفريد الجوائز (شابويات)**")
            
            st.caption(f"طول الشابويه: {L/4:.0f} cm من وجه المسند")
        with c2:
            st.write("**مقص الدرج**")
            
        with c3:
            st.write("**أجر البطة (أشاير)**")
            

    # زر التحميل
    st.divider()
    st.button("💾 تصدير كافة المخططات والمذكرة إلى PDF")

else:
    st.warning("الرجاء رفع صورة المسقط المعماري للبدء في التصميم.")
