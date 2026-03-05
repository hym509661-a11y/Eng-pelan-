import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="مشروع برج دمشق - م. بيلان", layout="wide")

# العنوان الجانبي
st.sidebar.title("المكتب الهندسي")
st.sidebar.markdown("### المهندس بيلان مصطفى")
st.sidebar.info("دراسة برج سكني 11 طابق - دمشق")

st.title("🏗️ حاسبة التصميم الإنشائي الذكية")

# تقسيم الشاشة إلى تبويبات حسب التقرير
tab1, tab2, tab3, tab4 = st.tabs(["البلاطات والملجأ", "بلاطة الهوردي", "الأساسات (الحصيرة)", "التحليل الزلزالي"])

# --- 1. بلاطة القبو والملجأ ---
with tab1:
    st.header("دراسة بلاطة سقف القبو")
    is_shelter = st.checkbox("هل المنطقة المختارة هي 'الملجأ'؟")
    
    L = st.number_input("أدخل طول أكبر مجاز (m):", value=5.3, min_value=1.0)
    
    if is_shelter:
        [span_1](start_span)st.warning("⚠️ شروط الملجأ (وزارة الدفاع): السماكة لا تقل عن 20 سم والحمولة 20kN/m²")[span_1](end_span)
        h = 20 # الحد الأدنى للملجأ
        live_load = 20
    else:
        h = 12 # بلاطة القبو العادي المصمتة
        live_load = 3 # ممرات
    
    st.success(f"السماكة المقترحة: {h} cm")
    [span_2](start_span)st.write(f"الحمولة الحية المعتمدة: {live_load} kN/m²")[span_2](end_span)

# --- 2. بلاطة الطابق المتكرر (الهوردي) ---
with tab2:
    st.header("بلاطة هوردي (Ribbed Slab)")
    l_rib = st.number_input("طول العصب (m):", value=5.3, key="rib_l")
    [span_3](start_span)st_case = st.selectbox("حالة الاستناد:", ["بسيط (L/16)", "مستمر من طرف (L/18)", "مستمر من طرفين (L/20)", "ظفر (L/8)"])[span_3](end_span)
    
    divisors = {"بسيط (L/16)": 16, "مستمر من طرف (L/18)": 18, "مستمر من طرفين (L/20)": 20, "ظفر (L/8)": 8}
    h_min = (l_rib * 100) / divisors[st_case]
    
    st.info(f"السماكة الإنشائية الدنيا المطلوبة: {h_min:.2f} cm")
    [span_4](start_span)[span_5](start_span)st.write("تم اعتماد سماكة **30 cm** للمشروع لتحقيق كافة الشروط.")[span_4](end_span)[span_5](end_span)

# --- 3. الأساسات (الحصيرة) ---
with tab3:
    st.header("تصميم الحصيرة")
    l_raft = st.number_input("أكبر مجاز في الحصيرة (m):", value=5.3, key="raft_l")
    
    # الكود السوري L/6 إلى L/8
    [span_6](start_span)h_syrian = (l_raft * 100) / 6[span_6](end_span)
    st.write(f"السماكة حسب الكود السوري (L/6): {h_syrian:.1f} cm")
    [span_7](start_span)st.success("تم اعتماد سماكة **90 cm** في المشروع لتقليل نسبة التسليح.")[span_7](end_span)
    [span_8](start_span)st.write("التسليح المعتمد: 7T20 لكل متر طولي بالاتجاهين.")[span_8](end_span)

# --- 4. التحليل الزلزالي (دمشق) ---
with tab4:
    st.header("المعطيات الزلزالية (دمشق)")
    [span_9](start_span)st.write("• المنطقة الزلزالية: **2C**")[span_9](end_span)
    [span_10](start_span)st.write("• معامل التسارع الزلزالي: **0.25**")[span_10](end_span)
    soil = st.selectbox("نوع التربة:", ["C (صلبة)", "D", "E"])
    
    ca = 0.29 if soil.startswith("C") else 0.32
    [span_11](start_span)cv = 0.38 if soil.startswith("C") else 0.44[span_11](end_span)
    
    [span_12](start_span)st.table({"المعلم": ["Ca", "Cv", "R (جدران قص)"], "القيمة": [ca, cv, 4.5]})[span_12](end_span)

st.divider()
st.caption("برمجية تفاعلية لمشروع الدكتور فادي نقرش - المهندس بيلان مصطفى")
