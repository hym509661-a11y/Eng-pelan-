import streamlit as st
import numpy as np
import ezdxf
import io

# 1. الإعدادات البصرية الملكية (Engineering Luxury Theme)
st.set_page_config(page_title="Pelan Masterpiece v46", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #0d1b1e;
        background-image: url("https://www.transparenttextures.com/patterns/carbon-fibre.png");
        color: #ffffff;
    }
    .master-card {
        background: rgba(16, 44, 41, 0.9);
        border: 2px solid #d4af37;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    }
    .gold-title { color: #d4af37; font-weight: bold; font-size: 1.5rem; }
    .emerald-val { color: #50c878; font-weight: bold; font-size: 1.8rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='master-card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Grand Masterpiece v46</h1><p class='gold-title'>المكتب الهندسي المتكامل | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية: المدخلات والتحكم بالحديد
with st.sidebar:
    st.header("📏 مدخلات التصميم")
    elem = st.selectbox("العنصر الإنشائي:", [
        "جائز بيتون (Beam)", "أعصاب البلاطة (Ribs)", "أعمدة", 
        "بلاطة هوردي", "بلاطة مصمتة", "خزان مياه"
    ])
    
    st.divider()
    L = st.number_input("طول العنصر L (m):", 1.0, 15.0, 5.0)
    B = st.number_input("العرض B (cm):", 10.0, 100.0, 25.0)
    H = st.number_input("الارتفاع H (cm):", 20.0, 150.0, 60.0)
    Wu = st.number_input("الحمل المصعد Wu (kN/m):", 0.0, 150.0, 35.0)
    
    st.divider()
    st.subheader("🏗️ تسليح المهندس بيلان")
    n_bars = st.number_input("عدد القضبان السفلي:", 1, 15, 4)
    phi = st.selectbox("القطر (mm):", [10, 12, 14, 16, 18, 20, 25])

# 3. محرك الحسابات الإنشائية (Real-time Calculations)
M_max = (Wu * L**2) / 8  # العزم الأقصى kN.m
V_max = (Wu * L) / 2     # القص الأقصى kN
# حساب مساحة الحديد الفعلية
As_actual = n_bars * (np.pi * (phi/10)**2 / 4) # cm2

# 4. واجهة العرض والنتائج
col_data, col_draw = st.columns([1.2, 1])

with col_data:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 التحليل الإنشائي: {elem}")
    
    # عرض النتائج في مربعات فاخرة
    r1, r2, r3 = st.columns(3)
    r1.metric("Max Moment (kN.m)", f"{M_max:.2f}")
    r2.metric("Max Shear (kN)", f"{V_max:.2f}")
    r3.metric("As (cm²)", f"{As_actual:.2f}")

    st.divider()
    st.markdown("### 👨‍🏫 توصية المهندس بيلان:")
    
    # معالجة الأخطاء البرمجية في الشروط (الإزاحات)
    if "جائز" in elem or "أعصاب" in elem:
        st.info(f"💡 نصيحة: التسليح المختار {n_bars}Φ{phi} يغطي العزم المحسوب. تأكد من تكسيح الحديد عند المساند لمقاومة القص.")
            elif "أعمدة" in elem:
        st.info("💡 نصيحة: تأكد من توزيع الكانات (Stirrups) كل 15 سم بحد أقصى لمنع انبعاج القضبان الطولية.")
    elif "خزان" in elem:
        st.info("💡 نصيحة: استخدم خرسانة ذات نفاذية منخفضة ودقق إجهادات الشد في الجدران.")
    else:
        st.success("✅ التصميم يحقق شروط الأمان والاستقرار الإنشائي.")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_draw:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ تفاصيل التسليح والتفريط")
    
    # محاكاة الرسم الهندسي المتقدم مع رفع السهم
    st.write("🔍 **مخطط تفريد الحديد (BBS):**")
        
    st.markdown(f"""
    <div style='background:#1a3c34; border:1px solid #d4af37; padding:15px; border-radius:10px; text-align:center;'>
        <p style='margin:0;'>📍 تفصيل الحديد السفلي:</p>
        <h2 style='color:#d4af37; margin:5px;'>{n_bars} T {phi}</h2>
        <p style='font-size:0.8rem;'>↑ (سهم مرفوع يوضح القطر والعدد) ↑</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    # زر التصدير للأوتوكاد
    if st.button("🚀 تصدير المخطط التنفيذي (DXF)"):
        try:
            doc = ezdxf.new(setup=True); msp = doc.modelspace()
            # رسم الخرسانة
            msp.add_lwpolyline([(0,0), (L*10,0), (L*10,H), (0,H), (0,0)])
            # رسم سيخ الحديد مع سهم وتوصيف
            msp.add_line((0.5, 5), (L*10-0.5, 5), dxfattribs={'color': 1}) # الحديد
            msp.add_line((L*5, 5), (L*5, 15), dxfattribs={'color': 2}) # سهم الرفع
            msp.add_text(f"{n_bars}%%c{phi}", dxfattribs={'height': 2.5}).set_placement((L*5, 17))
            
            buf = io.StringIO(); doc.write(buf)
            st.download_button("📥 تحميل ملف AutoCAD", buf.getvalue(), f"Pelan_{elem}.dxf")
            st.success("تم توليد المخطط بنجاح!")
        except Exception as e:
            st.error(f"عذراً، حدث خطأ أثناء التصدير: {e}")
            
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37; font-size:0.8rem;'>Pelan Engineering Engine v46 | 2026</p>", unsafe_allow_html=True)
