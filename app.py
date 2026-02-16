import streamlit as st
import ezdxf
from ezdxf import units
import io

# إعدادات الصفحة
st.set_page_config(page_title="المصمم الإنشائي المتكامل", layout="wide")

st.title("تطبيق التفاصيل الإنشائية (DXF)")
st.write("تم دمج الرقم 0998449697 في الختم النهائي للمخططات.")

# تقسيم المدخلات في القائمة الجانبية
with st.sidebar:
    st.header("🏗️ مدخلات العناصر الإنشائية")
    
    with st.expander("بيانات الجسر (Beam)"):
        b_length = st.number_input("طول الجسر (m)", value=5.0)
        b_depth = st.number_input("عمق الجسر (cm)", value=60)
        b_width = st.number_input("عرض الجسر (cm)", value=25)
        cover = st.number_input("الغطاء الخرساني (cm)", value=2.5)

    with st.expander("حديد التسليح (Reinforcement)"):
        # السفلي
        st.subheader("التسليح السفلي")
        bot_bars_n = st.number_input("عدد القضبان السفلية", value=4)
        bot_bars_d = st.selectbox("قطر السفلي (mm)", [12, 14, 16, 18, 20, 25], index=2)
        
        # العلوي والتعليق
        st.subheader("التسليح العلوي/التعليق")
        top_bars_n = st.number_input("عدد القضبان العلوية", value=2)
        top_bars_d = st.selectbox("قطر العلوي (mm)", [10, 12, 14, 16], index=1)
        
        # الكانات
        st.subheader("الكانات (Stirrups)")
        stirrup_d = st.selectbox("قطر الكانة (mm)", [8, 10, 12], index=0)
        stirrup_spacing = st.number_input("المسافة بين الكانات (cm)", value=15)

    st.divider()
    st.info("الختم المعتمد: 0998449697")

# دالة الرسم التفصيلي
def generate_detailed_dxf():
    doc = ezdxf.new('R2010', setup=True)
    doc.header['$INSUNITS'] = units.M
    msp = doc.modelspace()

    # تحويل الوحدات للمتر
    L = b_length
    D = b_depth / 100
    W = b_width / 100
    C = cover / 100

    # 1. رسم حدود الجسر (Outer Frame)
    msp.add_lwpolyline([(0, 0), (L, 0), (L, D), (0, D)], close=True, dxfattribs={'color': 7, 'lwweight': 30})

    # 2. رسم حديد التسليح السفلي (Main Bottom Reinforcement)
    # رسم خط يمثل الحديد السفلي مع ترك غطاء خرساني
    msp.add_line((C, C), (L-C, C), dxfattribs={'color': 1, 'lwweight': 40})
    msp.add_text(f"{bot_bars_n}T{bot_bars_d}", dxfattribs={'height': 0.1}).set_placement((L/2, C+0.05))

    # 3. رسم حديد التعليق العلوي (Top Support Bars)
    msp.add_line((C, D-C), (L-C, D-C), dxfattribs={'color': 1, 'lwweight': 40})
    msp.add_text(f"{top_bars_n}T{top_bars_d}", dxfattribs={'height': 0.1}).set_placement((L/2, D-C-0.15))

    # 4. رسم الكانات (Stirrups) - رسم عينات توضيحية
    num_stirrups = int((L - 2*C) / (stirrup_spacing/100))
    for i in range(min(num_stirrups + 1, 50)): # حد أقصى للرسم التوضيحي
        x_pos = C + i * (stirrup_spacing/100)
        if x_pos < L - C:
            msp.add_line((x_pos, C), (x_pos, D-C), dxfattribs={'color': 3, 'linetype': 'DASHED'})

    # 5. الختم والمعلومات (Stamp)
    stamp_y = -0.5
    msp.add_text(f"DETAILS: {bot_bars_n}T{bot_bars_d} BOT / {top_bars_n}T{top_bars_d} TOP", 
                 dxfattribs={'height': 0.15}).set_placement((0, stamp_y))
    
    # السطر الخاص بك مع الرقم المطلوب
    msp.add_text(f"Contact & Verification: 0998449697", 
                 dxfattribs={'height': 0.15, 'color': 2}).set_placement((0, stamp_y - 0.2))

    out = io.StringIO()
    doc.write(out)
    return out.getvalue()

# واجهة التشغيل
if st.button("توليد المخططات والرسومات التفصيلية"):
    try:
        dxf_file = generate_detailed_dxf()
        st.success("تم إنشاء الرسومات التفصيلية بنجاح!")
        st.download_button(
            label="تحميل المخطط التفصيلي (DXF)",
            data=dxf_file,
            file_name="structural_details.dxf",
            mime="application/dxf"
        )
    except Exception as e:
        st.error(f"حدث خطأ أثناء التوليد: {e}")

st.divider()
st.caption("التدقيق الإنشائي - الرقم المرفق بالختم: 0998449697")
