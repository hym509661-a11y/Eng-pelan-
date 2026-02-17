import streamlit as st
import ezdxf
import io

def create_dxf_with_stamp(text_content):
    # إنشاء ملف DXF جديد
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # إضافة المحتوى الأساسي للرسم هنا (اختياري)
    msp.add_text("Original Content", dxfattribs={'height': 0.5}).set_placement((0, 2))

    # إضافة الختم مع الرقم المطلوب في نهاية الختم
    # الرقم: 0998449697
    stamp_text = f"{text_content} | Mob: 0998449697"
    
    # إضافة النص في أسفل الرسم كختم
    msp.add_text(stamp_text, 
                 dxfattribs={
                     'height': 0.7, 
                     'color': 1 # اللون الأحمر مثلاً
                 }).set_placement((0, 0))

    # حفظ الملف في ذاكرة مؤقتة لتحميله
    out_stream = io.StringIO()
    doc.write(out_stream)
    return out_stream.getvalue()

# واجهة Streamlit
st.title("برنامج مهندس بلان - توليد ملفات DXF")

user_input = st.text_input("أدخل نص الختم الإضافي:", "ختم هندسي")

if st.button("توليد ملف الأوتوكاد"):
    dxf_data = create_dxf_with_stamp(user_input)
    
    st.download_button(
        label="تحميل ملف DXF",
        data=dxf_data,
        file_name="plan_with_stamp.dxf",
        mime="application/dxf"
    )
