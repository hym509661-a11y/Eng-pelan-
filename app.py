import streamlit as st
import ezdxf
from ezdxf import units
import io

# إعدادات الصفحة
st.set_page_config(page_title="المصمم الإنشائي الذكي", layout="wide")

st.title("تطبيق التصميم الإنشائي وتصدير DXF")
st.write("تم ضبط الكود ليشمل كافة العناصر الإنشائية والختم المطلوب.")

# مدخلات المستخدم للعناصر الإنشائية
with st.sidebar:
    st.header("بيانات المشروع")
    project_name = st.text_input("اسم المشروع", "مخطط إنشائي سكني")
    beam_length = st.number_input("طول الجسر (m)", value=5.0)
    column_width = st.number_input("عرض العمود (cm)", value=30)
    
    st.divider()
    st.info("سيتم إضافة الرقم 0998449697 تلقائياً للختم.")

# دالة إنشاء ملف DXF
def generate_dxf(p_name, b_len, c_width):
    # إنشاء ملف جديد بتنسيق R2010
    doc = ezdxf.new('R2010', setup=True)
    doc.header['$INSUNITS'] = units.M  # ضبط الوحدات للمتر
    msp = doc.modelspace()

    # 1. رسم العناصر الإنشائية (مثال: جسر وعمودين)
    # رسم العمود الأول
    c_m = c_width / 100
    msp.add_lwpolyline([(0, 0), (c_m, 0), (c_m, c_m), (0, c_m)], close=True)
    
    # رسم الجسر
    msp.add_line((c_m, c_m/2), (b_len + c_m, c_m/2))
    
    # رسم العمود الثاني
    msp.add_lwpolyline([(b_len + c_m, 0), (b_len + 2*c_m, 0), (b_len + 2*c_m, c_m), (b_len + c_m, c_m)], close=True)

    # 2. إضافة الختم (Stamp) في أسفل اللوحة
    footer_text = f"مشروع: {p_name} | التدقيق الإنشائي: مهندس معتمد | تواصل: 0998449697"
    msp.add_text(footer_text, 
                 dxfattribs={'height': 0.2, 'color': 7}).set_placement((0, -0.5))

    # حفظ الملف في ذاكرة مؤقتة
    out = io.StringIO()
    doc.write(out)
    return out.getvalue()

# عرض النتائج
if st.button("توليد المخطط الإنشائي"):
    dxf_content = generate_dxf(project_name, beam_length, column_width)
    
    st.success("تم توليد المخطط بنجاح مع كافة العناصر والختم!")
    
    st.download_button(
        label="تحميل ملف DXF",
        data=dxf_content,
        file_name="structural_plan.dxf",
        mime="application/dxf"
    )

st.divider()
st.caption("جميع الحقوق محفوظة - الرقم المعتمد في الختم: 0998449697")
