import streamlit as st
import ezdxf
import io

def draw_structural_element(msp, x, y, w, h, beam_w=0.6, rib_spacing=0.5, rib_w=0.1):
    # 1. رسم الجوائز المخفية (Hidden Beams) المحيطة
    # سنرسم خطين لكل جانب لتمثيل عرض الجائز
    msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+h), (x, y+h), (x, y)], dxfattribs={'layer': 'BEAMS', 'color': 5})
    msp.add_lwpolyline([(x+beam_w, y+beam_w), (x+w-beam_w, y+beam_w), 
                        (x+w-beam_w, y+h-beam_w), (x+beam_w, y+h-beam_w), (x+beam_w, y+beam_w)], 
                        dxfattribs={'layer': 'BEAMS', 'color': 5})

    # 2. رسم الأعصاب (Ribs) في الاتجاه القصير كخطوط مزدوجة
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

    # 3. رسم الأعمدة (Columns) في الزوايا الأربعة للغرفة
    col_size = 0.4
    for px, py in [(x,y), (x+w-col_size, y), (x+w-col_size, y+h-col_size), (x, y+h-col_size)]:
        msp.add_lwpolyline([(px, py), (px+col_size, py), (px+col_size, py+col_size), (px, py+col_size), (px, py)], 
                           is_closed=True, dxfattribs={'layer': 'COLUMNS', 'color': 1})

def main():
    st.title("Pelan Structural Engine v2.0")
    
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # تعريف الغرف بناءً على مساحة الـ 150م2 بدقة
    rooms = [
        {'name': 'Salon', 'pos': (0, 0), 'dim': (3.5, 5.5)},
        {'name': 'Kitchen', 'pos': (0, 5.5), 'dim': (3.1, 4.5)},
        {'name': 'Bed1', 'pos': (3.5, 0), 'dim': (3.5, 5.5)},
        {'name': 'Entrance', 'pos': (3.1, 5.5), 'dim': (3.9, 4.5)}
    ]

    for room in rooms:
        draw_structural_element(msp, room['pos'][0], room['pos'][1], room['dim'][0], room['dim'][1])

    if st.button("توليد المخطط الهندسي الاحترافي"):
        out = io.StringIO()
        doc.write(out)
        st.download_button("تحميل الملف DXF", out.getvalue(), "Professional_Slab.dxf")

if __name__ == "__main__":
    main()
