import streamlit as st

# إعداد واجهة البرنامج
st.set_page_config(page_title="برنامج المهندس بيلان الإنشائي", layout="wide")

st.sidebar.title("المكتب الهندسي")
st.sidebar.info("المهندس بيلان مصطفى عبدالكريم\nمشروع برج دمشق (11 طابق)")

st.title("🏗️ نظام الحسابات الإنشائية التفاعلي")

# تبويبات حسب معطيات المشروع
tab1, tab2, tab3 = st.tabs(["بلاطات القبو والملجأ", "بلاطة المتكرر (هوردي)", "الأساسات (الحصيرة)"])

# --- القسم الأول: بلاطات القبو والملجأ ---
with tab1:
    [span_1](start_span)st.header("دراسة بلاطة سقف القبو")[span_1](end_span)
    [span_2](start_span)[span_3](start_span)type_qabo = st.radio("نوع الجزء المراد دراسته:", ["قبو عادي (ممر/غرفة حارس)", "ملجأ"])[span_2](end_span)[span_3](end_span)
    
    [span_4](start_span)L_qabo = st.number_input("أكبر مجاز في البلاطة (m)", value=5.3, key="q1")[span_4](end_span)
    
    if type_qabo == "ملجأ":
        [span_5](start_span)st.warning("⚠️ اشتراطات وزارة الدفاع والكود السوري للملاجئ")[span_5](end_span)
        [span_6](start_span)h_shelter = st.selectbox("سماكة البلاطة المعتمدة (cm)", [20, 25], index=0)[span_6](end_span)
        [span_7](start_span)live_load = 20 # 2 ton/m2[span_7](end_span)
        [span_8](start_span)st.write(f"• السماكة الدنيا: 20 cm")[span_8](end_span)
        [span_9](start_span)st.write(f"• الحمولة الحية (الردم/القصف): {live_load} kN/m²")[span_9](end_span)
    else:
        [span_10](start_span)h_qabo = (L_qabo * 100) / 35 # حساب تقريبي للمحيط المكافئ[span_10](end_span)
        [span_11](start_span)st.write(f"• السماكة المقترحة إنشائياً: 12 cm")[span_11](end_span)
        [span_12](start_span)live_load = 3 # ممرات[span_12](end_span)
        [span_13](start_span)st.write(f"• الحمولة الحية للممرات: {live_load} kN/m²")[span_13](end_span)

# --- القسم الثاني: بلاطة المتكرر (هوردي) ---
with tab2:
    [span_14](start_span)st.header("دراسة البلاطة المعصبة (Hordy)")[span_14](end_span)
    [span_15](start_span)[span_16](start_span)L_rib = st.number_input("طول مجاز العصب (m)", value=5.3, key="r1")[span_15](end_span)[span_16](end_span)
    [span_17](start_span)case = st.selectbox("حالة استمرار العصب:", ["بسيط (L/16)", "مستمر طرف (L/18)", "مستمر طرفين (L/20)", "ظفر (L/8)"])[span_17](end_span)
    
    divisors = {"بسيط (L/16)": 16, "مستمر طرف (L/18)": 18, "مستمر طرفين (L/20)": 20, "ظفر (L/8)": 8}
    h_min_rib = (L_rib * 100) / divisors[case]
    
    [span_18](start_span)st.success(f"السماكة الدنيا المطلوبة: {h_min_rib:.1f} cm")[span_18](end_span)
    [span_19](start_span)st.write("• السماكة المعتمدة في المشروع: 30 cm")[span_19](end_span)
    [span_20](start_span)st.write("• تغطية البلاطة (Concrete Topping): 6 cm")[span_20](end_span)

# --- القسم الثالث: الأساسات (الحصيرة) ---
with tab3:
    [span_21](start_span)st.header("دراسة الحصيرة (Raft Foundation)")[span_21](end_span)
    [span_22](start_span)st.write("عدد الطوابق: 11 طابق")[span_22](end_span)
    [span_23](start_span)L_raft = st.number_input("أكبر مجاز بين المساند (m)", value=5.3, key="f1")[span_23](end_span)
    
    [span_24](start_span)h_raft_syrian = (L_raft * 100) / 6 # الكود السوري L/6[span_24](end_span)
    [span_25](start_span)st.write(f"• السماكة حسب الكود السوري (L/6): {h_raft_syrian:.1f} cm")[span_25](end_span)
    [span_26](start_span)st.info("السماكة المعتمدة للمشروع لتقليل الحديد: 90 cm")[span_26](end_span)
    
    st.subheader("تسليح الحصيرة")
    [span_27](start_span)st.write("• التسليح الأدنى المعتمد: 7T20 لكل متر في الاتجاهين")[span_27](end_span)
    [span_28](start_span)st.write("• التراكب (Overlap): 50Ø (يصل إلى 1 متر)")[span_28](end_span)

st.divider()
st.center = st.write("تمت البرمجة وفق معطيات مشروع الدكتور فادي نقرش - إعداد م. بيلان")
