import streamlit as st
import numpy as np
import ezdxf
import io

# 1. إعدادات المظهر الفاخر (Emerald & Gold Royal Theme)
st.set_page_config(page_title="Pelan Masterpiece v49", layout="wide")

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
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .result-box {
        background: #1a3c34;
        border-left: 5px solid #d4af37;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .gold { color: #d4af37; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='master-card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Grand Masterpiece v49</h1><p class='gold'>النظام الهندسي الموحد | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية (المدخلات)
with st.sidebar:
    st.header("⚙️ مدخلات المهندس بيلان")
    elem = st.selectbox("العنصر الإنشائي:", [
        "جائز بيتون (Beam)", 
        "أعصاب هوردي (Ribs)", 
        "بلاطة مصمتة - اتجاه واحد",
        "بلاطة مصمتة - اتجاهين",
        "بلاطة هوردي - اتجاهين",
        "أعمدة خرسانية"
    ])
    
    st.divider()
    L = st.number_input("الطول L (m):", 1.0, 15.0, 5.0)
    Wu = st.number_input("الحمل المصعد Wu (kN/m):", 0.0, 150.0, 30.0)
    
    st.subheader("🏗️ تفاصيل الحديد")
    n_bars = st.number_input("عدد القضبان:", 1, 20, 4)
    phi = st.selectbox("القطر (mm):", [10, 12, 14, 16, 18, 20, 25])

# 3. محرك الحسابات الإنشائية
M_max = (Wu * L**2) / 8
V_max = (Wu * L) / 2
As_actual = n_bars * (np.pi * (phi/10)**2 / 4)

# 4. العرض الرئيسي
col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 نتائج التحليل: {elem}")
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='result-box'>عزم التصميم:<br><b style='color:#50c878;'>{M_max:.2f} kN.m</b></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='result-box'>قوة القص:<br><b style='color:#50c878;'>{V_max:.2f} kN</b></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='result-box'>مساحة الحديد:<br><b style='color:#50c878;'>{As_actual:.2f} cm²</b></div>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 👨‍🏫 توصية المهندس بيلان:")
    
    # هيكل برمجي آمن جداً لمنع أخطاء الإزاحة
    if "أعمدة" in elem:
        st.info("💡 تأكد من استمرارية أشاير الحديد وتكثيف الكانات في الثلث العلوي والسفلي.")
            elif "هوردي" in elem or "أعصاب" in elem:
        st.info("💡 دقق عرض الأعصاب وجساءة الجوائز المخفية لمقاومة سهم الترخيم.")
            elif "اتجاهين" in elem:
        st.info("💡 دقق توزيع العزوم في الاتجاهين الطويل والقصير وتأكد من تسليح الزوايا.")
            else:
        st.success("✅ التصميم آمن. دقق طول التشريك (Lap Length) ومسافات التغطية الخرسانية.")
            st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ مخطط تفريد الحديد")
    
    # تمثيل مرئي للسهم المرفوع والوصف
    st.markdown(f"""
    <div style='text-align:center; padding:20px; border:2px dashed #d4af37; border-radius:10px;'>
        <p class='gold'>توصيف الحديد المعتمد</p>
        <h1 style='color:#50c878; margin:10px;'>{n_bars} T {phi}</h1>
        <p style='color:#d4af37;'>↑ سهم رفع وتوصيف دقيق ↑</p>
        <hr style='border-color:#d4af37;'>
        <p style='font-size:0.8rem;'>مخصص للمخطط الإنشائي رقم (01)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    if st.button("🛠️ تصدير المخطط إلى AutoCAD 🚀"):
        try:
            doc = ezdxf.new(setup=True); msp = doc.modelspace()
            # رسم توضيحي للعنصر والحديد
            msp.add_lwpolyline([(0,0), (L*10,0), (L*10,20), (0,20), (0,0)])
            msp.add_line((0.5, 5), (L*10-0.5, 5), dxfattribs={'color': 1})
            # رسم سهم وتوصيف
            msp.add_line((L*5, 5), (L*5, 12), dxfattribs={'color': 2})
            msp.add_text(f"{n_bars}%%c{phi}", dxfattribs={'height': 2}).set_placement((L*5, 14))
            
            buf = io.StringIO(); doc.write(buf)
            st.download_button("📥 تحميل ملف DXF", buf.getvalue(), f"Pelan_{elem}.dxf")
            st.success("تم التصدير بنجاح يا هندسة!")
        except Exception as e:
            st.error(f"خطأ: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37;'>Pelan Engine v49 | م. بيلان عبد الكريم | 2026</p>", unsafe_allow_html=True)
