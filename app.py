import streamlit as st
import math

# إعدادات الصفحة وهوية المكتب
st.set_page_config(page_title="برج دمشق - م. بيلان", layout="wide")
st.sidebar.markdown("### 🏗️ المهندس المدني")
st.sidebar.info("بيلان مصطفى عبدالكريم\nدراسات - إشراف - تعهدات\n0998449697")

st.title("نظام الحسابات الإنشائية التفاعلي")
st.markdown("---")

# تبويبات المشروع
tab1, tab2, tab3 = st.tabs(["البلاطات", "الجوائز", "الأعمدة والأساسات"])

# --- 1. قسم البلاطات ---
with tab1:
    st.header("تصميم البلاطات")
    l_input = st.number_input("أدخل طول المجاز L (cm):", value=530, step=10)
    
    # حساب بلاطة القبو (المحيط المكافئ / 140)
    h_qabo_min = l_input / 35
    # جعل القيمة المعتمدة تتغير (أقرب رقم زوجي أكبر من المحسوب)
    h_qabo_final = max(12, math.ceil(h_qabo_min / 2) * 2)
    
    st.subheader("سقف القبو (مصمتة)")
    st.write(f"• السماكة الدنيا المحسوبة: {h_qabo_min:.1f} cm")
    [span_0](start_span)st.success(f"• السماكة المعتمدة ديناميكياً: {h_qabo_final} cm")[span_0](end_span)

    # بلاطة الهوردي
    st.subheader("بلاطة المتكرر (هوردي)")
    case = st.selectbox("حالة استمرار العصب:", ["مستمرة طرفين (L/20)", "مستمرة طرف (L/18)", "بسيطة (L/16)", "ظفر (L/8)"])
    divs = {"مستمرة طرفين (L/20)": 20, "مستمرة طرف (L/18)": 18, "بسيطة (L/16)": 16, "ظفر (L/8)": 8}
    
    h_rib_min = l_input / divs[case]
    h_rib_final = max(30, math.ceil(h_rib_min / 2) * 2) # الحد الأدنى 30 سم حسب المشروع
    
    st.write(f"• السماكة الدنيا المطلوبة: {h_rib_min:.1f} cm")
    [span_1](start_span)st.success(f"• السماكة المعتمدة ديناميكياً: {h_rib_final} cm")[span_1](end_span)

# --- 2. قسم الجوائز (المطلوب في الصورة) ---
with tab2:
    st.header("تصميم الجوائز (Beams)")
    
    # حساب الجوائز الساقطة
    h_drop_req = l_input / 14 # شرط السهم L/14
    # المحدد بالأخضر يتغير هنا: المحسوب + 10 سم أمان كما ورد في تقريرك
    h_drop_final = math.ceil((h_drop_req + 10) / 5) * 5 
    
    st.subheader("الجوائز الساقطة (سقف القبو)")
    st.write(f"• الارتفاع المطلوب (L/14): {h_drop_req:.1f} cm")
    [span_2](start_span)st.success(f"• الأبعاد المعتمدة: 30x{h_drop_final} cm (زيادة أمان متغيرة)")[span_2](end_span)

    # حساب الجوائز المخفية
    # وسطي L/4 وطرفي L/6
    b_hidden_req = l_input / 4
    # العرض المعتمد يتغير ليكون أكبر من المحسوب ويقبل القسمة على 5
    b_hidden_final = max(105, math.ceil(b_hidden_req / 5) * 5)
    
    st.subheader("الجوائز المخفية (الهوردي)")
    st.write(f"• العرض الأدنى المطلوب للجائز الوسطي: {b_hidden_req:.1f} cm")
    [span_3](start_span)st.success(f"• العرض المعتمد ديناميكياً: {b_hidden_final} cm")[span_3](end_span)

# --- 3. قسم الأساسات ---
with tab3:
    st.header("الأساسات (الحصيرة)")
    # الكود السوري L/6
    h_raft_min = l_input / 6
    h_raft_final = max(90, math.ceil(h_raft_min / 10) * 10)
    
    st.write(f"• السماكة حسب الكود السوري (L/6): {h_raft_min:.1f} cm")
    [span_4](start_span)st.success(f"• سماكة الحصيرة المعتمدة: {h_raft_final} cm")[span_4](end_span)
