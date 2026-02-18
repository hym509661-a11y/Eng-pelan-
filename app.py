import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ترويسة التطبيق بناءً على تعليماتك
st.set_page_config(page_title="مكتب المهندس بيلان الإنشائي", layout="wide")

def main():
    st.sidebar.title("القائمة الرئيسية")
    page = st.sidebar.selectbox("اختر المرحلة:", 
        ["المدخلات العامة", "البلاطات المصمتة", "الجوائز الساقطة", "الأعمدة", "الهوردي والآجر", "الأساسات"])

    # الختم الخاص بك يظهر في أسفل القائمة الجانبية
    st.sidebar.markdown("---")
    st.sidebar.info("المهندس المدني بيلان مصطفى عبدالكريم\n\nدراسات-اشراف-تعهدات\n\n0998449697")

    if page == "المدخلات العامة":
        show_general_inputs()
    elif page == "البلاطات المصمتة":
        show_solid_slabs()

# --- الصفحة الأولى: المدخلات العامة ---
def show_general_inputs():
    st.header("📋 المدخلات العامة للمشروع")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("خصائص المواد")
        fcu = st.number_input("إجهاد الخرسانة المميز (fcu) - MPa", value=25)
        fy = st.number_input("إجهاد خضوع الحديد (fy) - MPa", value=400)
    
    with col2:
        st.subheader("الأحمال التصميمية")
        st.session_state['live_load'] = st.number_input("الحمولة الحية (LL) - kN/m²", value=2.0)
        st.session_state['cover_load'] = st.number_input("حمولة التغطية (Cover) - kN/m²", value=1.5)

# --- الصفحة الثانية: دراسة البلاطات ---
def show_solid_slabs():
    st.header("🏗️ دراسة البلاطات المصمتة")
    
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        L_max = st.number_input("الطول الأكبر للفتحة (L max) - m", value=5.0)
        L_min = st.number_input("الطول الأصغر للفتحة (L min) - m", value=4.0)
    
    # تحديد نوع البلاطة تلقائياً
    r = L_max / L_min
    slab_type = "اتجاه واحد (One-Way)" if r > 2 else "اتجاهين (Two-Way)"
    st.success(f"النتيجة: البلاطة تعمل في {slab_type} (r = {r:.2f})")

    # حساب السماكة المقترحة (تبسيط للكود)
    h = (L_min * 100) / 35  # مثال تقريبي
    st.write(f"**السماكة الدنيا المقترحة:** {np.ceil(h)} cm")

    # رسم توضيحي بسيط للحديد
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.add_patch(plt.Rectangle((0, 0), L_max, L_min, fill=None, hatch='/', label='Concrete'))
    ax.set_title(f"مخطط توزيع الحديد - {slab_type}")
    st.pyplot(fig)

if __name__ == "__main__":
    main()
