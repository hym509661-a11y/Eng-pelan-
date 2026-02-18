import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# الإعدادات العامة لبرنامجك
st.set_page_config(page_title="مكتب المهندس بيلان", layout="wide")

# الختم الرسمي حسب طلبك
OFFICIAL_SEAL = "المهندس المدني بيلان مصطفى عبدالكريم\nدراسات-اشراف-تعهدات\n0998449697"

def main():
    # العنوان الرئيسي مع الختم
    st.sidebar.title("🗂️ نظام التصميم الإنشائي")
    st.sidebar.info(OFFICIAL_SEAL)
    
    page = st.sidebar.radio("انتقل إلى الصفحة:", 
        ["1. المدخلات العامة", "2. البلاطات المصمتة", "3. الجوائز الساقطة", 
         "4. الأعمدة", "5. الهوردي والأعصاب", "6. الجوائز المخفية", "7. الأساسات"])

    if page == "1. المدخلات العامة":
        show_p1_inputs()
    elif page == "2. البلاطات المصمتة":
        show_p2_slabs()
    # ... بقية الصفحات تتبع نفس النمط

def show_p1_inputs():
    st.header("📋 الصفحة الأولى: المدخلات العامة للمشروع")
    st.subheader(f"بإشراف: {OFFICIAL_SEAL.splitlines()[0]}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state['fcu'] = st.number_input("إجهاد الخرسانة (fcu) - MPa", value=25)
        st.session_state['fy'] = st.number_input("إجهاد الحديد (fy) - MPa", value=400)
    with col2:
        st.session_state['LL'] = st.number_input("الحمولة الحية (LL) - kN/m²", value=2.0)
        st.session_state['DL_cov'] = st.number_input("التغطية (Cover) - kN/m²", value=1.5)

def show_p2_slabs():
    st.header("🏗️ الصفحة الثانية: دراسة البلاطات المصمتة")
    
    L_max = st.number_input("الطول الأكبر (L_max) m", value=5.0)
    L_min = st.number_input("الطول الأصغر (L_min) m", value=4.0)
    
    # منطق اختيار الاتجاه حسب الكود
    r = L_max / L_min
    slab_type = "اتجاهين (Two-Way)" if r <= 2 else "اتجاه واحد (One-Way)"
    
    # حساب السماكة (h)
    h = np.ceil((L_min * 100) / 35) if r <= 2 else np.ceil((L_min * 100) / 30)
    
    st.success(f"النتيجة: بلاطة {slab_type} - السماكة الدنيا: {h} cm")
    
    # الرسم الإنشائي الدقيق مع الختم
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.add_patch(plt.Rectangle((0, 0), L_max, L_min, fill=None, edgecolor='black', lw=2))
    
    # إضافة نص توضيحي للحديد والختم على الرسم
    ax.text(0.1, L_min + 0.2, OFFICIAL_SEAL, fontsize=8, color='blue', fontweight='bold')
    ax.text(L_max/2, L_min/2, f"السماكة h={h}cm\nتسليح {slab_type}", ha='center')
    
    st.pyplot(fig)

if __name__ == "__main__":
    main()

