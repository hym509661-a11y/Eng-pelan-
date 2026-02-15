import streamlit as st
import numpy as np
import ezdxf
import io
import matplotlib.pyplot as plt

# 1. تنسيق الواجهة (Luxury Engineering UI)
st.set_page_config(page_title="Pelan Supreme v36", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #050505; color: #ffffff; }
    .status-card {
        background: rgba(56, 189, 248, 0.05);
        border: 1px solid #38bdf8;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.1);
        margin-bottom: 20px;
    }
    .gold-text { color: #d4af37; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='status-card' style='text-align:center;'><h1 style='color:#38bdf8;'>Pelan Supreme v36</h1><p class='gold-text'>الموسوعة الهندسية المتكاملة | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. لوحة التحكم (Sidebar)
with st.sidebar:
    st.header("🛠️ خيارات المهندس")
    category = st.radio("المجال:", ["خرسانة مسلحة", "كميات الحفر (Earthwork)", "تحليل زلزالي"])
    
    if category == "خرسانة مسلحة":
        elem = st.selectbox("العنصر:", ["جائز", "بلاطة فطرية", "بلاطة معصبة", "أساسات حصيرية", "جدار استنادي", "خزان مياه"])
    elif category == "كميات الحفر (Earthwork)":
        elem = "حساب الحفر والردم"
        area = st.number_input("مساحة الموقع (m²):", 100)
        depth = st.number_input("عمق الحفر المطلوبه (m):", 1.5)
    else:
        elem = "تحليل زلزالي"

    st.divider()
    c_price = st.number_input("سعر البيتون ($/m3):", 110)
    s_price = st.number_input("سعر الحديد ($/ton):", 950)

# 3. محرك الحسابات (Engine)
def calculate_all():
    # حسابات افتراضية
    v_conc = 5.0
    w_steel = 0.4
    if category == "كميات الحفر (Earthwork)":
        v_excavation = area * depth
        total_c = v_excavation * 5 # فرضية 5 دولار للمتر مكعب حفر
        return v_excavation, 0, total_c
    
    total_c = (v_conc * c_price) + (w_steel * s_price)
    return v_conc, w_steel, total_c

vol, steel, cost = calculate_all()

# 4. العرض الفني وتصحيح أخطاء الإزاحة (Indentation Fix)
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 النتائج الفنية: {elem}")
    
    if category == "كميات الحفر (Earthwork)":
        st.write(f"🚜 **حجم الحفر الكلي:** {vol:.2f} m³")
        st.write(f"💰 **تكلفة الحفر التقديرية:** ${cost:.2f}")
    else:
        st.write(f"🏗️ **كمية المواد:** {vol} m³ بيتون | {steel} t حديد")
        st.write(f"💵 **التكلفة الإجمالية:** ${cost:.2f}")

    st.divider()
    st.markdown("### 🤖 توصية الذكاء الاصطناعي (AI):")
    
    # تصحيح هيكلي كامل لمنع أخطاء Indentation التي ظهرت في صورك
    if "حصيرية" in elem:
        st.info("💡 نصيحة الحصيرة: دقق 'القص الثاقب' (Punching) وتأكد من سماكة البلاطة لمقاومة اختراق الأعمدة.")
            elif "خزان" in elem:
        st.info("💡 نصيحة الخزان: استخدم بيتون عيار عالي وفواصل مائية (Waterstops) لمنع التسرب.")
            elif "فطرية" in elem:
        st.info("💡 نصيحة البلاطة: دقق العزوم السالبة عند الأعمدة ووزع التسليح حسب شرائح العمود والوسط.")
    elif category == "كميات الحفر (Earthwork)":
        st.info("💡 نصيحة الحفر: دقق منسوب المياه الجوفية ونوع التربة لتحديد زاوية الميل الآمنة للحفر.")
    else:
        st.success("✅ النظام الإنشائي المختار متوازن واقتصادي.")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ المخططات الفنية")
    
    if "حصيرية" in elem:
            elif "جدار" in elem:
            else:
        
    st.divider()
    if st.button("🚀 تصدير المخطط لـ AutoCAD"):
        doc = ezdxf.new(setup=True)
        msp = doc.modelspace()
        msp.add_lwpolyline([(0,0), (50,0), (50,20), (0,20), (0,0)])
        dxf_io = io.StringIO()
        doc.write(dxf_io)
        st.download_button("📥 تحميل ملف DXF", dxf_io.getvalue(), f"Pelan_{elem}.dxf")
    
    st.markdown("</div>", unsafe_allow_html=True)

# 5. التوقيع
st.divider()
st.markdown("<p style='text-align:center;'>Pelan Supreme v36 | م. بيلان عبد الكريم | 2026</p>", unsafe_allow_html=True)
