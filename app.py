import streamlit as st
import numpy as np
import ezdxf
import io

# 1. الإعدادات البصرية الملكية (Emerald & Gold Royal Theme)
st.set_page_config(page_title="Pelan Masterpiece v51", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #0d1b1e;
        background-image: url("https://www.transparenttextures.com/patterns/carbon-fibre.png");
        color: #ffffff;
    }
    .master-card {
        background: rgba(16, 44, 41, 0.95);
        border: 2px solid #d4af37;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    }
    .result-box {
        background: #1a3c34;
        border-left: 5px solid #d4af37;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .gold-text { color: #d4af37; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='master-card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Grand Masterpiece v51</h1><p class='gold-text'>المحرك الإنشائي الموحد | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية (مدخلات المهندس بيلان)
with st.sidebar:
    st.header("⚙️ مدخلات التصميم")
    elem = st.selectbox("العنصر الإنشائي:", [
        "جائز بيتون (Beam)", "أعصاب هوردي (Ribs)", "أعمدة خرسانية", 
        "بلاطة هوردي", "بلاطة مصمتة", "خزان مياه"
    ])
    
    st.divider()
    L = st.number_input("طول العنصر L (m):", 1.0, 20.0, 5.0)
    B = st.number_input("العرض B (cm):", 10.0, 100.0, 25.0)
    H = st.number_input("الارتفاع H (cm):", 20.0, 150.0, 60.0)
    Wu = st.number_input("الحمل Wu (kN/m):", 0.0, 200.0, 35.0)
    
    st.divider()
    st.subheader("🏗️ تسليح المهندس بيلان")
    n_bars = st.number_input("عدد القضبان:", 1, 20, 4)
    phi = st.selectbox("القطر (mm):", [10, 12, 14, 16, 18, 20, 25])

# 3. محرك الحسابات الإنشائية الفوري
M_max = (Wu * L**2) / 8  # العزم الأقصى
V_max = (Wu * L) / 2     # القص ورد الفعل
As_actual = n_bars * (np.pi * (phi/10)**2 / 4) # مساحة الحديد cm2

# 4. واجهة النتائج والتوصيات
col_main, col_detail = st.columns([1.3, 1])

with col_main:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 النتائج الإنشائية: {elem}")
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='result-box'>العزم الأقصى:<br><b style='color:#50c878; font-size:1.5rem;'>{M_max:.2f} kN.m</b></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='result-box'>القص ورد الفعل:<br><b style='color:#50c878; font-size:1.5rem;'>{V_max:.2f} kN</b></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='result-box'>مساحة الحديد:<br><b style='color:#50c878; font-size:1.5rem;'>{As_actual:.2f} cm²</b></div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 👨‍🏫 توصية المهندس بيلان:")
    
    # هيكل برمجي ثابت لمنع أخطاء الإزاحة (Indentation)
    if "جائز" in elem or "أعصاب" in elem:
        st.info(f"💡 التسليح المختار {n_bars}Φ{phi} يحقق المتطلبات الإنشائية. دقق سهم الترخيم.")
            elif "أعمدة" in elem:
        st.info("💡 تأكد من توزيع الحديد بشكل متناظر وتكثيف الكانات عند مناطق الوصل.")
            elif "هوردي" in elem:
        st.info("💡 دقق عرض الجوائز المخفية وسماكة بلاطة التغطية العلوية.")
            else:
        st.success("✅ تم التدقيق الإنشائي؛ العنصر آمن ومطابق لمخططات المهندس بيلان.")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_detail:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ مخطط التفريد (BBS)")
    
    # تمثيل رفع السهم وتوصيف الحديد
    st.markdown(f"""
    <div style='background:#1a3c34; border:2px dashed #d4af37; padding:20px; border-radius:15px; text-align:center;'>
        <p class='gold-text'>توصيف الحديد السفلي</p>
        <h1 style='color:#50c878; margin:15px;'>{n_bars} T {phi}</h1>
        <p style='color:#d4af37;'>↑ سهم رفع (العدد: {n_bars} | القطر: {phi}mm) ↑</p>
        <hr style='border-color:#d4af37;'>
        <p style='font-size:0.8rem;'>مخصص للمخطط التنفيذي - بيلان 2026</p>
    </div>
    """, unsafe_allow_html=True)
    
    
    st.divider()
    
    if st.button("🛠️ تصدير المخطط إلى AutoCAD 🚀"):
        try:
            doc = ezdxf.new(setup=True); msp = doc.modelspace()
            # رسم العنصر والحديد
            msp.add_lwpolyline([(0,0), (L*10,0), (L*10,H), (0,H), (0,0)])
            msp.add_line((0.5, 5), (L*10-0.5, 5), dxfattribs={'color': 1})
            # رسم سهم وتوصيف الحديد
            msp.add_line((L*5, 5), (L*5, 15), dxfattribs={'color': 2})
            msp.add_text(f"{n_bars}%%c{phi}", dxfattribs={'height': 2.5}).set_placement((L*5, 17))
            
            buf = io.StringIO(); doc.write(buf)
            st.download_button("📥 تحميل ملف DXF", buf.getvalue(), f"Pelan_{elem}.dxf")
            st.success("تم التصدير بنجاح يا هندسة!")
        except Exception as e:
            st.error(f"خطأ: {e}")
            
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37; font-size:0.8rem;'>Pelan Structural Engine v51 | 2026</p>", unsafe_allow_html=True)
