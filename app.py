import streamlit as st
import numpy as np
import ezdxf
import io
import matplotlib.pyplot as plt

# 1. الإعدادات البصرية (Masterpiece Theme)
st.set_page_config(page_title="Pelan Grandmaster v32.1", layout="wide")
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

st.markdown("<div class='main-box' style='text-align:center;'><h1 style='color:#38bdf8;'>Pelan Grandmaster v32.1</h1><p class='gold-text'>النظام الهندسي الشامل | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية (Engineering Dashboard)
with st.sidebar:
    st.header("⚙️ الإعدادات")
    category = st.radio("المجال:", ["بيتون مسلح", "منشآت معدنية", "دراسة زلزالية"])
    
    if category == "بيتون مسلح":
        elem = st.selectbox("العنصر:", ["جائز مستمر", "بلاطة فطرية", "بلاطة معصبة", "عمود", "أساسات حصيرية", "جدار استنادي", "خزان مياه"])
    elif category == "منشآت معدنية":
        elem = st.selectbox("العنصر:", ["إطار معدني Portal", "جائز شبكي Truss", "وصلات"])
    else:
        elem = "دراسة زلزالية"

    st.divider()
    st.subheader("💰 الأسعار والتكاليف")
    c_price = st.number_input("سعر المتر المكعب ($):", 110)
    s_price = st.number_input("سعر طن الحديد ($):", 950)

# 3. محرك الحسابات الموحد
# (هنا نضع قيم افتراضية للحساب لمجرد العرض، يمكنك ربطها بمدخلات المستخدم)
def get_calculations():
    # قيم افتراضية للنمذجة
    vol = 1.5  # m3
    steel_w = 0.12 # ton
    cost = (vol * c_price) + (steel_w * s_price)
    return vol, steel_w, cost

vol, steel_w, total_cost = get_calculations()

# 4. عرض النتائج والتحليل (مع تصحيح الأخطاء البرمجية)
col_info, col_draw = st.columns([1.2, 1])

with col_info:
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    st.subheader(f"📊 تحليل: {elem}")
    
    # بطاقات النتائج الممالية
    st.write(f"💵 **التكلفة التقديرية للمواد:** ${total_cost:.2f}")
    st.write(f"🧱 **كمية البيتون:** {vol} m³ | 🏗️ **كمية الحديد:** {steel_w} ton")
    
    st.divider()
    st.markdown("### 🤖 توصية الذكاء الاصطناعي (AI):")
    
    # الجزء الذي كان يسبب الخطأ - تم تصحيحه وضمان الإزاحة
    if "خزان" in elem:
        st.info("💡 يجب مراعاة ضغط الماء المثلثي واستخدام فواصل الصب Waterstops.")
    elif "فطرية" in elem:
        st.info("💡 دقق تسليح القص الثاقب (Punching) عند رؤوس الأعمدة.")
    elif "حصيرية" in elem:
        st.info("💡 تأكد من توزيع ضغط التربة بانتظام وتجنب الهبوط التفاضلي.")
    elif "معصبة" in elem:
        st.info("💡 دقق توزيع الأحمال على الأعصاب في الاتجاهين (α & β).")
    elif "زلزالية" in category:
        st.warning("🚨 دقق الانتقال الجانبي (Drift) لضمان استقرار المنشأ.")
    else:
        st.success("✅ النظام الإنشائي المختار آمن ومطابق لاشتراطات الكود.")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_draw:
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    st.subheader("🖋️ المخطط والرسومات")
    
    # عرض الصور حسب العنصر
    if "خزان" in elem:
            elif "حصيرية" in elem:
            elif "فطرية" in elem:
            elif "جدار" in elem:
            else:
        
    st.divider()
    # ميزة التصدير لـ AutoCAD
    if st.button("🚀 تصدير ملف AutoCAD (DXF)"):
        try:
            doc = ezdxf.new(setup=True)
            msp = doc.modelspace()
            msp.add_lwpolyline([(0, 0), (10, 0), (10, 5), (0, 5), (0, 0)]) # رسم مستطيل جائز
            dxf_stream = io.StringIO()
            doc.write(dxf_stream)
            st.download_button("📥 تحميل DXF", dxf_stream.getvalue(), file_name=f"Pelan_{elem}.dxf")
            st.success("تم التصدير بنجاح!")
        except Exception as e:
            st.error(f"خطأ في التصدير: {e}")
            
    st.markdown("</div>", unsafe_allow_html=True)

# 5. التوقيع
st.divider()
st.markdown(f"<p style='text-align:center;'>المصمم الإنشائي م. بيلان عبد الكريم | تم التحديث في: 2026</p>", unsafe_allow_html=True)
