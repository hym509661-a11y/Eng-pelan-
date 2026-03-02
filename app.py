import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt

# محاولة استيراد مكتبة الأوتوكاد لتجنب انهيار البرنامج إذا لم تكن مثبتة
try:
    import ezdxf
    DXF_AVAILABLE = True
except ImportError:
    DXF_AVAILABLE = False

# --- إعدادات الهوية المهنية للمهندس بيلان ---
st.set_page_config(page_title="Eng. Pelan - Structural Suite", layout="wide")
st.markdown(f"""
    <div style="background-color:#1e272e; padding:20px; border-radius:10px; border-right: 10px solid #ef5350; text-align:right;">
        <h1 style="color:white; margin:0;">المنظومة الهندسية المتكاملة للتصميم وحصر الكميات</h1>
        <p style="color:#d2dae2;"><b>المهندس المدني بيلان مصطفى عبدالكريم | 0998449697</b></p>
        <p style="color:#d2dae2; font-size:14px;">دراسات - إشراف - تعهدات | نسخة 2026 الاحترافية</p>
    </div>
""", unsafe_allow_html=True)

# --- محرك الحسابات الذكي ---
def auto_design_steel(as_required):
    """يختار القطر والعدد الأنسب ليكون بين 5 و 10 أسياخ في المتر"""
    for dia in [10, 12, 14, 16]:
        area_bar = (math.pi * (dia/10)**2) / 4
        num = math.ceil(as_required / area_bar)
        if 5 <= num <= 10: return dia, num
    return 16, math.ceil(as_required / 2.01)

# --- القائمة الجانبية لاختيار العنصر ---
element = st.sidebar.selectbox("🎯 اختر العنصر الإنشائي للتصميم:", 
                               ("بلاطة مصمتة (Slab)", "جائز مسلح (Beam)", "عمود خرساني (Column)"))

# ==========================================
# 1. قسم البلاطات (Slabs)
# ==========================================
if element == "بلاطة مصمتة (Slab)":
    with st.sidebar:
        Ly = st.number_input("طول البلاطة Ly (m)", value=27.0)
        Lx = st.number_input("عرض البلاطة Lx (m)", value=2.0)
        h = st.number_input("السماكة المدخلة h (cm)", value=12)
        mesh = st.radio("نظام التسليح:", ("شبكة واحدة + برانيط", "شبكتين كاملتين"))
    
    # الحسابات الإنشائية (ACI/Code Standard)
    wu = 1.2 * ((h/100)*2500 + 150) + 1.6 * 200 # Wu = 1.2DL + 1.6LL
    mu = (wu * Lx**2) / 8
    d = h - 2.5 # الارتفاع الفعال
    as_req = mu / (0.9 * 4000 * 0.9 * d)
    dia, num = auto_design_steel(as_req)
    
    # حساب الكميات مع معاملات الهالك والكراسي
    concrete = Lx * Ly * (h/100)
    steel_multiplier = 2.25 if mesh == "شبكتين كاملتين" else 1.35
    total_steel = (num * (dia**2/162) * Lx * Ly) * steel_multiplier

    st.subheader("✅ نتائج تصميم البلاطة")
    c1, c2, c3 = st.columns(3)
    c1.metric("التسليح المختار", f"{num} Φ {dia} / m'")
    c2.metric("حجم الخرسانة", f"{concrete:.2f} m³")
    c3.metric("إجمالي وزن الحديد", f"{total_steel:.1f} kg")

    # جدول تفريد الحديد (BBS)
    st.write("### 📋 جدول تفريد الحديد (Bar Bending Schedule)")
    bbs_slab = pd.DataFrame({
        "العنصر": ["حديد سفلي رئيسي", "حديد علوي (برانيط/شبكة)", "حديد توزيع (تعليق)"],
        "القطر (mm)": [dia, dia, 8],
        "الطول التقديري (m)": [Lx+0.3, Lx+0.3 if mesh=="شبكتين كاملتين" else Lx/3+0.2, Ly],
        "الوزن (kg)": [f"{total_steel*0.4:.1f}", f"{total_steel*0.4:.1f}", f"{total_steel*0.2:.1f}"]
    })
    st.table(bbs_slab)

# ==========================================
# 2. قسم الجوائز (Beams)
# ==========================================
elif element == "جائز مسلح (Beam)":
    with st.sidebar:
        L_beam = st.number_input("طول الجائز (m)", value=5.0)
        b_beam = st.number_input("عرض الجائز b (cm)", value=25)
        h_beam = st.number_input("عمق الجائز h (cm)", value=60)
        v_u = st.number_input("قوة القص Vu (Ton)", value=15.0)
    
    # حساب الكانات (تلقائي بناءً على القص)
    s = 15 if v_u < 12 else 10
    stirrup_design = f"Φ 8 @ {s} cm"
    
    st.subheader("✅ نتائج تصميم الجائز (Beam Details)")
    res_b1, res_b2 = st.columns(2)
    res_b1.info(f"**التسليح الطولي:**\n- سفلي: 4 Φ 16\n- علوي: 2 Φ 14")
    res_b2.success(f"**تسليح القص (الكانات):**\n{stirrup_design}")

# ==========================================
# 3. قسم الأعمدة (Columns)
# ==========================================
elif element == "عمود خرساني (Column)":
    with st.sidebar:
        p_load = st.number_input("الحمولة المحورية P (Ton)", value=120.0)
    
    # تصميم أولي للعمود
    area_required = (p_load * 1000) / (0.35 * 250 + 0.67 * 4000 * 0.01)
    side = math.ceil(math.sqrt(area_required))
    st.subheader("✅ تصميم مقطع العمود")
    st.metric("أبعاد المقطع الموصى بها", f"{side} x {side} cm")
    st.write(f"**التسليح المقترح:** 8 Φ 16 مع كانات Φ 8 كل 15 سم")

# --- محرك تصدير الأوتوكاد (DXF Generator) ---
st.divider()
if st.button("🚀 تصدير المخطط التفصيلي إلى AutoCAD"):
    if DXF_AVAILABLE:
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        # رسم مستطيل يمثل العنصر
        msp.add_lwpolyline([(0, 0), (100, 0), (100, 50), (0, 50), (0, 0)])
        msp.add_text(f"Eng. Pelan - {element} Design").set_placement((0, -15))
        
        filename = "Pelan_Professional_Design.dxf"
        doc.saveas(filename)
        with open(filename, "rb") as f:
            st.download_button("📥 تحميل ملف DXF الآن", f, file_name=filename)
    else:
        st.error("يرجى إضافة ezdxf إلى ملف requirements.txt لتفعيل ميزة الأوتوكاد")

# --- الختم المهني النهائي ---
st.markdown("---")
st.markdown(f"<center><b>المهندس المدني بيلان مصطفى عبدالكريم</b><br>دراسات - إشراف - تعهدات | <b>0998449697</b></center>", unsafe_allow_html=True)
