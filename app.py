import streamlit as st
import ezdxf
import io

def draw_section(msp, x, y, w, l, name):
    x, y, w, l = float(x), float(y), float(w), float(l)
    beam_w = 0.60  # عرض الجائز المخفي
    
    # 1. رسم الجوائز المحيطة
    msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+l), (x, y+l), (x, y)], dxfattribs={'layer': 'BEAMS', 'color': 5})
    msp.add_lwpolyline([(x+beam_w, y+beam_w), (x+w-beam_w, y+beam_w), 
                        (x+w-beam_w, y+l-beam_w), (x+beam_w, y+l-beam_w), (x+beam_w, y+beam_w)], 
                        dxfattribs={'layer': 'BEAMS', 'color': 5})

    # 2. توزيع الأعصاب (Ribs) في الاتجاه القصير
    spacing = 0.50
    if w <= l:
        num = int((l - 2*beam_w) / spacing)
        for i in range(1, num + 1):
            yp = y + beam_w + (i * spacing)
            msp.add_line((x+beam_w, yp), (x+w-beam_w, yp), dxfattribs={'layer': 'RIBS', 'color': 8})
    else:
        num = int((w - 2*beam_w) / spacing)
        for i in range(1, num + 1):
            xp = x + beam_w + (i * spacing)
            msp.add_line((xp, y+beam_w), (xp, y+l-beam_w), dxfattribs={'layer': 'RIBS', 'color': 8})

    # 3. إضافة النص (تم إصلاح السطر 30 هنا)
    text_element = msp.add_text(name, dxfattribs={'height': 0.25, 'color': 7})
    text_element.dxf.insert = (x + beam_w + 0.1, y + l - 0.4)

def main():
    st.title("Pelan Structural Engine v3.0")
    st.subheader("مخطط بلاطة هوردي مطابق للمعماري (150م²)")

    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # تعريف الطبقات
    for layer, color in [('BEAMS', 5), ('RIBS', 8)]:
        if layer not in doc.layers: doc.layers.new(name=layer, dxfattribs={'color': color})

    # إحداثيات الغرف مطابقة لمخططك (150 m2)
    # ملاحظة: تم ضبط الإحداثيات لتعكس الجوار الحقيقي في مخططك
    layout = [
        {'n': 'الصالون', 'p': (0, 0), 'd': (3.50, 5.50)},
        {'n': 'غرفة نوم 1', 'p': (3.50, 0), 'd': (3.55, 5.50)},
        {'n': 'المطبخ', 'p': (0, 5.50), 'd': (3.10, 4.50)},
        {'n': 'بيت الدرج', 'p': (3.10, 5.50), 'd': (2.40, 3.00)},
        {'n': 'غرفة نوم 2', 'p': (5.50, 5.50), 'd': (3.35, 5.00)},
    ]

    for item in layout:
        draw_section(msp, item['p'][0], item['p'][1], item['d'][0], item['d'][1], item['n'])

    if st.button("توليد المخطط الإنشائي"):
        out = io.StringIO()
        doc.write(out)
        st.download_button("💾 تحميل ملف DXF", out.getvalue(), "Pelan_Final_Plan.dxf")

if __name__ == "__main__":
    main()
