import streamlit as st

# إعداد الصفحة الأساسية
st.set_page_config(page_title="مشروع برج دمشق - م. بيلان", layout="wide")

# تصميم الشريط الجانبي للهوية الشخصية
st.sidebar.markdown("### 🏢 المكتب الهندسي")
st.sidebar.info("المهندس بيلان مصطفى عبدالكريم\nدراسة مشروع دمشق (11 طابق)")

st.title("🏗️ حاسبة المعايير الإنشائية التفاعلية")
st.markdown("---")

# تبويبات لتنظيم واجهة المستخدم
tab1, tab2, tab3, tab4 = st.tabs(["البلاطات والملجأ", "بلاطة الهوردي", "الأساسات (الحصيرة)", "التحليل الزلزالي"])

# --- 1. بلاطة القبو والملجأ ---
with tab1:
    st.header("دراسة بلاطة سقف القبو")
    is_shelter = st.checkbox("تحديد المنطقة كـ 'ملجأ'")
    
    L_qabo = st.number_input("أدخل طول المجاز (m):", value=5.3, step=0.1, key="q_l")
    
    if is_shelter:
        st.warning("⚠️ شروط الملجأ: السماكة الدنيا 20 cm والحمولة الحية 20 kN/m²")
        h_val = 20
        load_val = 20
    else:
        st.info("بلاطة مصمتة عاملة باتجاهين (قبو عادي)")
        h_val = 12
        load_val = 3
    
    st.success(f"النتيجة: السماكة المقترحة {h_val} cm | الحمولة الحية {load_val} kN/m²")

# --- 2. بلاطة المتكرر (الهوردي) ---
with tab2:
    st.header("بلاطة الهوردي (Ribbed Slab)")
    l_rib = st.number_input("طول مجاز العصب (m):", value=5.3, step=0.1, key="r_l")
    st_case = st.selectbox("حالة الاستمرار:", ["بسيط (L/16)", "مستمر من طرف (L/18)", "مستمر من طرفين (L/20)", "ظفر (L/8)"])
    
    div_map = {"بسيط (L/16)": 16, "مستمر من طرف (L/18)": 18, "مستمر من طرفين (L/20)": 20, "ظفر (L/8)": 8}
    h_min = (l_rib * 100) / div_map[st_case]
    
    st.write(f"السماكة الإنشائية المطلوبة: **{h_min:.1f} cm**")
    st.write("📌 تم اعتماد سماكة **30 cm** للمشروع لتحقيق شروط السهم.")

# --- 3. الأساسات (الحصيرة) ---
with tab3:
    st.header("تصميم الحصيرة (Raft)")
    l_raft = st.number_input("أكبر مجاز في الحصيرة (m):", value=5.3, step=0.1, key="f_l")
    
    h_syr = (l_raft * 100) / 6
    st.write(f"السماكة حسب الكود السوري (L/6): **{h_syr:.1f} cm**")
    st.success("الخيار المعتمد: سماكة **90 cm** لتقليل الحاجة للحديد وتحقيق الثقب.")

# --- 4. التحليل الزلزالي (دمشق) ---
with tab4:
    st.header("معطيات UBC 97 لمدينة دمشق")
    soil = st.selectbox("نوع التربة (حسب التقرير الجيوتكنيكي):", ["C (صلبة)", "D", "E"])
    
    # المعطيات ثابتة لدمشق (المنطقة 2C) وفق ملفك
    ca_val = 0.29 if "C" in soil else 0.32
    cv_val = 0.38 if "C" in soil else 0.44
    
    col1, col2 = st.columns(2)
    col1.metric("معامل Ca", ca_val)
    col2.metric("معامل Cv", cv_val)
    st.write("معامل الاستجابة الزلزالية (R) لجدران القص: **4.5**")

st.markdown("---")
st.caption("تمت البرمجة بناءً على دراسة مشروع الدكتور فادي نقرش | إعداد المهندس بيلان")
