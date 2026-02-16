import streamlit as st
import ezdxf
from ezdxf import units
import io
import math

# إعدادات الصفحة لتطابق الصور
st.set_page_config(page_title="البرنامج الهندسي المتكامل", layout="wide")

# تخصيص التصميم ليطابق صور المستخدم
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ffffff; color: #31333F; border: 1px solid #dcdcdc; }
    </style>
    """, unsafe_allow_html=True)

def main():
    # العنوان الرئيسي كما في الصورة
    st.title("البرنامج الهندسي المتكامل لتفاصيل التسليح")

    # القائمة الجانبية (بيانات المقطع الإنشائي) كما في الصورة 1000224383
    with st.sidebar:
        st.header("بيانات المقطع الإنشائي")
        L = st.number_input("طول الجسر (m)", value=5.00, format="%.2f")
        H = st.number_input("(cm) الارتفاع", value=60)
        B = st.number_input("(cm) العرض", value=25)
        
        st.divider()
        st.header("الحديد المطلوب (حساب آلي)")
        moment = st.number_input("العزم (kN.m)", value=120.00, format="%.2f")
        bar_dia = st.selectbox("(mm) قطر الحديد", [12, 14, 16, 18, 20, 25], index=2)

    # الحسابات الإنشائية التلقائية
    d_eff = (H - 4) / 100 # العمق الفعال
    as_req = (moment * 10**6) / (0.9 * 420 * d_eff * 1000 * 0.9)
    bar_area = (math.pi * (bar_dia**2)) / 4
    num_bars = math.ceil(as_req / bar_area)
    if num_bars < 2: num_bars = 2

    # رسالة النتيجة الزرقاء كما في الصورة 1000224382
    st.info(f"النتيجة: سيتم رسم {num_bars} قضبان قطر {bar_dia} مم سفلي، و 2 قطر 12 مم علوي.")

    # زر التوليد
    if st.button("توليد المخطط النهائي كما في الصور"):
        try:
            # إنشاء ملف DXF
            doc = ezdxf.new('R2010', setup=True)
            msp = doc.modelspace()
            
            # تحويل الوحدات
            Lm, Hm, Bm = L, H/100, B/100
            c = 0.03 # غطاء خرساني

            # رسم المقطع الطولي (إصلاح خطأ lwweight باستخدام قيمة صحيحة)
            # ملاحظة: ezdxf يستخدم قيم مثل 13, 15, 18, 20 لتمثيل ملم x 100
            msp.add_lwpolyline([(0, 0), (Lm, 0), (Lm, Hm), (0, Hm)], close=True, dxfattribs={'lineweight': 20})
            
            # رسم الحديد (السفلي والعلوي)
            msp.add_line((c, c), (Lm-c, c), dxfattribs={'color': 1, 'lineweight': 35}) # سفلي
            msp.add_line((c, Hm-c), (Lm-c, Hm-c), dxfattribs={'color': 1, 'lineweight': 35}) # علوي
            
            # رسم الكانات
            for i in range(11):
                x = c + i * ((Lm - 2*c)/10)
                msp.add_line((x, c), (x, Hm-c), dxfattribs={'color': 3})

            # الختم الهندسي مع رقمك
            msp.add_text(f"STRUCTURAL DETAILS - CONTACT: 0998449697", 
                         dxfattribs={'height': 0.15, 'color': 2}).set_placement((0, -0.5))

            # حفظ الملف
            buf = io.StringIO()
            doc.write(buf)
            
            st.success("تم توليد الملف بنجاح!")
            st.download_button("💾 اضغط هنا لتحميل ملف DXF", buf.getvalue(), "Structural_Design.dxf")
            
        except Exception as e:
            st.error(f"حدث خطأ أثناء التوليد: {e}")

    # التذييل السفلي كما في الصور
    st.divider()
    st.caption("التدقيق الإنشائي - الرقم المرفق بالختم: 0998449697")

if __name__ == "__main__":
    main()
