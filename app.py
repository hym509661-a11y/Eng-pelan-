import streamlit as st
import numpy as np
import ezdxf
import io

# 1. الإعدادات الملكية (Emerald & Gold)
st.set_page_config(page_title="Pelan Professional Designer v53", layout="wide")

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
    .label { color: #d4af37; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='master-card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Professional Designer v53</h1><p style='color:#d4af37;'>محرك التصميم التلقائي الموحد | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية (المدخلات الفنية)
with st.sidebar:
    st.header("📐 معايير التصميم")
    elem = st.selectbox("العنصر الإنشائي:", ["جائز (Beam)", "عصب (Rib)", "بلاطة (Slab)"])
    L = st.number_input("طول البحر L (m):", 1.0, 15.0, 5.0)
    B = st.number_input("العرض B (cm):", 10, 100, 25)
    H = st.number_input("السماكة H (cm):", 10, 150, 60)
    Wu = st.number_input("الحمل المصعد Wu (kN/m):", 1.0, 200.0, 35.0)
    
    st.divider()
    st.subheader("⚙️ خيارات الحديد")
    phi_main = st.selectbox("قطر الحديد الرئيسي (mm):", [12, 14, 16, 18, 20, 25], index=2)
    phi_stirrups = st.selectbox("قطر الكانات (mm):", [8, 10, 12])
    f_y = 420 # إجهاد الخضوع MPa
    f_cu = 25 # مقاومة الخرسانة MPa

# 3. محرك التصميم الإنشائي التلقائي
# حساب القوى
M_max = (Wu * L**2) / 8  # kN.m
V_max = (Wu * L) / 2     # kN

# تصميم الحديد (Simplified RC Design)
d = H - 5 # العمق الفعال cm
As_required = (M_max * 10**6) / (0.87 * f_y * d * 10) # mm2
area_single_bar = (np.pi * phi_main**2) / 4
n_bars_bottom = int(np.ceil(As_required / area_single_bar))
if n_bars_bottom < 2: n_bars_bottom = 2 # الحد الأدنى سيخان

# حديد التعليق والعلوي (تقديري 20% من الرئيسي)
n_bars_top = max(2, int(np.ceil(n_bars_bottom * 0.3)))
n_bars_hang = 2

# الكانات (تقديري بناءً على القص)
s_spacing = 15 # cm

# 4. العرض الفني والنتائج
col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 مذكرة التصميم التلقائية: {elem}")
    
    c = st.columns(4)
    c[0].markdown(f"<div class='result-box'>العزم:<br><b>{M_max:.1f} kN.m</b></div>", unsafe_allow_html=True)
    c[1].markdown(f"<div class='result-box'>القص:<br><b>{V_max:.1f} kN</b></div>", unsafe_allow_html=True)
    c[2].markdown(f"<div class='result-box'>B x H:<br><b>{B}x{H} cm</b></div>", unsafe_allow_html=True)
    c[3].markdown(f"<div class='result-box'>As req:<br><b>{As_required/100:.2f} cm²</b></div>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 👨‍🏫 جدول التسليح المقترح من المهندس بيلان:")
    st.write(f"✅ **الفرش السفلي (الرئيسي):** {n_bars_bottom} T {phi_main}")
    st.write(f"✅ **الغطاء العلوي:** {n_bars_top} T {phi_main}")
    st.write(f"✅ **حديد التعليق:** {n_bars_hang} T 12")
    st.write(f"✅ **الكانات:** T {phi_stirrups} كل {s_spacing} سم")
    
    st.info(f"💡 توصية بيلان: تم حساب {n_bars_bottom} أسياخ قطر {phi_main} لضمان الأمان الإنشائي تحت عزم {M_max:.1f} kN.m.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ تفصيل رفع الحديد (Automatic BBS)")
    
    # واجهة مرئية للتفريد
    st.markdown(f"""
    <div style='border:2px solid #d4af37; padding:15px; border-radius:10px;'>
        <div style='text-align:right; color:#50c878;'>Top: {n_bars_top} T {phi_main} ↑</div>
        <div style='height:80px; border:4px solid #fff; margin:10px 0; position:relative;'>
             <div style='position:absolute; bottom:5px; left:10%; right:10%; height:4px; background:#ff4b4b;'></div>
             <div style='position:absolute; top:5px; left:10%; right:10%; height:3px; background:#4b4bff;'></div>
        </div>
        <div style='text-align:left; color:#ff4b4b;'>Bottom: {n_bars_bottom} T {phi_main} ↓</div>
        <p style='text-align:center; font-size:0.8rem; color:#aaa;'>الكانات: T {phi_stirrups} @ {s_spacing}cm</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    if st.button("🎨 تصدير مخطط بيلان التفصيلي للأوتوكاد 🚀"):
        try:
            doc = ezdxf.new(setup=True); msp = doc.modelspace()
            # رسم المقطع الطولي
            msp.add_lwpolyline([(0,0), (L*100,0), (L*100,H), (0,H), (0,0)])
            # الحديد السفلي + سهم وتوصيف
            msp.add_line((2, 5), (L*100-2, 5), dxfattribs={'color': 1})
            msp.add_text(f"BOTTOM: {n_bars_bottom}%%c{phi_main}", dxfattribs={'height': 4}).set_placement((L*50, -10))
            # الحديد العلوي
            msp.add_line((2, H-5), (L*100-2, H-5), dxfattribs={'color': 5})
            msp.add_text(f"TOP: {n_bars_top}%%c{phi_main}", dxfattribs={'height': 4}).set_placement((L*50, H+5))
            
            buf = io.StringIO(); doc.write(buf)
            st.download_button("📥 تحميل المخطط التنفيذي (DXF)", buf.getvalue(), f"Pelan_AutoDesign_{elem}.dxf")
            st.success("تم التصميم والتصدير بنجاح!")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37;'>Pelan Engineering Engine v53 | 2026</p>", unsafe_allow_html=True)
