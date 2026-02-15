import streamlit as st
import numpy as np
import ezdxf
import io
from datetime import datetime

# 1. إعدادات الواجهة والطباعة
st.set_page_config(page_title="Eng. Pelan Office", layout="wide")
st.markdown("""
<style>
    @media print {
        .no-print { display: none !important; }
        .stApp { background-color: white !important; color: black !important; }
        .card { border: 1px solid #000 !important; margin: 0 !important; padding: 10px !important; }
    }
    .stApp { background-color: #0b1619; color: #fff; }
    .report-card { background: #f8f9fa; color: #1a1a1a; border-left: 10px solid #d4af37; padding: 30px; border-radius: 5px; font-family: 'Arial'; }
    .stamp-box { border: 3px double #d4af37; padding: 15px; width: 300px; text-align: center; margin-top: 50px; float: left; color: #1a1a1a; background: #fff; }
    .gold-text { color: #d4af37; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 2. لوحة التحكم الجانبية (مدخلات المشروع)
with st.sidebar:
    st.markdown("<h2 class='no-print'>⚙️ إعدادات المذكرة</h2>", unsafe_allow_html=True)
    project_name = st.text_input("اسم المشروع:", "فيلا سكنية - نموذج A")
    owner_name = st.text_input("اسم المالك:", "مجمع المهندسين")
    category = st.selectbox("العنصر الإنشائي:", ["خرسانة (جوائز وأعمدة)", "بلاطات (Slabs)", "أساسات (Foundations)", "خزانات مائية"])
    
    st.divider()
    B = st.number_input("العرض B (cm):", 20, 1000, 30)
    H = st.number_input("الارتفاع/السماكة H (cm):", 10, 1000, 60)
    L = st.number_input("الطول L (m):", 0.1, 100.0, 5.0)
    Load = st.number_input("الحمل المصمم (kN):", 1.0, 1000000.0, 150.0)
    phi = st.selectbox("القطر (mm):", [12, 14, 16, 18, 20, 25], index=2)

# 3. محرك الحسابات الهندسية
f_y, f_cu = 420, 25
area_bar = (np.pi * phi**2) / 4
results = []
detailing = ""

if "خرسانة" in category:
    M = (Load * L**2) / 8
    As = (M * 1e6) / (0.87 * f_y * (H-5) * 10)
    n = max(2, int(np.ceil(As / area_bar)))
    results = [
        ("الحمل المطبق (Ultimate Load)", f"{Load} kN"),
        ("عزم الانعطاف (Moment)", f"{M:.2f} kNm"),
        ("مساحة الحديد المطلوبة (As)", f"{As:.1f} mm²"),
        ("التسليح المقترح", f"{n} T {phi}")
    ]
    detailing = f"{n} T {phi}"

elif "بلاطات" in category:
    M = (Load * L**2) / 10
    As = (M * 1e6) / (0.87 * f_y * (H-3) * 10)
    n = max(5, int(np.ceil(As / area_bar)))
    results = [
        ("سماكة البلاطة", f"{H} cm"),
        ("عزم البلاطة", f"{M:.2f} kNm/m'"),
        ("التسليح المعتمد/م", f"{n} T {phi}")
    ]
    detailing = f"{n} T {phi} / m'"

elif "أساسات" in category:
    stress = Load / (B * L / 10000)
    n = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar)))
    results = [
        ("أبعاد القاعدة", f"{B} x {L} cm"),
        ("إجهاد التربة المحسوب", f"{stress:.2f} kN/m²"),
        ("تسليح القاعدة (اتجاهين)", f"{n} T {phi} / m'")
    ]
    detailing = f"{n} T {phi} @ 15cm"

else: # خزانات
    Mt = (10 * (H/100) * L**2) / 12
    n = max(7, int(np.ceil(((Mt * 1e6) / (0.87 * f_y * (H-5) * 10)) / area_bar)))
    results = [
        ("ضغط الماء التصميمي", f"{10 * H/100:.2f} kN/m²"),
        ("العزم المؤثر على الجدار", f"{Mt:.2f} kNm"),
        ("تسليح جدار الخزان", f"{n} T {phi} / m'")
    ]
    detailing = f"{n} T {phi} / m'"

# 4. المذكرة الحسابية الجاهزة للطباعة
st.markdown("<h1 style='text-align:center;' class='no-print'>📂 المكتب الهندسي - م. بيلان مصطفى</h1>", unsafe_allow_html=True)

# الجزء القابل للطباعة
st.markdown(f"""
<div class="report-card">
    <div style="text-align: center; border-bottom: 2px solid #1a1a1a; padding-bottom: 10px;">
        <h2 style="margin:0;">المذكرة الحسابية الإنشائية</h2>
        <p>التاريخ: {datetime.now().strftime('%Y-%m-%d')}</p>
    </div>
    
    <div style="margin-top: 20px;">
        <p><b>اسم المشروع:</b> {project_name}</p>
        <p><b>اسم المالك:</b> {owner_name}</p>
        <p><b>العنصر المدروس:</b> {category}</p>
    </div>

    <table style="width:100%; margin-top: 20px; border-collapse: collapse;">
        <tr style="background: #eee;">
            <th style="border: 1px solid #ddd; padding: 12px; text-align: right;">الوصف البرمجي</th>
            <th style="border: 1px solid #ddd; padding: 12px; text-align: right;">القيمة التصميمية</th>
        </tr>
""", unsafe_allow_html=True)

for label, value in results:
    st.markdown(f"""
        <tr>
            <td style="border: 1px solid #ddd; padding: 10px;">{label}</td>
            <td style="border: 1px solid #ddd; padding: 10px; font-weight: bold;">{value}</td>
        </tr>
    """, unsafe_allow_html=True)

st.markdown(f"""
    </table>
    
    <div style="margin-top: 20px; padding: 15px; background: #fff; border: 1px dashed #d4af37;">
        <h3 style="margin:0; color:#d4af37;">التوصيف الفني للتسليح (BBS):</h3>
        <p style="font-size: 24px; font-weight: bold; margin: 10px 0;">{detailing}</p>
    </div>
""", unsafe_allow_html=True)

# إضافة صورة توضيحية حسب العنصر
if "خزانات" in category:
    
elif "أساسات" in category:
    
else:
    

# الختم الاحترافي في نهاية المذكرة
st.markdown(f"""
    <div class="stamp-box">
        <p style="margin:0; font-weight:bold; font-size:18px;">المهندس المدني</p>
        <p style="margin:5px 0; font-size:20px; color:#d4af37; font-weight:bold;">بيلان مصطفى عبدالكريم</p>
        <p style="margin:0; font-size:14px;">دراسة - إشراف - تعهدات</p>
        <div style="margin-top:10px; border-top:1px solid #d4af37; padding-top:5px; font-size:12px;">
            توقيع المكتب المعتمد
        </div>
    </div>
    <div style="clear:both;"></div>
</div>
""", unsafe_allow_html=True)

# أزرار الإجراءات
st.divider()
c1, c2 = st.columns(2)
with c1:
    st.button("🖨️ طباعة المذكرة الحسابية (Ctrl+P)", on_click=None)
with c2:
    if st.button("🚀 تصدير المخطط (DXF)"):
        doc = ezdxf.new(setup=True)
        doc.modelspace().add_text(f"ENG. PELAN OFFICE - {project_name}", dxfattribs={'height': 5})
        buf = io.StringIO()
        doc.write(buf)
        st.download_button("📥 تحميل ملف AutoCAD", buf.getvalue(), "Project_Pelan.dxf")

st.markdown("<p style='text-align:center; color:gray;' class='no-print'>تم التدقيق بواسطة نظام بيلان الذكي v79 © 2026</p>", unsafe_allow_html=True)
