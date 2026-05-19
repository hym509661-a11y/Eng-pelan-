import streamlit as st
import ezdxf
import io

def draw_section(msp, x, y, w, l, name):
    x, y, w, l = float(x), float(y), float(w), float(l)
    beam_w = 0.60   # عرض الجائز المخفي
    rib_w = 0.10    # سماكة العصب 10 سم
    block_w = 0.40  # عرض بلوك الهوردي
    spacing = rib_w + block_w # الخطوة الإنشائية 50 سم
    
    # 1. رسم الجوائز المخفية (باللون الأزرق)
    msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+l), (x, y+l), (x, y)], dxfattribs={'layer': 'BEAMS', 'color': 5})
    msp.add_lwpolyline([(x+beam_w, y+beam_w), (x+w-beam_w, y+beam_w), 
                        (x+w-beam_w, y+l-beam_w), (x+beam_w, y+l-beam_w), (x+beam_w, y+beam_w)], 
                        dxfattribs={'layer': 'BEAMS', 'color': 5})

    # 2. رسم الأعصاب المزدوجة (Double Ribs) كما في المخطط
    if w <= l: # الاتجاه القصير
        num = int((l - 2*beam_w) / spacing)
        for i in range(1, num + 1):
            yp = y + beam_w + (i * spacing)
            msp.add_line((x+beam_w, yp), (x+w-beam_w, yp), dxfattribs={'layer': 'RIBS', 'color': 8})
            msp.add_line((x+beam_w, yp-rib_w), (x+w-beam_w, yp-rib_w), dxfattribs={'layer': 'RIBS', 'color': 8})
    else:
        num = int((w - 2*beam_w) / spacing)
        for i in range(1, num + 1):
            xp = x + beam_w + (i * spacing)
            msp.add_line((xp, y+beam_w), (xp, y+l-beam_w), dxfattribs={'layer': 'RIBS', 'color': 8})
            msp.add_line((xp-rib_w, y+beam_w), (xp-rib_w, y+l-beam_w), dxfattribs={'layer': 'RIBS', 'color': 8})

    # 3. تسمية الفراغ المعماري
    txt = msp.add_text(name, dxfattribs={'height': 0.25, 'color': 7})
    txt.dxf.insert = (x + beam_w + 0.2, y + l - 0.5)

def main():
    st.set_page_config(page_title="Pelan Structural Pro", layout="wide")
    st.title("🏗️ محرك بيلان الإنشائي v5.0")
    
    doc = ezdxf.new('R2010', setup=True)
    msp = doc.modelspace()
    
    # تعريف الطبقات الأساسية
    for layer, color in [('BEAMS', 5), ('RIBS', 8), ('TEXT', 7)]:
        if layer not in doc.layers: doc.layers.new(name=layer, dxfattribs={'color': color})

    # توزيع المسقط المعماري 150م2
    layout = [
        {'n': 'الصالون', 'p': (0, 0), 'd': (3.5, 5.5)},
        {'n': 'غرفة نوم 1', 'p': (3.5, 0), 'd': (3.55, 5.5)},
        {'n': 'المطبخ', 'p': (0, 5.5), 'd': (3.1, 4.5)},
        {'n': 'بيت الدرج', 'p': (3.1, 5.5), 'd': (2.4, 3.0)},
        {'n': 'غرفة نوم 2', 'p': (5.5, 5.5), 'd': (3.35, 5.0)},
    ]

    for room in layout:
        draw_section(msp, room['p'][0], room['p'][1], room['d'][0], room['d'][1], room['n'])

    if st.button("توليد وتحميل المخطط"):
        # حل مشكلة العرض النصي: الحفظ بتنسيق ثنائي (Binary)
        buf = io.BytesIO()
        doc.write(buf)
        byte_data = buf.getvalue()
        
        st.download_button(
            label="💾 اضغط هنا لتحميل ملف الأوتوكاد",
            data=byte_data,
            file_name="Pelan_Hordi_Plan.dxf",
            mime="application/octet-stream" # يمنع المتصفح من فتحه كنص
        )

if __name__ == "__main__":
    main()
