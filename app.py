import streamlit as st
import numpy as np
import ezdxf
import io

# 1. الإعدادات البصرية الملكية
st.set_page_config(page_title="Pelan Masterpiece v52", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0d1b1e; color: #ffffff; }
    .master-card {
        background: rgba(16, 44, 41, 0.95);
        border: 2px solid #d4af37;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .result-box {
        background: #1a3c34; border-left: 5px solid #d4af37;
        padding: 10px; border-radius: 5px; margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='master-card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Grand Masterpiece v52</h1><p style='color:#d4af37;'>المحرك الإنشائي المتكامل | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية (المدخلات)
with st.sidebar:
    st.header("⚙️ مدخلات المهندس بيلان")
    elem = st.selectbox("العنصر الإنشائي:", [
        "جائز بيتون (Beam)", "أعصاب هوردي (Ribs)", "أعمدة خرسانية", 
        "بلاطة مصمتة (1-Way)", "بلاطة مصمتة (2-Way)", "بلاطة هوردي (2-Way)"
    ])
    L = st.number_input("الطول L (m):", 1.0, 15.0, 5.0)
    Wu = st.number_input("الحمل Wu (kN/m):", 0.0, 150.0, 30.0)
    st.divider()
    n_bars = st.number_input("عدد القضبان:", 1, 20, 4)
    phi = st.selectbox("القطر (mm):", [10, 12, 14, 16, 18, 20, 25])

# 3. محرك الحسابات
M_max = (Wu * L**2) / 8
V_max = (Wu * L) / 2
As_actual = n_bars * (np.pi * (phi/10)**2 / 4)

# 4. العرض الفني (بدون شروط معقدة لمنع أخطاء الإزاحة)
col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 النتائج الإنشائية: {elem}")
    
    res_cols = st.columns(3)
    res_cols[0].markdown(f"<div class='result-box'>العزم:<br><b style='color:#50c878;'>{M_max:.2f} kN.m</b></div>", unsafe_allow_html=True)
    res_cols[1].markdown(f"<div class='result-box'>القص:<br><b style='color:#50c878;'>{V_max:.2f} kN</b></div>", unsafe_allow_html=True)
    res_cols[2].markdown(f"<div class='result-box'>الحديد:<br><b style='color:#50c878;'>{As_actual:.2f} cm²</b></div>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 👨‍🏫 توصية المهندس بيلان:")
    st.info(f"💡 تم تحليل {elem} بطول {L}m. التسليح المعتمد هو {n_bars} قضبان بقطر {phi}mm. تأكد من مطابقة التنفيذ لمخططات القص والعزم.")
    
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ تفصيل التسليح (BBS)")
    
    
    
    st.markdown(f"""
    <div style='text-align:center; padding:15px; border:2px dashed #d4af37; border-radius:10px;'>
        <p style='color:#d4af37;'>توصيف الحديد المرفوع</p>
        <h2 style='color:#50c878;'>{n_bars} Φ {phi}</h2>
        <p style='color:#d4af37;'>↑ سهم رفع وتوصيف دقيق ↑</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🛠️ تصدير المخطط إلى AutoCAD 🚀"):
        try:
            doc = ezdxf.new(setup=True)
            msp = doc.modelspace()
            msp.add_lwpolyline([(0,0), (L*10,0), (L*10,20), (0,20), (0,0)])
            msp.add_line((0.5, 5), (L*10-0.5, 5), dxfattribs={'color': 1})
            msp.add_line((L*5, 5), (L*5, 12), dxfattribs={'color': 2})
            msp.add_text(f"{n_bars}%%c{phi}", dxfattribs={'height': 2}).set_placement((L*5, 14))
            buf = io.StringIO()
            doc.write(buf)
            st.download_button("📥 تحميل DXF", buf.getvalue(), f"Pelan_{elem}.dxf")
            st.success("تم التصدير بنجاح!")
        except Exception as e:
            st.error(f"خطأ: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37;'>Pelan Engine v52 | م. بيلان عبد الكريم | 2026</p>", unsafe_allow_html=True)
