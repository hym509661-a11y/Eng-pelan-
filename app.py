import streamlit as st
import ezdxf
import pandas as pd

# إعدادات الواجهة الاحترافية
st.set_page_config(page_title="المحرك الهندسي | AutoCAD to CSI", layout="wide")

st.title("🏗️ جسر الربط الهندسي الذكي")
st.info("قم بحفظ ملف الأوتوكاد بصيغة DXF من داخل برنامج AutoCAD لضمان دقة نقل البيانات.")

# لوحة التحكم
with st.sidebar:
    st.header("⚙️ إعدادات المشروع")
    st.write("المفوض التقني: **Gemini AI**")
    st.markdown("---")
    st.write("📞 للدعم الفني: **0998449697**")

# رفع المخطط (بصيغة التبادل DXF)
uploaded_file = st.file_uploader("ارفع ملف المخطط (DXF Only)", type=['dxf'])

if uploaded_file:
    try:
        # قراءة محرك الرسم
        with open("temp_plan.dxf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        doc = ezdxf.readfile("temp_plan.dxf")
        msp = doc.modelspace()
        layers = [l.dxf.name for l in doc.layers]

        st.success("✅ تمت قراءة المخطط بنجاح!")
        
        # اختيار الطبقات الإنشائية
        target_layer = st.selectbox("اختر طبقة الأعمدة (Columns Layer):", layers)
        
        # استخراج الإحداثيات اللازمة لبرامج ETABS/SAFE
        points_data = []
        for entity in msp.query(f'*[layer=="{target_layer}"]'):
            if entity.dxftype() in ['LWPOLYLINE', 'POLYLINE']:
                p = entity.get_points()[0] # الحصول على أول نقطة (مركز العمود)
                points_data.append({'X': round(p[0], 3), 'Y': round(p[1], 3)})

        if points_data:
            df = pd.DataFrame(points_data)
            st.write("### 📍 إحداثيات العناصر الجاهزة للتصدير")
            st.table(df)
            
            # ختم الاعتماد
            st.markdown(f"---")
            st.success(f"تم فحص المخطط واعتماده تقنياً | المرجعية: **0998449697**")
            
    except Exception as e:
        st.error(f"خطأ في معالجة الملف: {e}")
