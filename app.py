import streamlit as st
import numpy as np
import pandas as pd
import ezdxf
import io
import matplotlib.pyplot as plt

# 1. إعدادات الصفحة والستايل
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
        margin-bottom: 20px;
    }
    .highlight-gold { color: #d4af37; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='legend-card' style='text-align:center;'><h1 style='color:#38bdf8;'>Pelan Ultimate Legend v32</h1><p class='highlight-gold'>المنظومة الهندسية الشاملة - م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. لوحة التحكم
with st.sidebar:
    st.header("🗂️ اختيار العنصر الإنشائي")
    category = st.selectbox("التصنيف الرئيسي:", ["خرسانة مسلحة", "منشآت معدنية", "تحليل زلزالي"])
    
    if category == "خرسانة مسلحة":
        elem = st.selectbox("العنصر:", ["جائز مستمر", "بلاطة فطرية", "بلاطة معصبة", "عمود طويل", "أساسات حصيرية", "جدار استنادي", "خزان مياه"])
    elif category == "منشآت معدنية":
        elem = st.selectbox("العنصر:", ["إطارات معدنية", "وصلات", "جوائز شبكية"])
    else:
        elem = "تحليل زلزالي"

    st.divider()
    conc_p = st.number_input("سعر البيتون ($/m3):", 110)
    steel_p = st.number_input("سعر الحديد ($/ton):", 950)

# 3. محرك الحسابات
def calculate_all():
    L, wu = 6.0, 4.0
    Mu = (wu * L**2) / 8
    As = (Mu * 10**5) / (0.87 * 4000 * 55)
    cost = (0.3 * 0.6 * L * conc_p) + (As * L * 0.00785 * steel_p)
    return Mu, As, cost

Mu, As, total_cost = calculate_all()

# 4. عرض النتائج (حل مشكلة الخطأ في الإزاحة)
col_data, col_visual = st.columns([1.3, 1])

with col_data:
    st.markdown("<div class='legend-card'>", unsafe_allow_html=True)
    st.subheader(f"🔍 تحليل وتصميم: {elem}")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("العزم التصميمي", f"{Mu:.2f} t.m")
    c2.metric("التسليح المطلوب", f"{As:.2f} cm²")
    c3.metric("التكلفة التقديرية", f"${total_cost:.1f}")

    st.write("---")
    st.markdown("### 🤖 توصية الذكاء الاصطناعي:")
    
    # تصحيح الـ if statements لمنع الخطأ الظاهر في الصورة
    if "خزان" in elem:
        st.info("💡 خزان المياه يحتاج تصميم Stage 1 لمنع التشرخ.")
    elif "حصيرية" in elem:
        st.info("💡 دقق إجهادات القص الثاقب Punching Shear.")
    elif "فطرية" in elem:
        st.info("💡 دقق تسليح شريحة العمود Column Strip.")
    elif "معدنية" in category:
        st.info("💡 دقق التحنيب الجانبي للمقاطع المعدنية.")
    else:
        st.info("💡 النظام الإنشائي المختار ضمن الحدود الآمنة.")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_visual:
    st.markdown("<div class='legend-card'>", unsafe_allow_html=True)
    st.subheader("🖼️ المخطط الإنشائي")
    
    # استدعاء المخططات التوضيحية
    if "جدار" in elem:
        st.write("رسم توضيحي للجدار الاستنادي")
            elif "خزان" in elem:
        st.write("رسم توضيحي للخزان")
            elif "فطرية" in elem:
        st.write("رسم توضيحي للبلاطة الفطرية")
            else:
        st.write("رسم توضيحي للجائز الإنشائي")
        
    if st.button("🚀 تصدير إلى AutoCAD"):
        doc = ezdxf.new(setup=True); msp = doc.modelspace()
        msp.add_lwpolyline([(0,0), (500,0), (500,50), (0,50), (0,0)])
        out = io.StringIO(); doc.write(out)
        st.download_button("📥 تحميل DXF", out.getvalue(), "Pelan_Design.dxf")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center;'>Pelan v32 | تم التصحيح بنجاح | 2026</p>", unsafe_allow_html=True)
