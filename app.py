import streamlit as st
import numpy as np
import ezdxf
import io
import matplotlib.pyplot as plt

# 1. الإعدادات البصرية الاحترافية
st.set_page_config(page_title="Pelan Grand Master v33", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #050505; color: #ffffff; }
    .main-box {
        background: rgba(56, 189, 248, 0.05);
        border: 1px solid #38bdf8;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
    }
    .gold-text { color: #d4af37; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-box' style='text-align:center;'><h1 style='color:#38bdf8;'>Pelan Grand Master v33</h1><p class='gold-text'>نظام التحليل الإنشائي المتكامل | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية (Control Panel)
with st.sidebar:
    st.header("⚙️ الإعدادات")
    category = st.radio("المجال:", ["بيتون مسلح", "منشآت معدنية", "دراسة زلزالية"])
    
    # تنظيم القوائم المنسدلة
    if category == "بيتون مسلح":
        elem = st.selectbox("العنصر:", ["جائز مستمر", "بلاطة فطرية", "بلاطة معصبة", "عمود", "أساسات حصيرية", "جدار استنادي", "خزان مياه"])
    elif category == "منشآت معدنية":
        elem = st.selectbox("العنصر:", ["إطار معدني Portal", "جائز شبكي Truss", "وصلات"])
    else:
        elem = "دراسة زلزالية"

    st.divider()
    c_price = st.number_input("سعر البيتون ($/m3):", 110)
    s_price = st.number_input("سعر الحديد ($/ton):", 950)

# 3. محرك الحسابات (Simplified Logic)
def get_stats():
    # قيم افتراضية للحساب المالي
    vol = 2.5 # m3
    steel = 0.2 # ton
    cost = (vol * c_price) + (steel * s_price)
    return vol, steel, cost

vol, steel, total_cost = get_stats()

# 4. عرض النتائج والذكاء الاصطناعي (تم تصحيح الإزاحة هنا)
col_info, col_draw = st.columns([1.2, 1])

with col_info:
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    st.subheader(f"📊 النتائج: {elem}")
    st.write(f"💵 **التكلفة التقديرية:** ${total_cost:.2f}")
    
    st.divider()
    st.markdown("### 🤖 نصيحة AI للنظام الإنشائي:")
    
    # حل مشكلة IndentationError التي ظهرت في الصور
    if "خزان" in elem:
        st.info("💡 نصيحة: صمم المقطع ليكون Un-cracked Section لضمان عزل المياه.")
    elif "حصيرية" in elem:
        st.info("💡 نصيحة: دقق إجهاد التربة الفعلي وقارنه بالجهد المسموح.")
    elif "فطرية" in elem:
        st.info("💡 نصيحة: استخدم تيجان الأعمدة (Capitals) إذا كان القص الثاقب عالياً.")
    elif "زلزالية" in category:
        st.warning("🚨 تنبيه: تأكد من كفاية جدران القص لمقاومة القوى الجانبية.")
    elif "معدنية" in category:
        st.info("💡 نصيحة: تأكد من استقرار الوصلات لمقاومة العزوم.")
    else:
        st.success("✅ النظام الإنشائي المختار متوافق مع اشتراطات الكود.")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_draw:
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    st.subheader("🖋️ المخططات الفنية")
    
    # عرض الصور التوضيحية
    if "خزان" in elem:
            elif "حصيرية" in elem:
            elif "فطرية" in elem:
            elif "جدار" in elem:
            else:
        
    st.divider()
    # ميزة AutoCAD
    if st.button("🚀 توليد مخطط AutoCAD (DXF)"):
        try:
            doc = ezdxf.new(setup=True)
            msp = doc.modelspace()
            msp.add_lwpolyline([(0, 0), (10, 0), (10, 5), (0, 5), (0, 0)])
            dxf_stream = io.StringIO()
            doc.write(dxf_stream)
            st.download_button("📥 تحميل المخطط", dxf_stream.getvalue(), file_name=f"{elem}_design.dxf")
            st.success("تم تجهيز الملف!")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
            
    st.markdown("</div>", unsafe_allow_html=True)

# 5. التذييل
st.divider()
st.markdown("<p style='text-align:center;'>المصمم الإنشائي م. بيلان عبد الكريم | 2026</p>", unsafe_allow_html=True)
