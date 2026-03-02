import streamlit as st
import math
import pandas as pd
import ezdxf  # مكتبة الأوتوكاد (pip install ezdxf)

# --- الهوية المهنية (المهندس بيلان) ---
st.set_page_config(page_title="Eng. Pelan - Structural Pro", layout="wide")
st.markdown(f"""
    <div style="background-color:#2c3e50; padding:20px; border-radius:10px; border-right: 10px solid #e74c3c; text-align:right;">
        <h1 style="color:white; margin:0;">المنظومة الهندسية المتكاملة للتصميم والكميات</h1>
        <p style="color:#ecf0f1;"><b>المهندس المدني بيلان مصطفى عبدالكريم | 0998449697</b></p>
        <p style="color:#bdc3c7; font-size:14px;">تصميم - إشراف - تنفيذ | 2026</p>
    </div>
""", unsafe_allow_html=True)

# --- القائمة الجانبية للمدخلات ---
element = st.sidebar.selectbox("🎯 اختر العنصر الإنشائي:", ("بلاطة مصمتة (Slab)", "جائز مسلح (Beam)"))

def calculate_steel(as_req):
    """محرك اختيار القطر والعدد تلقائياً"""
    for dia in [10, 12, 14, 16]:
        area = (math.pi * (dia/10)**2) / 4
        num = math.ceil(as_req / area)
        if 5 <= num <= 10: return dia, num
    return 16, math.ceil(as_req / 2.01)

# --- 1. قسم البلاطات (Slabs) ---
if element == "بلاطة مصمتة (Slab)":
    with st.sidebar:
        Ly = st.number_input("الطول Ly (m)", value=27.0)
        Lx = st.number_input("العرض Lx (m)", value=2.0)
        h = st.number_input("السماكة h (cm)", value=12)
        mesh = st.radio("نظام التسليح:", ("شبكة واحدة + برانيط", "شبكتين كاملتين"))
    
    # الحسابات الإنشائية
    wu = 1.2 * ((h/100)*2500 + 150) + 1.6 * 200
    mu = (wu * Lx**2) / 8
    as_req = mu / (0.9 * 4000 * 0.9 * (h-2.5))
    dia, num = calculate_steel(as_req)
    
    # حساب الكميات وتفريد الحديد
    bar_len = Lx + 0.30 # طول السيخ مع العكفات
    total_m = num * bar_len * Ly
    unit_w = (dia**2 / 162)
    base_weight = total_m * unit_w
    
    if mesh == "شبكتين كاملتين":
        final_weight = base_weight * 2.2 # ضعف الحديد + 20% كراسي وفضلات
        top_desc = f"شبكة علوية كاملة {num}Φ{dia}/m"
    else:
        final_weight = base_weight * 1.3 # سفلي + برانيط + 10% فضلات
        top_desc = f"برانيط علوية {num}Φ{dia}/m"

    st.subheader("✅ نتائج التصميم وجدولة الكميات (BBS)")
    
    # عرض النتائج في بطاقات
    c1, c2, c3 = st.columns(3)
    c1.metric("التسليح السفلي", f"{num} Φ {dia} / m'")
    c2.metric("حجم البيتون الكلي", f"{Lx*Ly*h/100:.2f} m³")
    c3.metric("إجمالي وزن الحديد", f"{final_weight:.1f} kg")

    # جدول تفريد الحديد (BBS)
    st.write("### 📋 جدول تفريد الحديد (Bar Bending Schedule)")
    bbs_data = {
        "العنصر": ["حديد سفلي رئيسي", "حديد علوي (برانيط/شبكة)", "حديد توزيع (تعليق)"],
        "القطر (mm)": [dia, dia, 8],
        "الشكل": ["L-Shape", "L-Shape", "Straight"],
        "الطول الإجمالي (m)": [f"{bar_len:.2f}", f"{bar_len:.2f}" if mesh=="شبكتين كاملتين" else f"{Lx/3:.2f}", Ly],
        "الوزن الكلي (kg)": [f"{base_weight:.1f}", f"{base_weight if mesh=='شبكتين كاملتين' else base_weight*0.3:.1f}", f"{(8**2/162)*5*Lx*Ly:.1f}"]
    }
    st.table(pd.DataFrame(bbs_data))

# --- 2. محرك رسم DXF للأوتوكاد ---
st.divider()
if st.button("🚀 تصدير المخطط التفصيلي إلى AutoCAD (DXF)"):
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # رسم حدود المقطع العرضي
    p_h = h # الارتفاع
    p_w = Lx * 100 # العرض بالسم
    msp.add_lwpolyline([(0,0), (p_w, 0), (p_w, p_h), (0, p_h), (0,0)], dxfattribs={'color': 7})
    
    # رسم أسياخ الحديد
    msp.add_line((5, 3), (p_w-5, 3), dxfattribs={'color': 1, 'lineweight': 35}) # سفلي
    msp.add_text(f"Bottom: {num}T{dia}/m").set_placement((p_w/2, -10))
    
    # إضافة الختم المهني بيلان
    footer_text = f"Designed by Eng. Pelan - 0998449697"
    msp.add_text(footer_text).set_placement((0, -25))
    
    filename = "Pelan_Slab_Design.dxf"
    doc.saveas(filename)
    with open(filename, "rb") as f:
        st.download_button("📥 تحميل ملف الأوتوكاد الآن", f, file_name=filename)

# --- الختم المهني النهائي ---
st.markdown("---")
st.markdown(f"""
    <div style="text-align:center;">
        <p style="font-size:18px;">المهندس المدني <b>بيلان مصطفى عبدالكريم</b></p>
        <p>دراسات - إشراف - تعهدات | <b>0998449697</b></p>
    </div>
""", unsafe_allow_html=True)
