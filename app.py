import streamlit as st
import math

# إعدادات الصفحة والختم الخاص بك
st.set_page_config(page_title="مكتب المهندس بيلان مصطفى", layout="wide")
st.sidebar.markdown("### المهندس المدني بيلان مصطفى عبدالكريم\n دراسات-اشراف-تعهدات \n 0998449697")

st.title("نظام التصميم الإنشائي المتكامل - مشروع برج دمشق")

# تقسيم التطبيق إلى تبويبات حسب أقسام الملف
tab1, tab2, tab3, tab4 = st.tabs(["البلاطات (Slabs)", "الزلازل (Seismic)", "الأساسات (Foundations)", "الدرج (Stairs)"])

# --- القسم الأول: البلاطات ---
with tab1:
    st.header("تصميم البلاطات (مصمتة / هوردي)")
    type_slab = st.selectbox("نوع البلاطة", ["مصمتة (Solid)", "هوردي (Ribbed)"])
    
    L_max = st.number_input("أكبر مجاز (L) بالمتر", value=5.3)
    
    if type_slab == "مصمتة (Solid)":
        # [span_0](start_span)شرط الملف: البلاطة العاملة باتجاهين (المحيط المكافئ / 140)[span_0](end_span)
        h_min = (L_max * 100) / 35 # تقريبي للمحيط أو حسب شرط L/25
        st.info(f"السماكة المقترحة حسب الكود السوري: {h_min:.2f} سم")
        thickness = st.slider("اختر السماكة (cm)", 10, 25, 12)
        
        # [span_1](start_span)شرط الملجأ[span_1](end_span)
        is_shelter = st.checkbox("هل هي بلاطة ملجأ؟")
        if is_shelter:
            if thickness < 20:
                [span_2](start_span)st.error("تحذير: حسب توصيات وزارة الدفاع لا تقل سماكة الملجأ عن 20 سم[span_2](end_span)")
            [span_3](start_span)live_load = 20 # 20kn/m2[span_3](end_span)
            st.write(f"الحمولة الحية للملجأ: {live_load} kN/m²")
            
    else: # هوردي
        # [span_4](start_span)شروط الهوردي حسب الاستمرارية[span_4](end_span)
        condition = st.selectbox("حالة الاستناد", ["بسيط (L/16)", "مستمرة طرف واحد (L/18)", "مستمرة طرفين (L/20)", "ظفر (L/8)"])
        divisor = {"بسيط (L/16)": 16, "مستمرة طرف واحد (L/18)": 18, "مستمرة طرفين (L/20)": 20, "ظفر (L/8)": 8}
        h_rib = (L_max * 100) / divisor[condition]
        st.success(f"السماكة الدنيا المطلوبة للهوردي: {h_rib:.2f} سم")

# --- القسم الثاني: الزلازل (UBC 97) ---
with tab2:
    st.header("التحليل الزلزالي (حسب المنطقة 2C)")
    # [span_5](start_span)المعطيات الثابتة في دمشق حسب الملف[span_5](end_span)
    st.write("المنطقة الزلزالية: **2C** (دمشق)")
    [span_6](start_span)soil_type = st.selectbox("نوع التربة", ["C", "D", "E"], index=0) # الملف ذكر تربة C[span_6](end_span)
    
    # حساب المعاملات Ca و Cv تلقائياً بناءً على اختيارك
    ca = 0.29 if soil_type == "C" else 0.32
    cv = 0.38 if soil_type == "C" else 0.44
    st.write(f"معاملات التصميم: Ca={ca}, Cv={cv}")
    
    system_type = st.radio("الجملة المقاومة", ["جدران قص فقط (R=4.5)", "جملة إطارية (R=5.5)", "جملة مشتركة (R=6.5)"])
    R_map = {"جدران قص فقط (R=4.5)": 4.5, "جملة إطارية (R=5.5)": 5.5, "جملة مشتركة (R=6.5)": 6.5}
    [span_7](start_span)st.write(f"معامل الاستجابة الزلزالية المعتمد: R = {R_map[system_type]}[span_7](end_span)")

# --- القسم الثالث: الأساسات (الحصيرة) ---
with tab3:
    st.header("تصميم الحصيرة (Raft Foundation)")
    L_raft = st.number_input("أكبر مجاز بين الأعمدة في الحصيرة (m)", value=5.3)
    # [span_8](start_span)شرط الكود السوري L/6 إلى L/8[span_8](end_span)
    h_syrian_min = (L_raft * 100) / 8
    h_syrian_max = (L_raft * 100) / 6
    st.write(f"السماكة حسب الكود السوري: بين {h_syrian_min:.1f} و {h_syrian_max:.1f} سم")
    
    chosen_h = st.number_input("السماكة المعتمدة للحصيرة (cm)", value=90)
    # [span_9](start_span)حساب التسليح الأدنى[span_9](end_span)
    min_reinforcement = 0.00125 * 1000 * (chosen_h * 10) / 1000 # cm2/m
    st.info(f"نسبة التسليح الدنيا (0.125%): {min_reinforcement:.2f} cm²/m")

# --- القسم الرابع: الدرج ---
with tab4:
    st.header("تصميم الشاحط والميدة")
    L_stair = st.number_input("طول الشاحط (cm)", value=290)
    # [span_10](start_span)حساب السماكة L/20 إلى L/25[span_10](end_span)
    t_min = L_stair / 25
    t_max = L_stair / 20
    st.write(f"سماكة الشاحط المقترحة: بين {t_min:.1f} و {t_max:.1f} سم")
    
    live_stair = st.slider("الحمولة الحية للدرج (kN/m²)", 3, 5, 4)
    [span_11](start_span)st.warning("ملاحظة: تم رفع الحمولة إلى 4 kN/m² لتغطية معامل الديناميك في حالات الطوارئ[span_11](end_span)")

st.divider()
st.caption("برمجية مخصصة لمشروع البرج السكني - إعداد المهندس بيلان مصطفى")
