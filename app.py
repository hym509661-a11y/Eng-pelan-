import streamlit as st

# إعدادات الصفحة والختم المهني الخاص بك
st.set_page_config(page_title="مكتب المهندس بيلان مصطفى", layout="wide")
st.sidebar.markdown(f"### المهندس المدني بيلان مصطفى عبدالكريم\nدراسات-اشراف-تعهدات\n0998449697")

st.title("🏗️ نظام التصميم الإنشائي - مشروع برج دمشق")
st.info("تتم الحسابات وفق الكود العربي السوري وملحق الزلازل UBC 97")

# التبويبات الأساسية
tab1, tab2, tab3, tab4 = st.tabs(["البلاطات (Slabs)", "الجوائز (Beams)", "الأعمدة (Columns)", "الأساسات والزلازل"])

# --- 1. قسم البلاطات (Slabs) ---
with tab1:
    st.header("تصميم البلاطات")
    st.subheader("أولاً: بلاطة القبو (مصمتة Solid Slab)")
    l_max = st.number_input("أكبر مجاز للبلاطة (m)", value=5.3)
    
    # [span_1](start_span)حسب الملف: المحيط المكافئ / 140 للبلاطة باتجاهين[span_1](end_span)
    h_calc = (l_max * 100) / 35 # تقريب للمحيط المكافئ
    st.write(f"السماكة المحسوبة إنشائياً: {h_calc:.1f} cm")
    [span_2](start_span)st.success("السماكة المعتمدة في المشروع: **12 cm**[span_2](end_span)")
    
    st.subheader("ثانياً: بلاطة الملجأ")
    [span_3](start_span)st.warning("حسب توصيات وزارة الدفاع والكود السوري: السماكة المعتمدة **20 cm**[span_3](end_span)")
    [span_4](start_span)st.write("الحمولة الحية للملجأ: **20 kN/m²** (2 ton/m²)[span_4](end_span)")

    st.subheader("ثالثاً: بلاطة المتكرر (هوردي Ribbed)")
    case = st.selectbox("حالة استمرار العصب", ["بسيط (L/16)", "مستمر طرف (L/18)", "مستمر طرفين (L/20)", "ظفر (L/8)"])
    divs = {"بسيط (L/16)": 16, "مستمر طرف (L/18)": 18, "مستمر طرفين (L/20)": 20, "ظفر (L/8)": 8}
    h_rib_min = (l_max * 100) / divs[case]
    st.write(f"السماكة الدنيا حسب الحالة: {h_rib_min:.1f} cm")
    [span_5](start_span)[span_6](start_span)st.success("السماكة المعتمدة في المشروع: **30 cm** (24 بلوك + 6 تغطية)[span_5](end_span)[span_6](end_span)")

# --- 2. قسم الجوائز (Beams) ---
with tab2:
    st.header("تصميم الجوائز (ساقطة ومخفية)")
    st.subheader("الجوائز الساقطة (سقف القبو)")
    # [span_7](start_span)حسب الملف: L/14 لشرط السهم مع زيادة 10-20 سم[span_7](end_span)
    h_beam_drop = (l_max * 100 / 14) + 10
    [span_8](start_span)st.write(f"الأبعاد المعتمدة: **30x50 cm**[span_8](end_span)")
    [span_9](start_span)st.info("العرض 30 سم تم أخذه من المعماري ليتناسب مع الأعمدة[span_9](end_span)")

    st.subheader("الجوائز المخفية (الهوردي)")
    # [span_10](start_span)حسب الملف: وسطي L/4، طرفي L/6[span_10](end_span)
    b_hidden = (400 / 4) # مثال لمجاز 4 متر
    [span_11](start_span)st.write(f"العرض الأدنى للجائز المخفي الوسطي: **100 cm**[span_11](end_span)")
    [span_12](start_span)st.write(f"العرض المعتمد في المخططات: **105 cm**[span_12](end_span)")

# --- 3. قسم الأعمدة (Columns) ---
with tab3:
    st.header("تصميم الأعمدة (الشاقولية)")
    [span_13](start_span)st.write("الجملة الإنشائية: جدران قص تقاوم الزلازل + أعمدة تقاوم الأحمال الشاقولية[span_13](end_span)")
    [span_14](start_span)st.write("نسبة التسليح الدنيا المعتمدة: **1%**[span_14](end_span)")
    
    col_dim = st.selectbox("اختر الطابق", ["القبو", "الطوابق الأخيرة"])
    if col_dim == "القبو":
        [span_15](start_span)st.success("أبعاد العمود C1: **30x100 cm**[span_15](end_span)")
    else:
        [span_16](start_span)st.success("أبعاد العمود C1: **30x50 cm**[span_16](end_span)")

# --- 4. الأساسات والزلازل ---
with tab4:
    st.header("الحصيرة والزلازل")
    st.subheader("الحصيرة (Raft)")
    # [span_17](start_span)الكود السوري L/6 إلى L/8[span_17](end_span)
    h_raft_min = (5.3 * 100) / 6
    st.write(f"السماكة حسب الكود السوري: {h_raft_min:.1f} cm")
    [span_18](start_span)st.success("السماكة المعتمدة: **90 cm** (لتقليل الحديد وتحقيق الثقب)[span_18](end_span)")
    [span_19](start_span)st.write("التسليح: **7T20/m** بالاتجاهين[span_19](end_span)")

    st.subheader("المعطيات الزلزالية (دمشق)")
    [span_20](start_span)st.write("المنطقة: **2C** | التربة: **C**[span_20](end_span)")
    st.table({"المعلم": ["Ca", "Cv", "R"], "القيمة": [0.29, 0.38, 4.5]})
