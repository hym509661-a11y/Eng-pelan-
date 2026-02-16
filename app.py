import streamlit as st
import ezdxf
from ezdxf import units
import io
import math

# إعدادات الصفحة
st.set_page_config(page_title="Structural Design System", layout="wide")

# دالة رسم الختم الهندسي (Title Block) كما في الصور الاحترافية
def draw_title_block(msp, Lm, Hm):
    # رسم إطار اللوحة
    msp.add_lwpolyline([(0, -1.5), (Lm + 2, -1.5), (Lm + 2, Hm + 1), (0, Hm + 1)], close=True, dxfattribs={'color': 7})
    # إضافة نص الختم والرقم المطلوب
    msp.add_text("PROJECT: STRUCTURAL DETAILS", dxfattribs={'height': 0.15}).set_placement((0.5, -0.8))
    msp.add_text(f"CONTACT & VERIFICATION: 0998449697", dxfattribs={'height': 0.15, 'color': 2}).set_placement((0.5, -1.1))
    msp.add_text("DATE: 2026-02-16", dxfattribs={'height': 0.1}).set_placement((0.5, -1.3))

def main():
    st.title("البرنامج الهندسي المتكامل لتفاصيل التسليح")
    
    with st.sidebar:
        st.header("بيانات المقطع الإنشائي")
        L = st.number_input("طول الجسر (m)", value=5.0)
        H = st.number_input("الارتفاع (cm)", value=60)
        B = st.number_input("العرض (cm)", value=25)
        
        st.subheader("الحديد المطلوب (حساب آلي)")
        moment = st.number_input("العزم (kN.m)", value=120.0)
        bar_dia = st.selectbox("قطر الحديد (mm)", [12, 14, 16, 18, 20, 25], index=2)
        
    # الحسابات الهندسية
    d = (H - 4) / 100 # العمق الفعال بالمتر
    as_req = (moment * 10**6) / (0.9 * 420 * d * 1000 * 0.9) # mm2
    num_bars = math.ceil(as_req / (math.pi * (bar_dia**2) / 4))
    if num_bars < 2: num_bars = 2

    # واجهة العرض
    st.info(f"النتيجة: سيتم رسم {num_bars} قضبان قطر {bar_dia} مم سفلي، و 2 قطر 12 مم علوي.")

    def generate_pro_dxf():
        doc = ezdxf.new('R2010', setup=True)
        msp = doc.modelspace()
        Lm, Hm, Bm = L, H/100, B/100
        cover = 0.03 # 3cm
        
        # 1. المقطع الطولي (Longitudinal Section)
        msp.add_lwpolyline([(0, 0), (Lm, 0), (Lm, Hm), (0, Hm)], close=True, dxfattribs={'lwweight': 25})
        # الحديد الرئيسي (سفلي وعلوي)
        msp.add_line((cover, cover), (Lm-cover, cover), dxfattribs={'color': 1, 'lwweight': 35})
        msp.add_line((cover, Hm-cover), (Lm-cover, Hm-cover), dxfattribs={'color': 1, 'lwweight': 35})
        
        # توزيع الكانات دقيق
        spacing = 0.15 # 15cm
        num_stirrups = int((Lm - 2*cover) / spacing)
        for i in range(num_stirrups + 1):
            x = cover + i * spacing
            msp.add_line((x, cover), (x, Hm-cover), dxfattribs={'color': 3})

        # 2. المقطع العرضي (Cross Section)
        cx = Lm + 0.8
        msp.add_lwpolyline([(cx, 0), (cx+Bm, 0), (cx+Bm, Hm), (cx, Hm)], close=True, dxfattribs={'lwweight': 25})
        # الكانة
        msp.add_lwpolyline([(cx+0.02, 0.02), (cx+Bm-0.02, 0.02), (cx+Bm-0.02, Hm-0.02), (cx+0.02, Hm-0.02)], close=True, dxfattribs={'color': 3})
        
        # توزيع قضبان الحديد في المقطع العرضي
        for i in range(num_bars):
            pos_x = cx + 0.04 + (i * (Bm-0.08)/(num_bars-1) if num_bars > 1 else 0)
            msp.add_circle((pos_x, 0.04), radius=0.01, dxfattribs={'color': 1})
        # الحديد العلوي
        msp.add_circle((cx+0.04, Hm-0.04), radius=0.01, dxfattribs={'color': 1})
        msp.add_circle((cx+Bm-0.04, Hm-0.04), radius=0.01, dxfattribs={'color': 1})

        # 3. جدول تفريد الحديد (BBS Table)
        tx = 0
        ty = -2.0
        msp.add_text("REINFORCEMENT TABLE", dxfattribs={'height': 0.15}).set_placement((tx, ty))
        msp.add_text(f"BOTTOM: {num_bars} T {bar_dia}", dxfattribs={'height': 0.12}).set_placement((tx, ty-0.2))
        msp.add_text(f"TOP: 2 T 12", dxfattribs={'height': 0.12}).set_placement((tx, ty-0.4))
        msp.add_text(f"STIRRUPS: T 8 @ 150mm", dxfattribs={'height': 0.12}).set_placement((tx, ty-0.6))

        # 4. الختم الهندسي مع الرقم
        draw_title_block(msp, Lm, Hm)

        out = io.StringIO()
        doc.write(out)
        return out.getvalue()

    if st.button("توليد المخطط النهائي كما في الصور"):
        dxf_file = generate_pro_dxf()
        st.download_button("📥 تحميل ملف DXF الاحترافي", dxf_file, "Final_Structural_Plan.dxf")

if __name__ == "__main__":
    main()
