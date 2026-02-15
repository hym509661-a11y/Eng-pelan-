import streamlit as st
import numpy as np
import ezdxf
import io

# إعدادات الهوية
ST_NAME = "بيلان مصطفى عبد الكريم"
ST_TEL = "0998449697"
ST_WORK = "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Elite v98", layout="wide")

# تصميم الخلفية الراقية والواجهة
st.markdown(f"""
<style>
    /* خلفية راقية متدرجة */
    .stApp {{
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }}
    .main-panel {{
        background: rgba(255, 255, 255, 0.95);
        color: #1a1a1a;
        padding: 30px;
        border-radius: 15px;
        direction: rtl;
        border-right: 15px solid #d4af37;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    /* الختم الجديد */
    .pro-stamp {{
        border: 4px double #d4af37;
        padding: 15px;
        width: 320px;
        text-align: center;
        background: white;
        color: black;
        float: left;
        margin-top: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }}
    .stButton>button {{
        background-color: #d4af37;
        color: white;
        border-radius: 8px;
        border: none;
        width: 100%;
    }}
</style>
""", unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.header("📐 معايير التصميم")
    mode = st.selectbox("العنصر الإنشائي:", ["جائز (Beam)", "عمود (Column)"])
    B = st.number_input("العرض B (cm):", 20, 100, 30)
    H = st.number_input("الارتفاع H (cm):", 20, 200, 60)
    L = st.number_input("الطول L (m):", 1.0, 15.0, 5.0)
    W = st.number_input("الحمل الموزع (kN/m):", 1.0, 200.0, 45.0)
    phi_bot = st.selectbox("قطر السفلي (mm):", [14, 16, 18, 20, 25], index=1)

# المحرك الإنشائي (الحساب التلقائي)
Mu = (W * L**2) / 8
d = H - 5
As_req = (Mu * 1e6) / (0.87 * 420 * d * 10)
n_calc = int(np.ceil(As_req / (np.pi * phi_bot**2 / 4)))
n_calc = max(2, n_calc)
n_top = 2 # حديد تعليق

# دالة رسم AutoCAD
def build_autocad(b, h, nb, pb, nt, pt):
    doc = ezdxf.new(setup=True); msp = doc.modelspace()
    w, hi, cv = b*10, h*10, 30
    # رسم الخرسانة والكانة
    msp.add_lwpolyline([(0,0),(w,0),(w,hi),(0,hi),(0,0)], dxfattribs={'color': 7})
    msp.add_lwpolyline([(cv,cv),(w-cv,cv),(w-cv,hi-cv),(cv,hi-cv),(cv,cv)], dxfattribs={'color': 3})
    # رسم الحديد السفلي وتوصيفه
    step_b = (w-2*cv-20)/(nb-1 if nb>1 else 1)
    for i in range(nb):
        msp.add_circle((cv+10+i*step_b, cv+10), radius=pb/2, dxfattribs={'color': 5})
    msp.add_text(f"{nb} T {pb} (MAIN)", dxfattribs={'height': 15}).set_placement((w+20, 20))
    # رسم الحديد العلوي
    step_t = (w-2*cv-20)/(nt-1 if nt>1 else 1)
    for i in range(nt):
        msp.add_circle((cv+10+i*step_t, hi-cv-10), radius=6, dxfattribs={'color': 5})
    # إضافة الاسم والرقم في الملف
    msp.add_text(f"ENG. {ST_NAME} - {ST_TEL}", dxfattribs={'height': 20}).set_placement((0, hi+50))
    return doc

# واجهة المستخدم
st.markdown(f"<h1 style='text-align:center; color:#d4af37;'>🏛️ Pelan Elite Structural Office</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("<div class='main-panel'>", unsafe_allow_html=True)
    st.subheader("📑 التقرير الفني الذكي")
    st.write(f"**العنصر:** {mode}")
    st.write(f"**العزم التصميمي:** {Mu:.2f} kNm")
    st.divider()
    st.markdown(f"✅ **العدد المطلوب:** <span style='color:#d4af37; font-size:24px;'>{n_calc} T {phi_bot}</span>", unsafe_allow_html=True)
    st.write(f"✅ **حديد التعليق:** 2 T 12")
    st.write(f"✅ **الكانات:** Φ 8 @ 15cm")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.subheader("🖋️ مخطط تفريد الحديد")
    # تمثيل مرئي بسيط
    st.code(f"Section: {B}x{H} cm\nMain: {n_calc}T{phi_bot}\nHangers: 2T12", language="text")
    
    # الختم المحدث
    st.markdown(f"""
    <div class='pro-stamp'>
        <p style='margin:0; font-weight:bold; color:#2c5364; font-size:16px;'>المهندس المدني</p>
        <p style='color:#d4af37; font-size:22px; font-weight:bold; margin:5px 0;'>{ST_NAME}</p>
        <p style='margin:0; font-size:14px; color:#555;'>{ST_WORK}</p>
        <p style='margin:5px 0; font-weight:bold; color:#d4af37;'>TEL: {ST_TEL}</p>
        <hr style='border:1px solid #d4af37; margin:10px;'>
        <p style='font-size:10px; color:#888;'>v98 - التصميم الإنشائي المتكامل</p>
    </div>
    <div style='clear:both;'></div>
    """, unsafe_allow_html=True)

st.divider()
if st.button("🚀 تصدير المخطط التفصيلي تلقائياً (AutoCAD DXF)"):
    dxf_file = build_autocad(B, H, n_calc, phi_bot, n_top, 12)
    buf = io.StringIO()
    dxf_file.write(buf)
    st.download_button("📥 تحميل ملف المخطط الجاهز", buf.getvalue(), f"Pelan_{ST_NAME}.dxf")
