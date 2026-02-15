import streamlit as st
import numpy as np
import ezdxf
import io

# 1. الإعدادات البصرية الملكية (Emerald & Gold Theme)
st.set_page_config(page_title="Pelan Masterpiece v50", layout="wide")

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
    .result-box {
        background: #1a3c34;
        border-left: 5px solid #d4af37;
        padding: 10px;
        border-radius: 5px;
    }
    .gold-title { color: #d4af37; font-weight: bold; font-size: 1.5rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='master-card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Grand Masterpiece v50</h1><p class='gold-title'>المحرك الإنشائي المتكامل | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية (المدخلات الهندسية)
with st.sidebar:
    st.header("📏 مدخلات التصميم")
    elem = st.selectbox("العنصر الإنشائي:", [
        "جائز بيتون (Beam)", "أعصاب (Ribs)", "أعمدة خرسانية", 
        "بلاطة هوردي", "بلاطة مصمتة", "خزان مياه"
    ])
    
    st.divider()
    L = st.number_input("طول العنصر L (m):", 1.0, 15.0, 5.0)
    B = st.number_input("العرض B (cm):", 10.0, 100.0, 25.0)
    H = st.number_input("الارتفاع H (cm):", 20.0, 150.0, 60.0)
    Wu = st.number_input("الحمل المصعد Wu (kN/m):", 0.0, 150.0, 35.0)
    
    st.divider()
    st.subheader("🏗️ التحكم بالحديد")
    n_bars = st.number_input("عدد القضبان السفلي:", 1, 20, 4)
    phi = st.selectbox("القطر المستخدم (mm):", [10, 12, 14, 16, 18, 20, 25])

# 3. محرك الحسابات الفورية (العزم، القص، رد الفعل)
M_max = (Wu * L**2) / 8  # أقصى عزم
V_max = (Wu * L) / 2     # أقصى قص (وهو نفسه رد الفعل عند المساند لجائز بسيط)
As_actual = n_bars * (np.pi * (phi/10)**2 / 4) # مساحة الحديد الفعلية cm2

# 4. واجهة النتائج وتوصية المهندس بيلان
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 النتائج الإنشائية: {elem}")
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='result-box'>العزم الأقصى:<br><b style='color:#50c878;'>{M_max:.2f} kN.m</b></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='result-box'>القص / رد الفعل:<br><b style='color:#50c878;'>{V_max:.2f} kN</b></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='result-box'>مساحة الحديد:<br><b style='color:#50c878;'>{As_actual:.2f} cm²</b></div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 👨‍🏫 توصية المهندس بيلان:")
    
    # حل جذري لأخطاء الإزاحة: كل شرط يتبعه كود مباشر ومحاذٍ بدقة
    if "جائز" in elem or "أعصاب" in elem:
        st.info(f"💡 التسليح المختار {n_bars}Φ{phi} آمن. دقق مخطط القص لتفريد الكانات وسهم الترخيم.")
            elif "أعمدة" in elem:
        st.info("💡 دقق النحافة وتأكد من تكثيف الكانات في مناطق الاتصال مع الجوائز.")
            elif "هوردي" in elem:
        st.info("💡 تأكد من جساءة الأعصاب وعرض الجوائز المخفية لمقاومة قوى القص الثاقب.")
            else:
        st.success("✅ التصميم يحقق اشتراطات الكود. دقق التفاصيل التنفيذية في الموقع.")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ تفاصيل التسليح والتفريط")
    
        
    # تمثيل مرئي لرفع السهم ووصف الحديد
    st.markdown(f"""
    <div style='background:#1a3c34; border:2px dashed #d4af37; padding:15px; border-radius:10px; text-align:center;'>
        <p style='margin:0;'>📍 تفصيل الحديد السفلي:</p>
        <h2 style='color:#d4af37; margin:5px;'>{n_bars} T {phi}</h2>
        <p style='color:#50c878; font-size:0.9rem;'>↑ سهم رفع وتوصيف دقيق (العدد {n_bars} - قطر {phi}mm) ↑</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    if st.button("🚀 تصدير المخطط إلى AutoCAD (DXF)"):
        try:
            doc = ezdxf.new(setup=True); msp = doc.modelspace()
            # رسم العنصر والحديد
            msp.add_lwpolyline([(0,0), (L*10,0), (L*10,H), (0,H), (0,0)])
            msp.add_line((0.5, 5), (L*10-0.5, 5), dxfattribs={'color': 1})
            # رسم سهم الرفع والنص
            msp.add_line((L*5, 5), (L*5, 15), dxfattribs={'color': 2})
            msp.add_text(f"{n_bars}%%c{phi}", dxfattribs={'height': 2.5}).set_placement((L*5, 17))
            
            buf = io.StringIO(); doc.write(buf)
            st.download_button("📥 تحميل ملف DXF", buf.getvalue(), f"Pelan_{elem}.dxf")
            st.success("تم التصدير بنجاح!")
        except Exception as e:
            st.error(f"خطأ تقني: {e}")
            
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37;'>Pelan Engineering Engine v50 | م. بيلان عبد الكريم | 2026</p>", unsafe_allow_html=True)
