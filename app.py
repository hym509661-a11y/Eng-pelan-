import streamlit as st
import numpy as np
import ezdxf
import io
from datetime import datetime

# 1. إعدادات الهوية البصرية (الختم والمذكرة)
ST_NAME = "بيلان مصطفى عبد الكريم"
ST_JOB = "دراسة - إشراف - تعهدات"
ST_TITLE = "المهندس المدني"

st.set_page_config(page_title="Eng. Pelan v82", layout="wide")
st.markdown(f"""
<style>
    .report-box {{ background: white; color: black; padding: 25px; border-radius: 10px; direction: rtl; border-right: 8px solid #d4af37; }}
    .stamp {{ border: 4px double #d4af37; padding: 10px; width: 280px; text-align: center; background: white; color: black; float: left; margin-top: 20px; }}
    .stApp {{ background-color: #0b1619; color: white; }}
</style>
""", unsafe_allow_html=True)

# 2. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.header("⚙️ مدخلات المشروع")
    p_title = st.text_input("اسم المشروع:", "مشروع بيلان الهندسي")
    mode = st.selectbox("العنصر الإنشائي:", ["الجوائز", "البلاطات", "الأساسات", "الخزانات"])
    B = st.number_input("العرض B (cm):", 20, 500, 30)
    H = st.number_input("الارتفاع H (cm):", 10, 500, 60)
    L = st.number_input("الطول L (m):", 1.0, 50.0, 5.0)
    P = st.number_input("الحمل (kN):", 1.0, 100000.0, 150.0)
    phi = st.selectbox("القطر (mm):", [12, 14, 16, 18, 20, 25], index=2)

# 3. محرك الحسابات الاحترافي
fy, fcu = 420, 25
area_bar = (np.pi * phi**2) / 4
res = {}
bbs = ""

if mode == "الجوائز":
    M = (P * L**2) / 8
    As = (M * 1e6) / (0.87 * fy * (H-5) * 10)
    n = max(2, int(np.ceil(As / area_bar)))
    res = {"العزم التصميمي": f"{M:.1f} kNm", "تسليح الشد الرئيسي": f"{n} T {phi}"}
    bbs = f"{n} T {phi}"

if mode == "البلاطات":
    M = (P * L**2) / 10
    As = (M * 1e6) / (0.87 * fy * (H-3) * 10)
    n = max(5, int(np.ceil(As / area_bar)))
    res = {"عزم المتر": f"{M:.1f} kNm/m", "التسليح المعتمد": f"{n} T {phi}/m"}
    bbs = f"{n} T {phi} / m'"

if mode == "الأساسات":
    stress = P / (B * L / 10000)
    n = max(6, int(np.ceil((0.0018 * B * H * 100) / area_bar)))
    res = {"إجهاد التربة": f"{stress:.2f} kN/m²", "تسليح القاعدة": f"{n} T {phi}/m"}
    bbs = f"{n} T {phi} @ 15cm"

if mode == "الخزانات":
    Mt = (10 * (H/100) * L**2) / 12
    n = max(7, int(np.ceil(((Mt * 1e6) / (0.87 * fy * (H-5) * 10)) / area_bar)))
    res = {"عزم جدار الخزان": f"{Mt:.1f} kNm", "تسليح الجدار": f"{n} T {phi}/m"}
    bbs = f"{n} T {phi} / m'"

# 4. المذكرة الحسابية والختم (المخرجات)
st.markdown(f"<h1 style='text-align:center;'>🏢 المذكرة الحسابية - مكتب م. بيلان</h1>", unsafe_allow_html=True)

st.markdown("<div class='report-box'>", unsafe_allow_html=True)
st.subheader(f"المشروع: {p_title}")
st.write(f"تاريخ المذكرة: {datetime.now().strftime('%Y-%m-%d')}")
st.divider()

# عرض النتائج الهندسية
for key, value in res.items():
    st.write(f"🔹 **{key}:** {value}")

st.markdown(f"<div style='background:#f9f9f9; padding:15px; border:1px dashed #d4af37; margin:15px 0;'><h4>التوصيف الإنشائي النهائي: {bbs}</h4></div>", unsafe_allow_html=True)

# الختم الهندسي
st.markdown(f"""
<div class='stamp'>
    <p style='margin:0;'><b>{ST_TITLE}</b></p>
    <p style='color:#d4af37; font-size:18px; margin:5px 0;'><b>{ST_NAME}</b></p>
    <p style='margin:0; font-size:14px;'>{ST_JOB}</p>
    <hr style='border:1px solid #d4af37;'>
    <p style='font-size:10px;'>ختم الاعتماد الهندسي</p>
</div>
<div style='clear:both;'></div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# الرسوم التوضيحية بناءً على العنصر
if mode == "الجوائز":
    
elif mode == "البلاطات":
    
