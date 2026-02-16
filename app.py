import streamlit as st
import ezdxf
from ezdxf import units
import io
import math

# إعدادات المنصة الشاملة
st.set_page_config(page_title="Structural AI System (ETABS + SAFE + AutoCAD)", layout="wide")

def main():
    st.title("🏗️ النظام الإنشائي الموحد (Integrated Structural System)")
    st.write("تحليل، تصميم، وتصدير تفاصيل إنشائية - مدمج برقم الاعتماد: 0998449697")

    # --- واجهة المدخلات (تحاكي إيتابس وسيف) ---
    with st.sidebar:
        st.header("📋 معطيات العناصر (SAFE/ETABS Input)")
        file_upload = st.file_uploader("استيراد معماري (DXF/DWG)", type=['dxf'])
        
        with st.expander("خصائص المواد والمقاطع", expanded=True):
            fc = st.number_input("مقاومة الخرسانة f'c (MPa)", value=25)
            fy = st.number_input("إجهاد حديد التسليح fy (MPa)", value=420)
            b = st.number_input("عرض العنصر B (cm)", value=25)
            h = st.number_input("عمق العنصر H (cm)", value=60)

        with st.expander("الأحمال والتحليل", expanded=False):
            dead_load = st.number_input("الحمل الميت (kN/m)", value=20.0)
            live_load = st.number_input("الحمل الحي (kN/m)", value=15.0)
            span = st.number_input("طول الفتحة (m)", value=5.0)

    # --- محرك الحسابات الإنشائية (AI Engine) ---
    # حساب العزم التصميمي Mu = 1.2DL + 1.6LL
    ultimate_load = (1.2 * dead_load) + (1.6 * live_load)
    Mu = (ultimate_load * (span**2)) / 8  # العزم في المنتصف
    
    # حساب الحديد (تلقائي)
    d = (h - 4) / 100 # العمق الفعال
    as_req = (Mu * 10**6) / (0.9 * fy * d * 1000 * 0.9) # mm2
    bar_dia = 16
    bar_area = (math.pi * (bar_dia**2)) / 4
    num_bars = math.ceil(as_req / bar_area)
    if num_bars < 2: num_bars = 2

    # --- عرض المخرجات (تحاكي تقارير التحليل) ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 نتائج التحليل (Analysis)")
        st.write(f"**الحمل التصميمي:** {ultimate_load:.2f} kN/m")
        st.write(f"**العزم الأقصى:** {Mu:.2f} kN.m")
        st.metric("عدد القضبان المطلوب", f"{num_bars} T {bar_dia}")

    with col2:
        st.subheader("🖼️ معاينة المخطط التفصيلي")
        st.info("سيتم تصدير المقطع الطولي والعرضي وجدول التسليح كما في برامج الرسم.")

    # --- محرك الرسم الهندسي (AutoCAD Engine) ---
    def generate_full_system_dxf():
        doc = ezdxf.new('R2010', setup=True)
        msp = doc.modelspace()
        Lm, Hm, Bm = span, h/100, b/100
        cv = 0.03

        # 1. رسم المقطع الطولي (Longitudinal Section)
        msp.add_lwpolyline([(0, 0), (Lm, 0), (Lm, Hm), (0, Hm)], close=True, dxfattribs={'lineweight': 25})
        msp.add_line((cv, cv), (Lm-cv, cv), dxfattribs={'color': 1, 'lineweight': 35}) # تسليح سفلي
        msp.add_line((cv, Hm-cv), (Lm-cv, Hm-cv), dxfattribs={'color': 1, 'lineweight': 35}) # تسليح علوي
        
        # 2. رسم المقطع العرضي (Cross Section)
        cx = Lm + 0.5
        msp.add_lwpolyline([(cx, 0), (cx+Bm, 0), (cx+Bm, Hm), (cx, Hm)], close=True, dxfattribs={'lineweight': 25})
        for i in range(num_bars):
            dist = (Bm-0.08)/(num_bars-1) if num_bars > 1 else 0
            msp.add_circle((cx+0.04+(i*dist), 0.04), radius=0.01, dxfattribs={'color': 1})

        # 3. الختم الهندسي الموحد (Stamp)
        msp.add_text(f"INTEGRATED STRUCTURAL SYSTEM - VERSION 2026", dxfattribs={'height': 0.1}).set_placement((0, -0.4))
        msp.add_text(f"DESIGN & VERIFICATION BY: 0998449697", 
                     dxfattribs={'height': 0.15, 'color': 2}).set_placement((0, -0.7))

        out = io.StringIO()
        doc.write(out)
        return out.getvalue()

    if st.button("توليد المخططات والتقارير (Export Everything)"):
        dxf_data = generate_full_system_dxf()
        st.download_button("💾 تحميل ملف الـ DXF الكامل", dxf_data, "Full_System_Design.dxf")

    st.divider()
    st.caption("نظام ذكاء اصطناعي لدمج ETABS, SAFE, AutoCAD - هاتف: 0998449697")

if __name__ == "__main__":
    main()
