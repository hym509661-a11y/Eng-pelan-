import streamlit as st
import ezdxf
from ezdxf.units import PaperUnits
import io

# --- الإعدادات الإنشائية ---
st.title("🏗️ نظام تصميم المنشآت - مهندس بلان")
st.sidebar.header("إعدادات المشروع")

# مدخلات الواجهة التي طلبتها
num_floors = st.sidebar.number_input("عدد الطوابق", min_value=1, value=3)
num_columns = st.sidebar.number_input("عدد الأعمدة في الطابق الواحد", min_value=2, value=6)
rebar_type = st.sidebar.selectbox("نوع التسليح الرئيسي", ["T12", "T14", "T16"])
stamp_number = "0998449697" # الرقم المطلوب في الختم

def generate_structure():
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # 1. رسم الأعمدة والجوائز (Beams) التي تربطها
    # سنفترض توزيع الأعمدة على صفين لتوضيح الربط
    col_spacing = 5.0
    for i in range(num_columns // 2):
        x = i * col_spacing
        # رسم عمودين (مربعين)
        msp.add_lwpolyline([(x, 0), (x+0.4, 0), (x+0.4, 0.4), (x, 0.4), (x, 0)], close=True)
        msp.add_lwpolyline([(x, 5), (x+0.4, 5), (x+0.4, 5.4), (x, 5.4), (x, 5)], close=True)
        
        # رسم الجائز (Beam) الذي يربط العمودين ببعضهما
        msp.add_line((x+0.2, 0.4), (x+0.2, 5))
        
        # توضيح التسليح (كتابة نوع التسليح فوق كل عنصر)
        msp.add_text(f"Reinforcement: {rebar_type}", 
                     dxfattribs={'height': 0.2}).set_placement((x, -0.5))

    # 2. إضافة واجهة البيانات (الجدول الإنشائي)
    msp.add_text(f"Floor Count: {num_floors}", dxfattribs={'height': 0.5}).set_placement((0, 10))
    msp.add_text(f"Columns per Floor: {num_columns}", dxfattribs={'height': 0.5}).set_placement((0, 9))

    # 3. إضافة الختم النهائي مع الرقم
    stamp_text = f"Designed by: Engineer Plan | Mob: {stamp_number}"
    msp.add_text(stamp_text, 
                 dxfattribs={'height': 0.6, 'color': 1}).set_placement((0, -2))

    # حفظ الملف
    out_buffer = io.StringIO()
    doc.write(out_buffer)
    return out_buffer.getvalue()

# --- واجهة Streamlit للعرض ---
if st.button("توليد المخطط الإنشائي والتسليح"):
    dxf_data = generate_structure()
    st.success(f"تم إنشاء المخطط لعدد {num_floors} طوابق بنجاح!")
    
    st.download_button(
        label="💾 تحميل ملف AutoCAD (DXF)",
        data=dxf_data,
        file_name="Structural_Plan_Stamp.dxf",
        mime="application/dxf"
    )

st.markdown("---")
st.info(f"ملاحظة: الختم يحتوي تلقائياً على الرقم: {stamp_number}")
