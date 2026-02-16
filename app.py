import streamlit as st
import ezdxf
from ezdxf import units
import io
import math

# إعدادات الصفحة
st.set_page_config(page_title="Professional Structural Designer", layout="wide")

def main():
    st.title("البرنامج الهندسي المتكامل لتفاصيل التسليح")
    
    with st.sidebar:
        st.header("بيانات المقطع الإنشائي")
        L = st.number_input("طول الجسر (m)", value=5.00, format="%.2f")
        H = st.number_input("(cm) الارتفاع", value=60)
        B = st.number_input("(cm) العرض", value=25)
        
        st.divider()
        st.header("الحديد المطلوب (حساب آلي)")
        moment = st.number_input("العزم (kN.m)", value=120.00, format="%.2f")
        bar_dia = st.selectbox("(mm) قطر الحديد الرئيسي", [12, 14, 16, 18, 20, 25], index=2)
        stirrup_dia = 8  # قطر الكانة ثابته 8 مم

    # الحسابات الإنشائية (تلقائية)
    d_eff = (H - 4) / 100
    as_req = (moment * 10**6) / (0.9 * 420 * d_eff * 1000 * 0.9)
    num_bars = math.ceil(as_req / (math.pi * (bar_dia**2) / 4))
    if num_bars < 2: num_bars = 2

    st.info(f"النتيجة: سيتم رسم {num_bars} قضبان قطر {bar_dia} مم سفلي، و 2 قطر 12 مم علوي.")

    if st.button("توليد المخطط النهائي كما في الصور"):
        doc = ezdxf.new('R2010', setup=True)
        msp = doc.modelspace()
        
        # تحويل الوحدات للرسم (متر)
        Lm, Hm, Bm = L, H/100, B/100
        cov = 0.03

        # --- 1. رسم المقطع الطولي (Longitudinal Section) ---
        # رسم الخرسانة بخط سميك
        msp.add_lwpolyline([(0, 0), (Lm, 0), (Lm, Hm), (0, Hm)], close=True, dxfattribs={'lineweight': 30})
        
        # رسم حديد التسليح (الأسياخ)
        # السفلي (أحمر سميك)
        msp.add_line((cov, cov), (Lm-cov, cov), dxfattribs={'color': 1, 'lineweight': 40})
        # العلوي (أحمر سميك)
        msp.add_line((cov, Hm-cov), (Lm-cov, Hm-cov), dxfattribs={'color': 1, 'lineweight': 40})
        
        # رسم الكانات (Stirrups) بتوزيع هندسي
        spacing = 0.15
        for i in range(int((Lm-2*cov)/spacing) + 1):
            x = cov + i * spacing
            msp.add_line((x, cov), (x, Hm-cov), dxfattribs={'color': 252})

        # --- 2. رسم المقطع العرضي (Cross Section) ---
        offset_x = Lm + 0.8
        msp.add_lwpolyline([(offset_x, 0), (offset_x+Bm, 0), (offset_x+Bm, Hm), (offset_x, Hm)], close=True, dxfattribs={'lineweight': 30})
        # الكانة العرضية
        msp.add_lwpolyline([(offset_x+0.02, 0.02), (offset_x+Bm-0.02, 0.02), (offset_x+Bm-0.02, Hm-0.02), (offset_x+0.02, Hm-0.02)], close=True, dxfattribs={'color': 3})
        
        # رسم دوائر الحديد (السفلي)
        for i in range(num_bars):
            gap = (Bm - 0.08) / (num_bars - 1) if num_bars > 1 else 0
            msp.add_circle((offset_x + 0.04 + i*gap, 0.04), radius=0.01, dxfattribs={'color': 1})
        # الحديد العلوي (دائرتين دائماً للتعليق)
        msp.add_circle((offset_x + 0.04, Hm-0.04), radius=0.01, dxfattribs={'color': 1})
        msp.add_circle((offset_x + Bm - 0.04, Hm-0.04), radius=0.01, dxfattribs={'color': 1})

        # --- 3. جدول تفريد الحديد (BBS Table) ---
        table_y = -0.5
        msp.add_text("REINFORCEMENT SCHEDULE", dxfattribs={'height': 0.12}).set_placement((0, table_y))
        msp.add_text(f"MAIN BARS: {num_bars} T {bar_dia} mm", dxfattribs={'height': 0.1}).set_placement((0, table_y - 0.2))
        msp.add_text(f"STIRRUPS: T 8 @ 150 mm", dxfattribs={'height': 0.1}).set_placement((0, table_y - 0.4))

        # --- 4. الختم الهندسي (Title Block) مع رقمك ---
        msp.add_line((0, -1), (Lm+Bm+0.8, -1), dxfattribs={'lineweight': 15})
        msp.add_text(f"DESIGNER CONTACT: 0998449697", 
                     dxfattribs={'height': 0.15, 'color': 2}).set_placement((0, -1.3))

        # تصدير الملف
        buf = io.StringIO()
        doc.write(buf)
        st.success("تم توليد المخطط التفصيلي الكامل!")
        st.download_button("💾 تحميل ملف DXF الاحترافي", buf.getvalue(), "Structural_Full_Detail.dxf")

    st.divider()
    st.caption("الرقم المعتمد في الختم الهندسي: 0998449697")

if __name__ == "__main__":
    main()
