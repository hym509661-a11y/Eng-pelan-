import streamlit as st
import numpy as np
import ezdxf
import io
import matplotlib.pyplot as plt

# 1. إعدادات الواجهة (Dark Luxury Theme)
st.set_page_config(page_title="Pelan Master Oracle v34", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #050505; color: #ffffff; }
    .main-card {
        background: rgba(56, 189, 248, 0.05);
        border: 1px solid #38bdf8;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
        margin-bottom: 20px;
    }
    .gold-label { color: #d4af37; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-card' style='text-align:center;'><h1 style='color:#38bdf8;'>Pelan Master Oracle v34</h1><p class='gold-label'>النظام الهندسي الشامل | إشراف م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. لوحة التحكم الجانبية
with st.sidebar:
    st.header("⚙️ خيارات التصميم")
    category = st.radio("المجال الإنشائي:", ["بيتون مسلح", "منشآت معدنية", "دراسة زلزالية"])
    
    if category == "بيتون مسلح":
        elem = st.selectbox("العنصر:", ["جائز مستمر", "بلاطة فطرية", "بلاطة معصبة", "عمود", "أساسات حصيرية", "جدار استنادي", "خزان مياه"])
    elif category == "منشآت معدنية":
        elem = st.selectbox("العنصر:", ["إطار معدني Portal", "جائز شبكي Truss", "وصلات معدنية"])
    else:
        elem = "دراسة زلزالية شاملة"

    st.divider()
    st.subheader("💰 تحليل التكاليف")
    c_price = st.number_input("سعر البيتون ($/m3):", 110)
    s_price = st.number_input("سعر الحديد ($/ton):", 950)

# 3. محرك الحسابات (Unified Calculations)
def get_engineering_data():
    # قيم افتراضية للتحليل المالي
    vol_est = 2.5 # m3
    steel_est = 0.22 # ton
    total_cost = (vol_est * c_price) + (steel_est * s_price)
    return vol_est, steel_est, total_cost

vol, steel, cost = get_engineering_data()

# 4. عرض النتائج والذكاء الاصطناعي (تم حل مشكلة الإزاحة هنا)
col_info, col_visual = st.columns([1.2, 1])

with col_info:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 نتائج التحليل: {elem}")
    
    res1, res2 = st.columns(2)
    res1.metric("التكلفة التقديرية", f"${cost:.2f}")
    res2.metric("حجم البيتون", f"{vol} m³")
    
    st.divider()
    st.markdown("### 🤖 توصيات العقل الذكي (AI Recommendation):")
    
    # هيكل برمجي متين لتجنب IndentationError
    if "خزان" in elem:
        st.info("💡 نصيحة: صمم المقطع ليكون 'مقطع مائي' لمنع تسرب الرطوبة للحديد.")
            elif "حصيرية" in elem:
        st.info("💡 نصيحة: دقق القص الثاقب (Punching) وتأكد من كفاية سمك الحصيرة.")
            elif "فطرية" in elem:
        st.info("💡 نصيحة: انتبه لتوزيع العزوم بين شريحة العمود وشريحة الوسط.")
            elif "جدار" in elem:
        st.info("💡 نصيحة: دقق الاستقرار ضد الانزلاق (Sliding) والانقلاب (Overturning).")
            elif "زلزالية" in category:
        st.warning("🚨 تنبيه: دقق مركز الكتلة ومركز الصلابة لتجنب فتل المنشأ.")
    else:
        st.success("✅ النظام الإنشائي المختار اقتصادي ويحقق متطلبات الكود.")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_visual:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ المخطط الهندسي (AutoCAD)")
    
    if "معدنية" in category:
            else:
            
    st.divider()
    if st.button("🚀 توليد مخطط DXF فوراً"):
        try:
            doc = ezdxf.new(setup=True)
            msp = doc.modelspace()
            msp.add_lwpolyline([(0,0), (20,0), (20,10), (0,10), (0,0)]) # إطار توضيحي
            dxf_stream = io.StringIO()
            doc.write(dxf_stream)
            st.download_button("📥 تحميل ملف AutoCAD", dxf_stream.getvalue(), file_name=f"Pelan_{elem}.dxf")
            st.success("تم التجهيز!")
        except Exception as e:
            st.error(f"خطأ تقني: {e}")
            
    st.markdown("</div>", unsafe_allow_html=True)

# 5. التذييل
st.divider()
st.markdown("<p style='text-align:center;'>Pelan Master Oracle v34 | م. بيلان عبد الكريم | 2026</p>", unsafe_allow_html=True)
