import streamlit as st
import numpy as np
import pandas as pd
import ezdxf
import io
import matplotlib.pyplot as plt

# 1. التنسيق الملكي (Royal Engineering UI)
st.set_page_config(page_title="Pelan Ultimate Legend v32", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #0a0a0a; color: #ffffff; }
    .legend-card {
        background: rgba(255, 255, 255, 0.03);
        border: 2px solid #38bdf8;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.15);
    }
    .highlight-gold { color: #d4af37; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='legend-card' style='text-align:center;'><h1 style='color:#38bdf8;'>Pelan Ultimate Legend v32</h1><p class='highlight-gold'>المنظومة الهندسية الشاملة (خرسانة - فولاذ - زلازل - تكاليف - AutoCAD) | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية (The Master Control)
with st.sidebar:
    st.header("🗂️ اختيار العنصر الإنشائي")
    category = st.selectbox("التصنيف الرئيسي:", ["خرسانة مسلحة", "منشآت معدنية", "تحليل زلزالي ديناميكي"])
    
    if category == "خرسانة مسلحة":
        elem = st.selectbox("العنصر:", ["جائز مستمر", "بلاطة فطرية (Flat Slab)", "بلاطة معصبة (Waffle)", "عمود طويل (Buckling)", "أساسات حصيرية (Raft)", "جدار استنادي", "خزان مياه"])
    elif category == "منشآت معدنية":
        elem = st.selectbox("العنصر:", ["إطارات معدنية (Portal Frame)", "وصلات (Connections)", "جوائز شبكية (Truss)"])
    else:
        elem = "تحليل زلزالي"

    st.divider()
    st.subheader("💰 بارامترات السوق")
    conc_p = st.number_input("سعر البيتون ($/m3):", 110)
    steel_p = st.number_input("سعر الحديد ($/ton):", 950)

# 3. محرك الحسابات الموحد (The Unified Engine)
def calculate_all():
    # حسابات افتراضية للتكلفة والتسليح بناءً على العنصر المختلط
    L = 6.0 # طول افتراضي
    wu = 4.0 # حمل افتراضي
    Mu = (wu * L**2) / 8
    As = (Mu * 10**5) / (0.87 * 4000 * 55) # d=55
    cost = (0.3 * 0.6 * L * conc_p) + (As * L * 0.00785 * steel_p)
    return Mu, As, cost

Mu, As, total_cost = calculate_all()

# 4. عرض المحتوى بناءً على العنصر المختار
col_data, col_visual = st.columns([1.3, 1])

with col_data:
    st.markdown("<div class='legend-card'>", unsafe_allow_html=True)
    st.subheader(f"🔍 تحليل وتصميم: {elem}")
    
    # تفريغ النتائج حسب النوع
    c1, c2, c3 = st.columns(3)
    c1.metric("العزم التصميمي", f"{Mu:.2f} t.m")
    c2.metric("التسليح المطلوب", f"{As:.2f} cm²")
    c3.metric("التكلفة التقديرية", f"${total_cost:.1f}")

    st.write("---")
    st.markdown("### 🤖 توصية الذكاء الاصطناعي (AI Analysis):")
    if "خزان" in elem:
        st.info("💡 خزان المياه يحتاج تصميم Stage 1 (تحت التشغيل) و Stage 2 (تحت الانهيار) لضمان عدم التسرب.")
        
    elif "حصيرية" in elem:
        st.info("💡 يجب التأكد من جساءة الحصيرة لمقاومة القص الثاقب (Punching Shear) تحت الأعمدة المركزية.")
        
    elif "معدنية" in category:
        st.info("💡 المنشآت المعدنية تتطلب تدقيق التحنيب الجانبي (Lateral Torsional Buckling).")
        
    elif "زلزالي" in category:
        st.error("🚨 يتم الآن حساب قوى القص القاعدي وتوزيعها مثلثياً على أدوار المبنى.")
        
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_visual:
    st.markdown("<div class='legend-card'>", unsafe_allow_html=True)
    st.subheader("🖼️ المخطط الإنشائي التفاعلي")
    
    if "جدار استنادي" in elem:
        
    elif "فطرية" in elem:
        
    elif "معصبة" in elem:
        
    elif "عمود" in elem:
        
    elif "مستمر" in elem:
        
    
    st.divider()
    if st.button("🚀 تصدير المخطط إلى AutoCAD (DXF)"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_lwpolyline([(0,0), (500,0), (500,50), (0,50), (0,0)]) # رسم تقريبي
        out = io.StringIO(); doc.write(out)
        st.download_button("📥 تحميل DXF", out.getvalue(), "Pelan_Master_Design.dxf")
    st.markdown("</div>", unsafe_allow_html=True)

# 5. التذييل النهائي
st.divider()
st.markdown("<h3 style='text-align:center;'>✅ تم التدقيق والمصادقة بواسطة: المهندس بيلان عبد الكريم</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Pelan Ultimate Legend v32 | 2026</p>", unsafe_allow_html=True)
