import streamlit as st
import ezdxf
import io

def draw_structural_element(msp, x, y, w, h, beam_w=0.6, rib_spacing=0.5, rib_w=0.1):
    # تحويل القيم لضمان عدم حدوث خطأ في النوع
    x, y, w, h = float(x), float(y), float(w), float(h)
    
    # 1. رسم حدود الغرفة (الجوائز)
    outer_points = [(x, y), (x+w, y), (x+w, y+h), (x, y+h), (x, y)]
    msp.add_lwpolyline(outer_points, dxfattribs={'layer': 'BEAMS', 'color': 5})
    
    inner_points = [(x+beam_w, y+beam_w), (x+w-beam_w, y+beam_w), 
                    (x+w-beam_w, y+h-beam_w), (x+beam_w, y+h-beam_w), (x+beam_w, y+beam_w)]
    msp.add_lwpolyline(inner_points, dxfattribs={'layer': 'BEAMS', 'color': 5})

    # 2. رسم الأعصاب (Ribs) في الاتجاه القصير
    if w <= h:
        num_ribs = int((h - 2*beam_w) / rib_spacing)
        for i in range(1, num_ribs + 1):
            ry = y + beam_w + (i * rib_spacing)
            msp.add_line((x+beam_w, ry), (x+w-beam_w, ry), dxfattribs={'layer': 'RIBS', 'color': 8})
            msp.add_line((x+beam_w, ry-rib_w), (x+w-beam_w, ry-rib_w), dxfattribs={'layer': 'RIBS', 'color': 8})
    else:
        num_ribs = int((w - 2*beam_w) / rib_spacing)
        for i in range(1, num_ribs + 1):
            rx = x + beam_w + (i * rib_spacing)
            msp.add_line((rx, y+beam_w), (rx, y+h-beam_w), dxfattribs={'layer': 'RIBS', 'color': 8})
            msp.add_line((rx-rib_w, y+beam_w), (rx-rib_w, y+h-beam_w), dxfattribs={'layer': 'RIBS', 'color': 8})

    # 3. رسم الأعمدة (Columns) - تم تصحيح القائمة هنا
    col_size = 0.4
    col_corners = [(x, y), (x+w-col_size, y), (x+w-col_size, y+h-col_size), (x, y+h-col_size)]
    for cx, cy in col_corners:
        # يجب تمرير النقاط كقائمة واحدة داخل add_lwpolyline
        cp = [(cx, cy), (cx+col_size, cy), (cx+col_size, cy+col_size), (cx, cy+col_size), (cx, cy)]
        msp.add_lwpolyline(cp, dxfattribs={'layer': 'COLUMNS', 'color': 1})

def main():
    st.title("Pelan Structural Pro v2.1")
    st.write("توليد مخطط إنشائي دقيق (جوائز، أعصاب، وأعمدة)")
    
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # تعريف الطبقات
    if 'BEAMS' not in doc.layers: doc.layers.new(name='BEAMS', dxfattribs={'color': 5})
    if 'RIBS' not in doc.layers: doc.layers.new(name='RIBS', dxfattribs={'color': 8})
    if 'COLUMNS' not in doc.layers: doc.layers.new(name='COLUMNS', dxfattribs={'color': 1})

    # بيانات مشروع الـ 150م2
    rooms = [
        {'pos': (0, 0), 'dim': (3.5, 5.5)},
        {'pos': (3.5, 0), 'dim': (3.5, 5.5)},
        {'pos': (0, 5.5), 'dim': (3.1, 4.5)},
        {'pos': (3.1, 5.5), 'dim': (3.9, 4.5)}
    ]

    for room in rooms:
        draw_structural_element(msp, room['pos'][0], room['pos'][1], room['dim'][0], room['dim'][1])

    if st.button("توليد المخطط الآن"):
        out = io.StringIO()
        doc.write(out)
        st.download_button("💾 تحميل الملف DXF", out.getvalue(), "Pelan_Final_Plan.dxf")

if __name__ == "__main__":
    main()
