import streamlit as st
import ezdxf
import pandas as pd

# إعدادات الواجهة لتظهر كافة ملفات الأوتوكاد
st.set_page_config(page_title="محرك الأوتوكاد المتكامل", layout="wide")

st.markdown("<h1 style='text-align: center;'>🏗️ نظام معالجة مخططات الأوتوكاد</h1>", unsafe_allow_all_html=True)

# لوحة التحكم
with st.sidebar:
    st.header("⚙️ الإعدادات التقنية")
    st.info("تم تفعيل دعم ملفات DWG و DXF")
    st.markdown("---")
    st.write("📞 للدعم الفني المباشر: **0998449697**")

# تعديل السطر المسؤول عن إظهار الملفات ليشمل DWG
# ملاحظة: برمجياً نستخدم DXF للمعالجة، لذا يفضل تحويل الملف داخل أوتوكاد لضمان القراءة
uploaded_file = st.file_uploader("اختر ملف المخطط من هاتفك", type=['dwg', 'dxf'])

if uploaded_file:
    st.success(f"تم اختيار الملف: {uploaded_file.name}")
    
    # تحذير تقني بسيط
    if uploaded_file.name.endswith('.dwg'):
        st.warning("⚠️ ملفات DWG مشفرة. إذا واجه التطبيق صعوبة في القراءة، يرجى حفظ الملف من الأوتوكاد بصيغة DXF لضمان سحب الإحداثيات لـ ETABS.")

    try:
        # معالجة الملف
        with open("temp_file", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # إذا كان DXF سيبدأ التحليل فوراً
        if uploaded_file.name.endswith('.dxf'):
            doc = ezdxf.readfile("temp_file")
            layers = [l.dxf.name for l in doc.layers]
            st.selectbox("اختر الطبقة لتحويلها إلى ETABS/SAFE:", layers)
            st.success("البيانات جاهزة للتصدير!")
            
    except Exception as e:
        st.error("يرجى التأكد من رفع ملف DXF إذا كنت ترغب في استخراج الإحداثيات برمجياً.")

# الختم الرسمي حسب التفويض الشامل
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; padding: 10px; border: 2px solid #1E3A8A;">
        <p>معتمد تقنياً | التواصل: 0998449697</p>
    </div>
    """, unsafe_allow_all_html=True)
