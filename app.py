import streamlit as st
import ezdxf
import io

def draw_section(msp, x, y, w, l, name):
    x, y, w, l = float(x), float(y), float(w), float(l)
    beam_w = 0.60  # عرض الجائز المخفي
    rib_w = 0.10   # سماكة العصب (10 سم) كما في صورتك
    block_w = 0.40 # عرض بلوكة الهوردي (40 سم)
    spacing = rib_w + block_w # الخطوة = 50 سم
    
    # 1. رسم الجوائز المخفية (باللون الأزرق - Color 5)
    msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+l), (x, y+l), (x, y)], dxfattribs={'layer': 'BEAMS', 'color': 5})
    msp.add_lwpolyline([(x+beam_w, y+beam_w), (x+w-beam_w, y+beam_w), 
                        (x+w-beam_w, y+l-beam_w), (x+beam_w, y+l-beam_w), (x+beam_w, y+beam_w)], 
                        dxfattribs={'layer': 'BEAMS', 'color': 5})

    # 2. توزيع الأعصاب المزدوجة (Double Lines) في الاتجاه القصير
    if w <= l:
        num = int((l - 2*beam_w) / spacing)
        for i in range(1, num + 1):
            yp = y + beam_w + (i * spacing)
            # رسم خطي العصب (سماكة 10 سم)
            msp.add_line((x+beam_w, yp), (x+w-beam_w, yp), dxfattribs={'layer': 'RIBS', 'color': 8})
            msp.add_line((x+beam_w, yp-rib_w), (x+w-beam_w, yp-rib_w), dxfattribs={'layer': 'RIBS', 'color': 8})
    else:
        num = int((w - 2*beam_w) / spacing)
        for i in range(1, num + 1):
            xp = x + beam_w + (i * spacing)
            msp.add_line((xp, y+beam_w), (xp, y+l-beam_w), dxfattribs={'layer': 'RIBS', 'color': 8})
            msp.add_line((xp-rib_w, y+beam_w), (xp-rib_w, y+l-beam_w), dxfattribs={'layer': 'RIBS', 'color': 8})

    # 3. تسمية الفراغ
    txt = msp.add_text(name, dxfattribs={'height': 0.25, 'color': 7})
    txt.dxf.insert = (x + beam_w + 0.2, y + l - 0.5)

def main():
    st.set_page_config(page_title="Pelan Structural Pro", layout="wide")
    st.title("🏗️ محرك بيلان الإنشائي v4.0")
    st.write("توليد مخطط بلاطة هوردي احترافي (أعصاب مزدوجة وجوائز مخفية)")

    # إنشاء مستند DXF بترميز متوافق
    doc = ezdxf.new('R2010', setup=True)
    msp = doc.modelspace()
    
    # تنظيم الطبقات
    for layer, color in [('BEAMS', 5), ('RIBS', 8), ('TEXT', 7)]:
        if layer not in doc.layers: doc.layers.new(name=layer, dxfattribs={'color': color})

    # توزيع الغرف حسب مخطط الـ 150م2 الخاص بك
    layout = [
        {'n': 'الصالون', 'p': (0, 0), 'd': (3.5, 5.5)},
        {'n': 'غرفة نوم 1', 'p': (3.5, 0), 'd': (3.55, 5.5)},
        {'n': 'المطبخ', 'p': (0, 5.5), 'd': (3.1, 4.5)},
        {'n': 'بيت الدرج', 'p': (3.1, 5.5), 'd': (2.4, 3.0)},
        {'n': 'غرفة نوم 2', 'p': (5.5, 5.5), 'd': (3.35, 5.0)},
    ]

    for room in layout:
        draw_section(msp, room['p'][0], room['p'][1], room['d'][0], room['d'][1], room['n'])

    if st.button("توليد المخطط الهندسي"):
        # تحويل الملف إلى BytesIO لضمان عدم فتحه كنص في المتصفح
        buf = io.BytesIO()
        doc.write(buf)
        byte_data = buf.getvalue()
        
        st.success("✅ تم توليد الملف بنجاح")
        st.download_button(
            label="💾 تحميل الملف للأوتوكاد (DXF)",
            data=byte_data,
            file_name="Pelan_Hordi_Plan.dxf",
            mime="application/dxf" # تحديد النوع ليفتح في البرامج الهندسية
        )

if __name__ == "__main__":
    main()
