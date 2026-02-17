import streamlit as st
import ezdxf
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="النظام الهندسي الموحد", layout="wide")

# تصميم الواجهة بشكل مبسط لتجنب أخطاء التنسيق
st.title("🏗️ المحرك الإنشائي الذكي")
st.info("نظام الأتمتة الإنشائية: AutoCAD ↔️ ETABS/SAFE")

# لوحة التحكم الجانبية
with st.sidebar:
    st.header("⚙️ إعدادات النموذج")
    usage = st.selectbox("نوع إشغال المبنى:", ["سكني", "تجاري", "مواقف"])
    f_c = st.number_input("مقاومة الخرسانة (Mpa):", value=30)
    st.markdown("---")
    st.write("📞 المراجعة الفنية: **0998449697**")

# رفع المخطط
uploaded_file = st.file_uploader("ارفع مخطط الأوتوكاد (DXF)", type=['dxf'])

if uploaded_file:
    try:
        # حفظ ومعالجة الملف
        with open("temp_master.dxf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        doc = ezdxf.readfile("temp_master.dxf")
        msp = doc.modelspace()
        layers = [l.dxf.name for l in doc.layers]

        col1, col2 = st.columns(2)
        with col1:
            c_layer = st.selectbox("طبقة الأعمدة:", layers)
        with col2:
            s_layer = st.selectbox("طبقة البلاطات:", layers)

        if st.button("🚀 تشغيل الربط وتوليد البيانات"):
            # استخراج البيانات
            extracted = []
            for e in msp.query(f'*[layer=="{c_layer}"]'):
                if e.dxftype() == 'LWPOLYLINE':
                    p = e.get_points()[0]
                    extracted.append({'X': p[0], 'Y': p[1], 'Type': 'Column'})
            
            if extracted:
                df = pd.DataFrame(extracted)
                st.write("### 📊 البيانات المستخرجة بدقة")
                st.dataframe(df)
                st.success("تم تجهيز بيانات الربط بنجاح!")
            else:
                st.warning("لم يتم العثور على عناصر في الطبقة المختارة.")

    except Exception as e:
        st.error(f"حدث خطأ تقني: {e}")

# الختم الرسمي (تنسيق مصلح)
st.markdown("---")
st.warning(f"**ختم الاعتماد الرقمي:** تم التنفيذ بموجب التفويض الشامل للمفوض التقني. للتواصل: **0998449697**")
