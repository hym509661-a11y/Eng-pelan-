import streamlit as st
import ezdxf
import io

def generate_dxf(rooms_data):
    # إنشاء مستند DXF
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # تعريف الطبقات
    doc.layers.new(name='BEAMS', dxfattribs={'color': 5})
    doc.layers.new(name='RIBS', dxfattribs={'color': 8})
    
    for room in rooms_data:
        x, y = room['pos']
        w, l = room['dim']
        
        # رسم حدود الغرفة (الجوائز)
        msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+l), (x, y+l), (x, y)], is_closed=True, dxfattribs={'layer': 'BEAMS'})
        
        # منطق هندسي: توزيع الأعصاب في الاتجاه القصير
        spacing = 0.50 # 40 سم بلوك + 10 سم عصب
        if w <= l: # الاتجاه القصير هو X
            for i in range(1, int(l/spacing)):
                msp.add_line((x, y + i*spacing), (x + w, y + i*spacing), dxfattribs={'layer': 'RIBS'})
        else: # الاتجاه القصير هو Y
            for i in range(1, int(w/spacing)):
                msp.add_line((x + i*spacing, y), (x + i*spacing, y + l), dxfattribs={'layer': 'RIBS'})

    # حفظ الملف في ذاكرة مؤقتة لتحميله
    out = io.StringIO()
    doc.write(out)
    return out.getvalue()

# واجهة تطبيق Streamlit
st.title("محرك بيلان الإنشائي - توليد مخططات AutoCAD")
st.write("هذا التطبيق يولد مخطط بلاطة هوردي مطابق للمعماري")

# إدخال البيانات (كمثال لمشروع الـ 150م2)
rooms = [
    {'name': 'الصالون', 'pos': (0, 0), 'dim': (3.5, 5.5)},
    {'name': 'المطبخ', 'pos': (0, 5.5), 'dim': (3.1, 4.5)},
    {'name': 'غرفة النوم', 'pos': (3.5, 0), 'dim': (3.5, 5.5)}
]

if st.button("توليد المخطط الإنشائي DXF"):
    dxf_content = generate_dxf(rooms)
    st.download_button(
        label="تحميل ملف المخطط للأوتوكاد",
        data=dxf_content,
        file_name="Structural_Plan_By_Pelan.dxf",
        mime="application/dxf"
    )
