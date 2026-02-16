import streamlit as st
import ezdxf
from ezdxf import units
import io
import math

# إعدادات الصفحة
st.set_page_config(page_title="المصمم الإنشائي الاحترافي", layout="wide")

def main():
    st.title("🏗️ نظام التصميم الإنشائي المتكامل (DXF)")
    st.write("حساب تلقائي للتسليح ورسم المقاطع التفصيلية.")

    # القائمة الجانبية للمدخلات
    with st.sidebar:
        st.header("📋 معطيات التصميم")
        L = st.number_input("طول الجسر (m)", value=5.0)
        H = st.number_input("ارتفاع الجسر (cm)", value=60)
        B = st.number_input("عرض الجسر (cm)", value=25)
        
        st.subheader("⚙️ الخصائص والمجهودات")
        moment = st.number_input("العزم التصميمي (kN.m)", value=120.0)
        fy = 420  # إجهاد خضوع الحديد
        bar_dia = st.selectbox("قطر الحديد الرئيسي (mm)", [12, 14, 16, 18, 20, 25], index=2)
        stirrup_dia = 8
        cover = 2.5  # cm

    # --- الحسابات الإنشائية التلقائية ---
    d = H - cover - (bar_dia/20) - (stirrup_dia/10) # العمق الفعال
    As_req = (moment * 10**6) / (0.9 * fy * d * 0.9) # مساحة الحديد mm2
    bar_area = (math.pi * (bar_dia**2)) / 4
    num_bars = math.ceil(As_req / bar_area)
    if num_bars < 2: num_bars = 2

    # عرض النتائج
    c1, c2, c3 = st.columns(3)
    c1.info(f"عدد القضبان السفلية: {num_bars}")
    c2.info(f"الحديد العلوي (تعليق): 2 T 12")
    c3.success(f"الختم: 0998449697")

    def create_dxf():
        doc = ezdxf.new('R2010', setup=True)
        msp = doc.modelspace()
        
        # تحويل الوحدات للمتر للرسم
        Lm, Hm, Bm, Cm = L, H/100, B/100, cover/100
        
        # --- 1. المقطع الطولي (Longitudinal Section) ---
        msp.add_lwpolyline([(0, 0), (Lm, 0), (Lm, Hm), (0, Hm)], close=True, dxfattribs={'color': 7})
        # الحديد السفلي والعلوي
        msp.add_line((Cm, Cm), (Lm-Cm, Cm), dxfattribs={'color': 1, 'lwweight': 35})
        msp.add_line((Cm, Hm-Cm), (Lm-Cm, Hm-Cm), dxfattribs={'color': 1, 'lwweight': 35})
        # الكانات
        for i in range(15):
            x = Cm + i * ((Lm - 2*Cm)/14)
            msp.add_line((x, Cm), (x, Hm-Cm), dxfattribs={'color': 3})

        # --- 2. المقطع العرضي (Cross Section) ---
        offset_x = Lm + 0.5 # إزاحة المقطع العرضي بجانب الطولي
        msp.add_lwpolyline([(offset_x, 0), (offset_x+Bm, 0), (offset_x+Bm, Hm), (offset_x, Hm)], close=True)
        # الكانة العرضية
        msp.add_lwpolyline([(offset_x+0.03, 0.03), (offset_x+Bm-0.03, 0.03), 
                            (offset_x+Bm-0.03, Hm-0.03), (offset_x+0.03, Hm-0.03)], close=True, dxfattribs={'color': 3})
        
        # رسم دوائر تمثل حديد التسليح (القضبان)
        # السفلي
        for i in range(num_bars):
            spacing = (Bm - 2*0.04) / (num_bars - 1) if num_bars > 1 else 0
            msp.add_circle((offset_x + 0.04 + i*spacing, 0.04), radius=0.01, dxfattribs={'color': 1})
        # العلوي
        msp.add_circle((offset_x + 0.04, Hm-0.04), radius=0.01, dxfattribs={'color': 1})
        msp.add_circle((offset_x + Bm - 0.04, Hm-0.04), radius=0.01, dxfattribs={'color': 1})

        # --- 3. الختم والنصوص ---
        msp.add_text(f"LONGITUDINAL SECTION - B:{B}xH:{H}", dxfattribs={'height': 0.1}).set_placement((0, Hm+0.1))
        msp.add_text(f"CROSS SECTION", dxfattribs={'height': 0.1}).set_placement((offset_x, Hm+0.1))
        msp.add_text(f"REINFORCEMENT: {num_bars} T {bar_dia} (Bottom)", dxfattribs={'height': 0.08}).set_placement((0, -0.2))
        
        # الرقم المطلوب في الختم
        msp.add_text(f"VERIFIED BY: 0998449697", dxfattribs={'height': 0.1, 'color': 2}).set_placement((0, -0.5))

        out = io.StringIO()
        doc.write(out)
        return out.getvalue()

    if st.button("توليد المخطط التفصيلي النهائي"):
        dxf_data = create_dxf()
        st.download_button("💾 تحميل ملف DXF المحدث", dxf_data, "Structural_Full_Detail.dxf")

    st.markdown("---")
    st.caption("جميع الحقوق محفوظة - التدقيق الإنشائي: 0998449697")

if __name__ == "__main__":
    main()
