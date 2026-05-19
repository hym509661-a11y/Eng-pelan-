import streamlit as st
import ezdxf
import io

def generate_dxf(rooms_data):
    # إنشاء مستند DXF جديد
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # إنشاء الطبقات
    if 'BEAMS' not in doc.layers:
        doc.layers.new(name='BEAMS', dxfattribs={'color': 5})
    if 'RIBS' not in doc.layers:
        doc.layers.new(name='RIBS', dxfattribs={'color': 8})
    
    for room in rooms_data:
        # التأكد من تحويل القيم إلى أرقام عشرية لتجنب TypeError
        x = float(room['pos'][0])
        y = float(room['pos'][1])
        w = float(room['dim'][0])
        l = float(room['dim'][1])
        
        # رسم حدود الغرفة (الجوائز) - تم إصلاح طريقة تمرير النقاط هنا
        points = [(x, y), (x + w, y), (x + w, y + l), (x, y + l), (x, y)]
        msp.add_lwpolyline(points, dxfattribs={'layer': 'BEAMS'})
        
        # منطق هندسي: توزيع الأعصاب في الاتجاه القصير
        spacing = 0.50
        if w <= l:
            # الأعصاب موازية لمحور X
            num_ribs = int(l / spacing)
            for i in range(1, num_ribs):
                y_pos = y + (i * spacing)
                msp.add_line((x, y_pos), (x + w, y_pos), dxfattribs={'layer': 'RIBS'})
        else:
            # الأعصاب موازية لمحور Y
            num_ribs = int(w / spacing)
            for i in range(1, num_ribs):
                x_pos = x + (i * spacing)
                msp.add_line((x_pos, y), (x_pos, y + l), dxfattribs={'layer': 'RIBS'})

    # استخدام StringIO أو BytesIO للتوافق مع Streamlit download
    out = io.StringIO()
    doc.write(out)
    return out.getvalue()

# واجهة التطبيق
st.set_page_config(page_title="Pelan Structural Pro", layout="centered")
st.title("🏗️ محرك بيلان الإنشائي")
st.subheader("توليد مخططات الهوردي للأوتوكاد (150م²)")

# البيانات مأخوذة من مسقطك المعماري بدقة
rooms = [
    {'name': 'الصالون', 'pos': (0, 0), 'dim': (3.5, 5.5)},
    {'name': 'المطبخ', 'pos': (0, 5.5), 'dim': (3.1, 4.5)},
    {'name': 'غرفة النوم', 'pos': (3.5, 0), 'dim': (3.5, 5.5)},
    {'name': 'الممر/بيت الدرج', 'pos': (3.1, 5.5), 'dim': (2.4, 3.0)}
]

if st.button("توليد ملف DXF الآن"):
    try:
        dxf_str = generate_dxf(rooms)
        st.success("تم توليد المخطط بنجاح!")
        st.download_button(
            label="💾 تحميل المخطط للأوتوكاد",
            data=dxf_str,
            file_name="Pelan_Structural_Project.dxf",
            mime="application/dxf"
        )
    except Exception as e:
        st.error(f"حدث خطأ أثناء التوليد: {e}")
