import streamlit as st
import ezdxf
import io

# دالة ذكية لرسم أي بلاطة هوردي مهما كانت أبعادها
def draw_hordi_slab(msp, width, length, slab_name="Slab"):
    beam_w = 0.60   # عرض الجائز المخفي ثابت
    rib_w = 0.10    # عصب 10 سم
    block_w = 0.40  # بلوك 40 سم
    spacing = rib_w + block_w # 0.50m
    
    # رسم الجوائز (اللون الأزرق)
    msp.add_lwpolyline([(0, 0), (width, 0), (width, length), (0, length), (0, 0)], dxfattribs={'layer': 'BEAMS', 'color': 5})
    msp.add_lwpolyline([(beam_w, beam_w), (width-beam_w, beam_w), (width-beam_w, length-beam_w), (beam_w, length-beam_w), (beam_w, beam_w)], dxfattribs={'layer': 'BEAMS', 'color': 5})

    # توزيع الأعصاب في الاتجاه القصير تلقائياً
    if width <= length:
        num = int((length - 2*beam_w) / spacing)
        for i in range(1, num + 1):
            y = beam_w + (i * spacing)
            msp.add_line((beam_w, y), (width-beam_w, y), dxfattribs={'layer': 'RIBS', 'color': 8})
            msp.add_line((beam_w, y-rib_w), (width-beam_w, y-rib_w), dxfattribs={'layer': 'RIBS', 'color': 8})
    else:
        num = int((width - 2*beam_w) / spacing)
        for i in range(1, num + 1):
            x = beam_w + (i * spacing)
            msp.add_line((x, beam_w), (x, length-beam_w), dxfattribs={'layer': 'RIBS', 'color': 8})
            msp.add_line((x-rib_w, beam_w), (x-rib_w, length-beam_w), dxfattribs={'layer': 'RIBS', 'color': 8})

    # إضافة اسم البلاطة
    txt = msp.add_text(slab_name, dxfattribs={'height': 0.3, 'color': 7})
    txt.dxf.insert = (width/2 - 0.5, length/2)

def main():
    st.set_page_config(page_title="By Pelan - Structural Engine", layout="centered")
    st.title("🏗️ محرك بيلان الهندسي الشامل")
    st.write("أدخل أبعاد أي مشروع لتوليد مخطط الهوردي فوراً")

    # مدخلات ديناميكية لأي مشروع
    col1, col2 = st.columns(2)
    with col1:
        w = st.number_input("عرض البلاطة (متر)", min_value=1.0, value=4.0, step=0.1)
    with col2:
        l = st.number_input("طول البلاطة (متر)", min_value=1.0, value=5.0, step=0.1)
    
    project_name = st.text_input("اسم المشروع/الغرفة", value="غرفة نوم")

    if st.button("توليد المخطط الآن"):
        try:
            doc = ezdxf.new('R2010', setup=True)
            msp = doc.modelspace()
            
            # رسم البلاطة بالأبعاد المدخلة
            draw_hordi_slab(msp, w, l, project_name)
            
            # معالجة الملف للتحميل المباشر
            buf = io.BytesIO()
            doc.write(buf)
            byte_data = buf.getvalue()
            
            st.success(f"✅ تم تجهيز مخطط {project_name} بنجاح!")
            st.download_button(
                label="💾 تحميل ملف الأوتوكاد (DXF)",
                data=byte_data,
                file_name=f"{project_name}.dxf",
                mime="application/octet-stream"
            )
        except Exception as e:
            st.error(f"حدث خطأ: {e}")

if __name__ == "__main__":
    main()
