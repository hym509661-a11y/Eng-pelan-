import streamlit as st
import ezdxf
import io

# إعدادات الصفحة
st.set_page_config(page_title="مهندس بلان - التصميم الإنشائي", layout="wide")

st.title("🏗️ برنامج مهندس بلان (المطور)")
st.write("نظام توليد المخططات الإنشائية مع الفرش والتسليح")

# --- الواجهة الجانبية للمدخلات ---
with st.sidebar:
    st.header("⚙️ معايير التصميم")
    num_floors = st.number_input("عدد الطوابق", min_value=1, value=3)
    num_columns = st.number_input("عدد الأعمدة في كل طابق", min_value=2, step=2, value=4)
    rebar_main = st.selectbox("تسليح الجوائز الرئيسي", ["3T12", "3T14", "4T16"])
    rebar_cols = st.selectbox("تسليح الأعمدة", ["4T14", "6T16", "8T16"])
    stirrups = st.text_input("الأساور (الكانات)", "T8 @ 15cm")

# --- وظيفة الرسم الهندسي ---
def generate_advanced_dxf():
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # 1. رسم الأعمدة والجوائز وتوضيح الربط
    col_width = 0.4
    spacing = 5.0
    for i in range(num_columns // 2):
        x_pos = i * spacing
        
        # رسم العمود الأول والثاني في الصف
        for y_pos in [0, 5]:
            # جسم العمود
            msp.add_lwpolyline([(x_pos, y_pos), (x_pos+col_width, y_pos), 
                                (x_pos+col_width, y_pos+col_width), (x_pos, y_pos+col_width)], close=True)
            # رسم حديد التسليح داخل العمود (نقاط)
            msp.add_circle((x_pos+0.1, y_pos+0.1), radius=0.03)
            msp.add_circle((x_pos+0.3, y_pos+0.1), radius=0.03)
            msp.add_text(rebar_cols, dxfattribs={'height': 0.15}).set_placement((x_pos, y_pos-0.3))

        # رسم الجائز (Beam) الواصل بين العمودين
        msp.add_line((x_pos+0.2, col_width), (x_pos+0.2, 5)) 
        msp.add_text(f"Beam: {rebar_main} + {stirrups}", 
                     dxfattribs={'height': 0.2}).set_placement((x_pos+0.3, 2.5), align=5)

    # 2. واجهة بيانات الطوابق (في زاوية اللوحة)
    info_x, info_y = -5, 10
    msp.add_text(f"عدد الطوابق الإجمالي: {num_floors}", dxfattribs={'height': 0.5}).set_placement((info_x, info_y))
    msp.add_text(f"عدد أعمدة الطابق: {num_columns}", dxfattribs={'height': 0.5}).set_placement((info_x, info_y-1))

    # 3. الختم الدائم مع الرقم المطلوب
    stamp_text = f"تصميم: مهندس بلان | موبايل: 0998449697"
    msp.add_text(stamp_text, dxfattribs={'height': 0.7, 'color': 1}).set_placement((0, -2))

    out_buffer = io.StringIO()
    doc.write(out_buffer)
    return out_buffer.getvalue()

# --- زر التشغيل والتحميل ---
if st.button("توليد المخطط الشامل وتحميل الملف"):
    try:
        dxf_file = generate_advanced_dxf()
        st.success(f"تم توليد مخطط لـ {num_floors} طوابق مع {num_columns} أعمدة وجوائز الربط.")
        st.download_button(
            label="💾 تحميل ملف DXF للأوتوكاد",
            data=dxf_file,
            file_name="Engineer_Plan_Full_Design.dxf",
            mime="application/dxf"
        )
    except Exception as e:
        st.error(f"خطأ في النظام: {e}")

st.markdown("---")
st.caption("الرقم المعتمد في الختم: 0998449697")
