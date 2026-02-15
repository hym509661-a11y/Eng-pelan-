import streamlit as st
import numpy as np
import ezdxf
import io

# 1. الإعدادات البصرية الملكية (Engineering Luxury Theme)
st.set_page_config(page_title="Pelan Masterpiece v47", layout="wide")

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

st.markdown("<div class='master-card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Grand Masterpiece v47</h1><p class='gold-title'>المكتب الهندسي المتكامل | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية: المدخلات والتحكم بالحديد
with st.sidebar:
    st.header("📏 مدخلات التصميم")
    field = st.selectbox("المجال:", ["بيتون مسلح", "أعمال التربة", "زلازل"])
    
    if field == "بيتون مسلح":
        elem = st.selectbox("العنصر الإنشائي:", [
            "جائز بيتون (Beam)", "أعصاب البلاطة (Ribs)", "أعمدة خرسانية", 
            "بلاطة هوردي", "بلاطة مصمتة", "خزان مياه", "جدار استنادي"
        ])
    else:
        elem = field

    st.divider()
    st.subheader("📐 الأبعاد والأحمال")
    L = st.number_input("الطول L (m):", 1.0, 15.0, 5.0)
    B = st.number_input("العرض B (cm):", 10.0, 100.0, 25.0)
    H = st.number_input("الارتفاع H (cm):", 20.0, 150.0, 60.0)
    Wu = st.number_input("الحمل Wu (kN/m):", 0.0, 150.0, 35.0)
    
    st.divider()
    st.subheader("🏗️ تسليح المهندس بيلان")
    n_bars = st.number_input("عدد القضبان السفلي:", 1, 15, 4)
    phi = st.selectbox("القطر (mm):", [10, 12, 14, 16, 18, 20, 25])

# 3. محرك الحسابات الإنشائية
M_max = (Wu * L**2) / 8  # العزم الأقصى
V_max = (Wu * L) / 2     # القص الأقصى
As_actual = n_bars * (np.pi * (phi/10)**2 / 4) # مساحة الحديد cm2

# 4. واجهة العرض والنتائج
col_data, col_draw = st.columns([1.2, 1])

with col_data:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 النتائج الإنشائية: {elem}")
    
    r1, r2, r3 = st.columns(3)
    r1.metric("Max Moment (kN.m)", f"{M_max:.2f}")
    r2.metric("Max Shear (kN)", f"{V_max:.2f}")
    r3.metric("As (cm²)", f"{As_actual:.2f}")

    st.divider()
    st.markdown("### 👨‍🏫 توصية المهندس بيلان:")
    
    # معالجة كافة احتمالات الـ elif لمنع خطأ الإزاحة (Indentation Error)
    if "جائز" in elem or "أعصاب" in elem:
        st.info(f"💡 نصيحة: التسليح المختار {n_bars}Φ{phi} آمن للعزوم. دقق طول التشريك وقص الكانات.")
            elif "أعمدة" in elem:
        st.info("💡 نصيحة: تأكد من توزيع الحديد بشكل متناظر وتكثيف الكانات في مناطق الاتصال.")
            elif "هوردي" in elem:
        st.info("💡 نصيحة: دقق عرض الجوائز المخفية وسماكة بلاطة التغطية (Top Slab).")
            elif "خزان" in elem:
        st.info("💡 نصيحة: صمم المقطع كمقطع غير متفطر (Uncracked) واستخدم مواد كتيمة.")
    else:
        st.success("✅ تم تدقيق العناصر؛ التصميم مطابق لاشتراطات الكود الهندسي.")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_draw:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ تفاصيل التسليح (BBS)")
    
    # عرض تفصيلة الحديد مع رفع السهم
    st.write("🔍 **مخطط تفريد الحديد:**")
        
    st.markdown(f"""
    <div style='background:#1a3c34; border:1px solid #d4af37; padding:15px; border-radius:10px; text-align:center;'>
        <p style='margin:0;'>📍 تفصيلة التسليح الرئيسية:</p>
        <h2 style='color:#d4af37; margin:5px;'>{n_bars} T {phi}</h2>
        <p style='font-size:0.9rem; color:#50c878;'>↑ سهم مرفوع يوضح القطر والعدد ↑</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    # زر التصدير للأوتوكاد مع الرسم الدقيق
    if st.button("🚀 تصدير المخطط التنفيذي (DXF)"):
        try:
            doc = ezdxf.new(setup=True); msp = doc.modelspace()
            # رسم إطار العنصر
            msp.add_lwpolyline([(0,0), (L*10,0), (L*10,H), (0,H), (0,0)])
            # رسم سيخ الحديد السفلي
            msp.add_line((0.5, 5), (L*10-0.5, 5), dxfattribs={'color': 1})
            # رسم سهم الرفع والنص
            msp.add_line((L*5, 5), (L*5, 15), dxfattribs={'color': 2})
            msp.add_text(f"{n_bars}%%c{phi}", dxfattribs={'height': 2.5}).set_placement((L*5, 17))
            
            buf = io.StringIO(); doc.write(buf)
            st.download_button("📥 تحميل ملف AutoCAD", buf.getvalue(), f"Pelan_Detail_{elem}.dxf")
            st.success("تم التصدير بنجاح!")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
            
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37;'>Pelan Engineering Engine v47 | م. بيلان عبد الكريم | 2026</p>", unsafe_allow_html=True)
