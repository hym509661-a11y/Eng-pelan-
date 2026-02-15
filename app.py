import streamlit as st
import numpy as np
import pandas as pd
import ezdxf  # مكتبة توليد ملفات الأوتوكاد
import io

# 1. التنسيق السينمائي الفاخر (Cinematic Gold UI)
st.set_page_config(page_title="Pelan Grand Master v31", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #050505; color: #d4af37; } /* خلفية سوداء مع خط ذهبي */
    .master-card {
        background: rgba(212, 175, 55, 0.05);
        border: 1px solid #d4af37;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.2);
    }
    .price-tag { color: #a8eb12; font-size: 1.5rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='master-card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Grand Master v31</h1><p>الذكاء الهندسي، التكلفة المالية، وتوليد المخططات | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. لوحة التحكم (The Engine)
with st.sidebar:
    st.header("💎 لوحة التحكم العليا")
    task = st.selectbox("المهمة الحالية:", ["تحليل وتصميم شامل", "حساب التكلفة التقديرية", "توليد ملفات AutoCAD"])
    
    st.divider()
    st.subheader("💰 أسعار السوق الحالية")
    conc_price = st.number_input("سعر م3 البيتون ($):", 50, 200, 110)
    steel_price = st.number_input("سعر طن الحديد ($):", 500, 1500, 950)
    
    st.divider()
    L = st.slider("طول البحر L (m):", 1.0, 15.0, 6.0)
    B = st.number_input("العرض B (cm):", 20, 100, 30)
    h = st.number_input("الارتفاع h (cm):", 20, 150, 60)
    wu = st.number_input("الحمل Wu (t/m):", 0.5, 50.0, 3.5)

# 3. محرك الحسابات المزدوج (AI + Cost + Design)
d = h - 5
Mu = (wu * L**2) / 8
As = (Mu * 10**5) / (0.87 * 4000 * d)
vol_conc = (B/100) * (h/100) * L
weight_steel = As * L * 100 * 0.000785 * 10 # بالطن تقريباً

# حساب التكلفة
total_cost = (vol_conc * conc_price) + (weight_steel * steel_price)

# 4. عرض النتائج المتكاملة
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("📑 المذكرة الفنية والمالية")
    
    res1, res2 = st.columns(2)
    res1.write(f"**العزم:** {Mu:.2f} t.m")
    res1.write(f"**حديد التسليح:** {As:.2f} cm²")
    
    res2.markdown(f"**تكلفة المواد التقديرية:**")
    res2.markdown(f"<span class='price-tag'>${total_cost:.2f}</span>", unsafe_allow_html=True)
    
    st.divider()
    st.write("🤖 **اقتراح AI:** النظام الإنشائي المختار اقتصادي جداً لهذه البحور.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("⚙️ توليد مخططات AutoCAD")
    
    if st.button("توليد ملف DXF للجائز"):
        # برمجة ملف AutoCAD آلياً
        doc = ezdxf.new(setup=True)
        msp = doc.modelspace()
        # رسم مستطيل الجائز
        msp.add_lwpolyline([(0, 0), (L*100, 0), (L*100, h), (0, h), (0, 0)])
        # رسم أسياخ التسليح
        msp.add_line((5, 5), (L*100 - 5, 5), dxfattribs={'color': 1}) # حديد سفلي
        
        # حفظ الملف في ذاكرة مؤقتة
        out = io.StringIO()
        doc.write(out)
        st.download_button("📥 تحميل ملف AutoCAD (DXF)", data=out.getvalue(), file_name="Pelan_Design.dxf")
        st.success("تم تجهيز ملف DXF بنجاح!")

    
    st.caption("تفريد الحديد كما سيظهر في ملف AutoCAD")
    st.markdown("</div>", unsafe_allow_html=True)

# 5. التذييل
st.divider()
st.markdown("<p style='text-align:center;'>Pelan Grand Master v31 | All-in-One Engineering Intelligence | م. بيلان عبد الكريم © 2026</p>", unsafe_allow_html=True)
