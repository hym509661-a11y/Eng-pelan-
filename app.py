import streamlit as st
import math

# إعداد واجهة المكتب الهندسي
st.set_page_config(page_title="مكتب المهندس بيلان مصطفى", layout="wide")
st.sidebar.markdown("### 🏗️ المهندس بيلان مصطفى عبدالكريم\nدراسات - إشراف - تعهدات\n0998449697")

st.title("نظام التصميم الإنشائي المتكامل - مشروع برج دمشق (11 طابق)")
st.markdown("---")

# تبويبات المشروع
tabs = st.tabs(["البلاطات (Slabs)", "الجوائز (Beams)", "الأعمدة (Columns)", "الأساسات والزلازل"])

# --- 1. قسم البلاطات ---
with tabs[0]:
    st.header("دراسة البلاطات")
    l_max = st.number_input("طول أكبر مجاز L (cm):", value=530)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("سقف القبو (مصمتة)")
        # [span_0](start_span)حسب التقرير: المحيط المكافئ / 140[span_0](end_span)
        h_solid = l_max / 35 # تقريب للمحيط المكافئ
        st.write(f"• السماكة المحسوبة: {h_solid:.1f} cm")
        [span_1](start_span)st.success("• السماكة المعتمدة: 12 cm[span_1](end_span)")
        
        st.subheader("الملجأ")
        [span_2](start_span)st.warning("• السماكة المعتمدة: 20 cm (توصيات الدفاع)[span_2](end_span)")
        [span_3](start_span)st.write("• الحمولة الحية: 20 kN/m²[span_3](end_span)")

    with col2:
        st.subheader("المتكرر (هوردي)")
        case = st.selectbox("حالة الاستناد للعصب:", ["بسيط (L/16)", "مستمر طرف (L/18)", "مستمر طرفين (L/20)", "ظفر (L/8)"])
        divs = {"بسيط (L/16)": 16, "مستمر طرف (L/18)": 18, "مستمر طرفين (L/20)": 20, "ظفر (L/8)": 8}
        h_rib = l_max / divs[case]
        [span_4](start_span)[span_5](start_span)st.write(f"• السماكة الدنيا المطلوبة: {h_rib:.1f} cm[span_4](end_span)[span_5](end_span)")
        [span_6](start_span)[span_7](start_span)st.success("• السماكة المعتمدة: 30 cm (24 بلوك + 6 تغطية)[span_6](end_span)[span_7](end_span)")

# --- 2. قسم الجوائز ---
with tabs[1]:
    st.header("دراسة الجوائز (Beams)")
    
    st.subheader("الجوائز الساقطة (سقف القبو)")
    [span_8](start_span)h_drop = l_max / 14 # شرط السهم L/14[span_8](end_span)
    st.write(f"• الارتفاع المطلوب (L/14): {h_drop:.1f} cm")
    [span_9](start_span)st.success("• الأبعاد المعتمدة: 30x50 cm (زيادة 10سم للأمان)[span_9](end_span)")
    
    st.subheader("الجوائز المخفية (Hidden Beams)")
    [span_10](start_span)b_hidden = l_max / 4 # الجائز الوسطي L/4[span_10](end_span)
    st.write(f"• العرض المطلوب للجائز الوسطي: {b_hidden:.1f} cm")
    [span_11](start_span)st.success("• العرض المعتمد في المخطط: 105 cm[span_11](end_span)")

# --- 3. قسم الأعمدة ---
with tabs[2]:
    st.header("تدرج أبعاد الأعمدة (Columns)")
    [span_12](start_span)st.info("نسبة التسليح الدنيا المعتمدة: 1%[span_12](end_span)")
    
    col_data = {
        "الطابق": ["القبو", "السطح الأخير"],
        "الأبعاد (cm)": ["30x100", "30x50"],
        "نسبة التسليح": ["1%", "1%"]
    }
    [span_13](start_span)st.table(col_data) #[span_13](end_span)

# --- 4. الأساسات والزلازل ---
with tabs[3]:
    st.header("الحصيرة والتحليل الزلزالي")
    
    st.subheader("الحصيرة (Raft)")
    [span_14](start_span)st.write(f"• السماكة حسب الكود السوري (L/6): {(l_max/6):.1f} cm[span_14](end_span)")
    [span_15](start_span)st.success("• السماكة المعتمدة: 90 cm (لتقليل الحديد وتحقيق الثقب)[span_15](end_span)")
    [span_16](start_span)[span_17](start_span)st.write("• التسليح: 7 T 20 بالاتجاهين[span_16](end_span)[span_17](end_span)")
    
    st.subheader("معطيات دمشق (UBC 97)")
    [span_18](start_span)st.write("• المنطقة: 2C | التسارع: 0.25[span_18](end_span)")
    [span_19](start_span)st.write("• التربة: C | Ca=0.29 | Cv=0.38[span_19](end_span)")
    [span_20](start_span)st.write("• معامل الاستجابة R (جدران قص): 4.5[span_20](end_span)")

st.divider()
st.caption("تمت البرمجة وفق دراسة الدكتور فادي نقرش - إعداد م. بيلان")
