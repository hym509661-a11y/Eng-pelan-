import streamlit as st
import math

# إعدادات الصفحة
st.set_page_config(page_title="برنامج المهندس بيلان الإنشائي", layout="centered")

# الترويسة والختم المهني
st.title("🏗️ نظام التصميم الإنشائي المتكامل")
st.subheader("المهندس المدني بيلان مصطفى عبدالكريم")
st.info("دراسات - إشراف - تعهدات | 📞 0998449697")

st.divider()

# منطقة المدخلات
st.sidebar.header("📥 مدخلات المشروع")
fcu = st.sidebar.number_input("المقاومة المكعبة للخرسانة fcu (MPa)", value=25)
fy = st.sidebar.number_input("إجهاد خضوع الحديد fy (MPa)", value=400)
q_soil = st.sidebar.number_input("قدرة تحمل التربة (kN/m²)", value=150)

tab1, tab2, tab3 = st.tabs(["البلاطات", "الأعمدة", "الأساسات"])

with tab1:
    st.header("📏 تصميم البلاطة (Slab)")
    L = st.number_input("طول المجاز (L) بالمتر", value=4.5)
    # حسابات الكود السوري (ممرات: 2.5 ميتة، 3 حية)
    wu = (1.4 * 2.5) + (1.7 * 3.0)
    mu = (wu * L**2) / 10
    d = 130 # لبلاطة 15 سم
    as_req = (mu * 1e6) / (0.9 * fy * 0.9 * d)
    as_min = (1.4 / fy) * 1000 * d
    final_as = max(as_req, as_min)
    
    st.success(f"التسليح السفلي المطلوب: {round(final_as)} مم²/م")
    st.caption("تم الحساب وفق معادلات جامعة دمشق والحد الأدنى للكود السوري.")

with tab2:
    st.header("🏛️ تصميم الأعمدة (Columns)")
    pu = st.number_input("الحمولة التصعيدية Pu (kN)", value=1500)
    f_prime_c = 0.8 * fcu
    # مقطع اقتصادي 1% حديد
    ag_req = (pu * 1000) / (0.65 * 0.8 * (0.85 * f_prime_c * 0.99 + fy * 0.01))
    side = math.sqrt(ag_req)
    
    st.success(f"المقطع الاقتصادي المقترح: {round(side/10)*10} x {round(side/10)*10} مم")
    st.write(f"نسبة التسليح: 1% (اقتصادية)")

with tab3:
    st.header("🧱 تصميم الأساسات (Footings)")
    p_service = st.number_input("الحمولة التشغيلية (kN)", value=1000)
    area_f = (p_service * 1.1) / q_soil
    width = math.sqrt(area_f)
    
    st.success(f"أبعاد الأساس المربع: {round(width, 2)} x {round(width, 2)} متر")

st.divider()
st.warning(f"تم التدقيق والاعتماد: {st.session_state.get('engineer', 'م. بيلان مصطفى عبدالكريم')}")
