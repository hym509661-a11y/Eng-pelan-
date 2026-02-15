import streamlit as st
import numpy as np
import ezdxf
import io
from datetime import datetime

# 1. UI and Print Configuration
st.set_page_config(page_title="Eng. Pelan Office v80", layout="wide")
st.markdown("""
<style>
    @media print { .no-print { display: none !important; } .stApp { background: white !important; color: black !important; } }
    .stApp { background-color: #0b1619; color: #fff; }
    .report-card { background: #f8f9fa; color: #1a1a1a; border-right: 10px solid #d4af37; padding: 30px; border-radius: 5px; font-family: 'Arial'; direction: rtl; }
    .stamp-box { border: 3px double #d4af37; padding: 15px; width: 300px; text-align: center; margin-top: 50px; color: #1a1a1a; background: #fff; float: right; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { border: 1px solid #ddd; padding: 12px; text-align: right; }
    th { background-color: #eee; }
</style>
""", unsafe_allow_html=True)

# 2. Stable Sidebar (Using Latin Keys to prevent Syntax Errors)
with st.sidebar:
    st.markdown("<h2 class='no-print'>⚙️ إعدادات المشروع</h2>", unsafe_allow_html=True)
    p_name = st.text_input("اسم المشروع:", "مشروع تصميم إنشائي")
    p_owner = st.text_input("اسم المالك:", "مجمع المهندسين")
    
    # Mapping Arabic labels to English keys for stability
    cat_map = {"Concrete": "خرسانة (جوائز وأعمدة)", "Slabs": "بلاطات (Slabs)", "Footing": "أساسات (Foundations)", "Tanks": "خزانات مائية"}
    category = st.selectbox("العنصر الإنشائي:", list(cat_map.keys()), format_func=lambda x: cat_map[x])
    
    st.divider()
    B = st.number_input("العرض B (cm):", 20, 1000, 30)
    H = st.number_input("الارتفاع/السماكة H (cm):", 10, 1000, 60)
    L = st.number_input("الطول L (m):", 0.1, 100.0, 5.0)
    Load = st.number_input("الحمل المصمم (kN):", 1.0, 1000000.0, 150.0)
    phi = st.selectbox("القطر (mm):", [12, 14, 16, 18, 20, 25], index=2)

# 3. Calculation Engine (Audit-Safe Structure)
fy, fcu = 420, 25
area_bar = (np.pi * phi**2) / 4
res_list = []
detailing = ""

# Professional Calculation Logic
if category == "Concrete":
    M = (Load * L**2) / 8
    As = (M * 1e6) / (0.87 * fy * (H-5) * 10)
    n = max(2, int(np.ceil(As / area_bar)))
    res_list = [("الحمل المطبق", f"{Load} kN"), ("عزم الانعطاف", f"{M:.2f} kNm"), ("التسليح المطلوب", f"{n} T {phi}")]
    detailing = f"{n} T {phi}"

if category == "Slabs":
    M = (Load * L**2) / 10
    As = (M * 1e6) / (0.87 * fy * (H-3) * 10)
    n = max(5, int(np.ceil(As / area_bar)))
    res_list = [("سماكة البلاطة", f"{H} cm"), ("العزم المحسوب", f"{M:.2f} kNm/m'"), ("التسليح المعتمد", f"{n} T {phi} / m'")]
    detailing = f"{n} T {phi} / m'"

if category == "Footing":
    stress = Load / (B * L / 10000)
    n = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar)))
    res_list = [("أبعاد القاعدة", f"{B} x {L} cm"), ("إجهاد التربة", f"{stress:.2f} kN/m²"), ("التسليح", f"{n} T {phi} / m'")]
    detailing = f"{n} T {phi} @ 15cm"

if category == "Tanks":
    Mt = (10 * (H/100) * L**2) / 12
    n = max(7, int(np.ceil(((Mt * 1e6) / (0.87 * fy * (H-5) * 10)) / area_bar)))
    res_list = [("ضغط الماء", f"{10 * H/100:.2f} kN/m²"), ("عزم الجدار", f"{Mt:.2f} kNm"), ("تسليح الجدار", f"{n} T {phi} / m'")]
    detailing = f"{n} T {phi} / m'"

# 4. The Engineering Report (Print Ready)
st.markdown("<h1 style='text-align:center;' class='no-print'>🏗️ مكتب المهندس بيلان مصطفى عبدالكريم</h1>", unsafe_allow_html=True)

st.markdown(f"""
<div class="report-card">
    <div style="text-align: center; border-bottom: 2px solid #1a1a1a; padding-bottom: 10px;">
        <h2 style="margin:0;">المذكرة الحسابية الهندسية (v80)</h2>
        <p>تاريخ الإصدار: {datetime.now().strftime('%Y-%m-%d')}</p>
    </div>
    <div style="margin-top: 20px;">
        <p><b>المشروع:</b> {p_name} | <b>المالك:</b> {p_owner}</p>
        <p><b>العنصر المدروس:</b> {cat_map[category]}</p>
    </div>
    <table>
        <tr><th>الوصف الهندسي</th><th>القيمة والوحدة</th></tr>
""", unsafe_allow_html=True)

for label, val in res_list:
    st.markdown(f"<tr><td>{label}</td><td><b>{val}</b></td></tr>", unsafe_allow_html=True)

st.markdown(f"""
    </table>
    <div style="margin-top: 20px; padding: 15px; background: #fff; border: 1px dashed #d4af37;">
        <p style="margin:0; color:#d4af37; font-weight:bold;">توصيف التسليح النهائي:</p>
        <p style="font-size: 26px; font-weight: bold; margin: 10px 0; color:#1a1a1a;">{detailing}</p>
    </div>
""", unsafe_allow_html=True)

# Image Triggering
if category == "Tanks":
    elif category == "Footing":
    else:
    
# الختم الرسمي الهندسي
st.markdown(f"""
    <div class="stamp-box">
        <p style="margin:0; font-weight:bold; font-size:18px;">المهندس المدني</p>
        <p style="margin:5px 0; font-size:20px; color:#d4af37; font-weight:bold;">بيلان مصطفى عبدالكريم</p>
        <p style="margin:0; font-size:14px;">دراسة - إشراف - تعهدات</p>
        <div style="margin-top:10px; border-top:1px solid #d4af37; padding-top:5px; font-size:12px;">توقيع المكتب المعتمد</div>
    </div>
    <div style="clear:both;"></div>
</div>
""", unsafe_allow_html=True)

# 5. Buttons
st.divider()
c1, c2 = st.columns(2)
with c1: st.button("🖨️ طباعة المذكرة (Print)", on_click=None)
with c2:
    if st.button("🚀 Export AutoCAD"):
        doc = ezdxf.new(setup=True); doc.modelspace().add_text(f"ENG. PELAN - {p_name}", dxfattribs={'height': 5})
        buf = io.StringIO(); doc.write(buf)
        st.download_button("📥 تحميل DXF", buf.getvalue(), "Pelan_Drawing.dxf")

st.markdown("<p style='text-align:center; color:gray;' class='no-print'>تم التدقيق والختم إلكترونياً © 2026</p>", unsafe_allow_html=True)
