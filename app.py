import streamlit as st
import numpy as np
import ezdxf
import io

# إعدادات الهوية
ST_NAME = "بيلان مصطفى عبد الكريم"
ST_TEL = "0998449697"
ST_WORK = "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Structural v99", layout="wide")

# تصميم الواجهة الراقية
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        color: white;
    }}
    .calc-sheet {{
        background: rgba(255, 255, 255, 0.98);
        color: #1a1a1a;
        padding: 30px;
        border-radius: 15px;
        direction: rtl;
        border-right: 15px solid #d4af37;
    }}
    .pro-stamp {{
        border: 4px double #d4af37;
        padding: 15px;
        width: 320px;
        text-align: center;
        background: white;
        color: black;
        float: left;
        margin-top: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# القائمة الجانبية للمدخلات
with st.sidebar:
    st.header("📐 معايير المذكرة الحسابية")
    B = st.number_input("العرض B (cm):", 20, 100, 30)
    H = st.number_input("الارتفاع H (cm):", 20, 200, 60)
    L = st.number_input("البحر L (m):", 1.0, 20.0, 5.0)
    W = st.number_input("الحمل q (kN/m):", 1.0, 300.0, 50.0)
    st.divider()
    phi_bot = st.selectbox("قطر السفلي (mm):", [14, 16, 18, 20, 25], index=1)
    phi_top = st.selectbox("قطر العلوي (mm):", [10, 12, 14, 16], index=1)

# الحسابات الإنشائية (Structural Analysis)
Mu = (W * L**2) / 8
Vu = (W * L) / 2
R1 = R2 = Vu
d = H - 5
As_bot_req = (Mu * 1e6) / (0.87 * 420 * d * 10)
n_bot = max(2, int(np.ceil(As_bot_req / (np.pi * phi_bot**2 / 4))))
n_top = 2 # عدد قضبان التعليق الافتراضي

# دالة رسم أوتوكاد الشاملة (Sections + Diagrams)
def build_full_cad(b, h, l_m, w_kn, nb, pb, nt, pt, mu_val, vu_val):
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    scale = 10 # 1cm = 10mm
    
    # 1. رسم المقطع العرضي (Section)
    w_mm, h_mm, cv = b*scale, h*scale, 30
    msp.add_lwpolyline([(0,0),(w_mm,0),(w_mm,h_mm),(0,h_mm),(0,0)], dxfattribs={'color': 7}) # Concrete
    msp.add_lwpolyline([(cv,cv),(w_mm-cv,cv),(w_mm-cv,h_mm-cv),(cv,h_mm-cv),(cv,cv)], dxfattribs={'color': 3}) # Stirrup
    
    # رسم الحديد وتفريده
    dx_b = (w_mm-2*cv-20)/(nb-1 if nb>1 else 1)
    for i in range(nb):
        msp.add_circle((cv+10+i*dx_b, cv+10), radius=pb/2, dxfattribs={'color': 5})
    
    dx_t = (w_mm-2*cv-20)/(nt-1 if nt>1 else 1)
    for i in range(nt):
        msp.add_circle((cv+10+i*dx_t, h_mm-cv-10), radius=pt/2, dxfattribs={'color': 5})
    
    # 2. رسم مخطط العزم (BMD) - إزاحة لليمين
    offset = w_mm + 200
    msp.add_text("BENDING MOMENT DIAGRAM (kNm)", dxfattribs={'height': 20}).set_placement((offset, h_mm + 50))
    points = []
    for x in np.linspace(0, l_m, 20):
        m_at_x = (w_kn * x / 2) * (l_m - x)
        points.append((offset + x*100, -m_at_x)) # رسم العزم للأسفل
    msp.add_lwpolyline(points, dxfattribs={'color': 1})
    msp.add_text(f"Mmax = {mu_val:.1f}", dxfattribs={'height': 15}).set_placement((offset + (l_m*100/2), -mu_val-20))

    # 3. رسم مخطط القص (SFD)
    msp.add_text("SHEAR FORCE DIAGRAM (kN)", dxfattribs={'height': 20}).set_placement((offset, -mu_val - 100))
    sfd_y = -mu_val - 250
    msp.add_line((offset, sfd_y + vu_val), (offset + l_m*100, sfd_y - vu_val), dxfattribs={'color': 2})
    msp.add_line((offset, sfd_y), (offset + l_m*100, sfd_y), dxfattribs={'color': 7}) # Base line

    # إضافة البيانات المهنية
    msp.add_text(f"DESIGN BY: ENG. {ST_NAME}", dxfattribs={'height': 25}).set_placement((0, h_mm + 150))
    msp.add_text(f"TEL: {ST_TEL}", dxfattribs={'height': 20}).set_placement((0, h_mm + 100))
    
    return doc

# واجهة المستخدم
st.markdown(f"<h1 style='text-align:center; color:#d4af37;'>🏛️ Pelan Structural Analysis Office</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("<div class='calc-sheet'>", unsafe_allow_html=True)
    st.subheader("📑 المذكرة الحسابية الإنشائية")
    st.write(f"**أبعاد المقطع:** {B} x {H} cm")
    st.write(f"**طول المجاز:** {L} m")
    st.divider()
    st.write(f"📊 **عزم الانعطاف الأعظمي:** {Mu:.2f} kNm")
    st.write(f"📊 **قوة القص الأعظمية:** {Vu:.2f} kN")
    st.write(f"📊 **ردود الأفعال عند المساند:** {R1:.2f} kN")
    st.divider()
    st.markdown(f"✅ **تسليح الشد (السفلي):** {n_bot} T {phi_bot}")
    st.markdown(f"✅ **تسليح التعليق (العلوي):** {n_top} T {phi_top}")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.subheader("🖼️ الرسم التوضيحي وتفريد الحديد")
    
    
    
    st.markdown(f"**توزيع الحديد:** {n_bot} قضبان سفلية بقطر {phi_bot} ملم + {n_top} قضبان علوية بقطر {phi_top} ملم.")

    # الختم المحدث
    st.markdown(f"""
    <div class='pro-stamp'>
        <p style='margin:0; font-weight:bold; color:#16213e; font-size:17px;'>المهندس المدني</p>
        <p style='color:#d4af37; font-size:22px; font-weight:bold; margin:5px 0;'>{ST_NAME}</p>
        <p style='margin:0; font-size:14px; color:#444;'>{ST_WORK}</p>
        <p style='margin:5px 0; font-weight:bold; color:#d4af37;'>TEL: {ST_TEL}</p>
        <hr style='border:1px solid #d4af37; margin:10px;'>
        <p style='font-size:10px; color:#999;'>v99 - المذكرة الحسابية المتكاملة</p>
    </div>
    <div style='clear:both;'></div>
    """, unsafe_allow_html=True)

st.divider()
if st.button("🚀 تصدير المذكرة والرسوم والمخططات (AutoCAD DXF)"):
    full_dxf = build_full_cad(B, H, L, W, n_bot, phi_bot, n_top, phi_top, Mu, Vu)
    buf = io.StringIO()
    full_dxf.write(buf)
    st.download_button("📥 تحميل المخطط الإنشائي الشامل", buf.getvalue(), f"Structural_Calc_{ST_NAME}.dxf")
٠ج
