import streamlit as st
import numpy as np
import ezdxf
import io

# الهوية والختم (0998449697)
ST_NAME, ST_TEL = "بيلان مصطفى عبد الكريم", "0998449697"
ST_WORK = "المهندس المدني - دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan CAD v97", layout="wide")

# لوحة التحكم
with st.sidebar:
    st.header("🏗️ مدخلات الحساب والرسم")
    mode = st.selectbox("العنصر:", ["جائز (Beam)", "عمود (Column)"])
    B = st.number_input("العرض B (cm):", 20, 100, 30)
    H = st.number_input("الارتفاع H (cm):", 20, 200, 60)
    L = st.number_input("الطول L (m):", 1.0, 15.0, 5.0)
    W = st.number_input("الحمل الموزع (kN/m):", 1.0, 200.0, 40.0)
    phi_bot = st.selectbox("قطر السفلي (mm):", [14, 16, 18, 20, 25])
    phi_top = st.selectbox("قطر العلوي (mm):", [10, 12, 14])

# 1. محرك الحسابات التلقائي
Mu = (W * L**2) / 8  # العزم التصميمي
# حساب تقريبي لعدد القضبان (As = Mu / (0.87 * fy * d))
d = H - 5 # الفعّال
As_req = (Mu * 1e6) / (0.87 * 420 * d * 10) 
n_calc = int(np.ceil(As_req / (np.pi * phi_bot**2 / 4)))
if n_calc < 2: n_calc = 2
n_top_fixed = 2 # حديد تعليق ثابت

# 2. محرك رسم AutoCAD التلقائي (تفريد كامل)
def generate_cad_detail(b_cm, h_cm, nb, pb, nt, pt):
    doc = ezdxf.new(setup=True); msp = doc.modelspace()
    w, hi, cv = b_cm*10, h_cm*10, 30 # مقاسات بالملم
    # رسم المقطع والكانة
    msp.add_lwpolyline([(0,0),(w,0),(w,hi),(0,hi),(0,0)], dxfattribs={'color': 7}) # خرسانة
    msp.add_lwpolyline([(cv,cv),(w-cv,cv),(w-cv,hi-cv),(cv,hi-cv),(cv,cv)], dxfattribs={'color': 3}) # كانة
    # رسم وتوصيف السفلي
    dx_b = (w-2*cv-20)/(nb-1 if nb>1 else 1)
    for i in range(nb):
        msp.add_circle((cv+10+i*dx_b, cv+10), radius=pb/2, dxfattribs={'color': 5})
    msp.add_line((w/2, cv), (w/2+50, -50), dxfattribs={'color': 1}) # سهم
    msp.add_text(f"{nb} T {pb} (MAIN BARS)", dxfattribs={'height': 15}).set_placement((w/2+55, -65))
    # رسم وتوصيف العلوي
    dx_t = (w-2*cv-20)/(nt-1 if nt>1 else 1)
    for i in range(nt):
        msp.add_circle((cv+10+i*dx_t, hi-cv-10), radius=pt/2, dxfattribs={'color': 5})
    msp.add_line((w/2, hi-cv), (w/2+50, hi+50), dxfattribs={'color': 1})
    msp.add_text(f"{nt} T {pt} (STIRRUP HANGERS)", dxfattribs={'height': 15}).set_placement((w/2+55, hi+55))
    # الختم
    msp.add_text(f"ENG. {ST_NAME} - {ST_TEL}", dxfattribs={'height': 20}).set_placement((0, hi+100))
    return doc

# واجهة العرض
st.markdown(f"<h1 style='text-align:center; color:#d4af37;'>🏢 Pelan Auto-CAD System v97</h1>", unsafe_allow_html=True)

c1, c2 = st.columns([1, 1.2])
with c1:
    st.subheader("📑 النتائج الحسابية")
    st.info(f"العزم المحسوب: {Mu:.2f} kNm")
    st.success(f"العدد المطلوب تلقائياً: {n_calc} قضبان T{phi_bot}")
    
    st.markdown(f"""
    <div style='border:2px solid #d4af37; padding:15px; background:white; color:black; direction:rtl;'>
        <b>الختم الهندسي:</b><br>
        {ST_NAME}<br>{ST_WORK}<br><b>TEL: {ST_TEL}</b>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.subheader("🖋️ معاينة المقطع (Preview)")
    st.write(f"المقطع: {B}x{H} سم")
    st.write(f"تسليح سفلي: {n_calc} T {phi_bot}")
    st.write(f"تسليح علوي: {n_top_fixed} T {phi_top}")
    # رسم توضيحي
    st.code(f"|----------------|\n|  o    {n_top_fixed}T{phi_top}    o  |\n|                |\n|  o  o  {n_calc}T{phi_bot}  o  o |\n|----------------|", language="text")

st.divider()
if st.button("🚀 توليد وتنزيل مخطط أوتوكاد (DXF)"):
    dxf_doc = generate_cad_detail(B, H, n_calc, phi_bot, n_top_fixed, phi_top)
    buf = io.StringIO(); dxf_doc.write(buf)
    st.download_button("📥 تحميل ملف AutoCAD الجاهز", buf.getvalue(), f"Pelan_{mode}_Design.dxf")
