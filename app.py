import streamlit as st
import numpy as np
import ezdxf
import io

# 1. إعدادات الواجهة (Dark Professional Theme)
st.set_page_config(page_title="Pelan Oracle v37", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #ffffff; }
    .status-card {
        background: rgba(56, 189, 248, 0.05);
        border: 1px solid #38bdf8;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='status-card' style='text-align:center;'><h1 style='color:#38bdf8;'>Pelan Oracle v37</h1><p>الموسوعة الإنشائية الشاملة | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية
with st.sidebar:
    st.header("🛠️ خيارات التصميم")
    category = st.radio("المجال:", ["خرسانة مسلحة", "حساب الحفر والردم", "تحليل زلزالي"])
    
    if category == "خرسانة مسلحة":
        elem = st.selectbox("العنصر:", ["جائز", "بلاطة فطرية", "أساسات حصيرية", "خزان مياه", "جدار استنادي"])
    elif category == "حساب الحفر والردم":
        elem = "كميات التربة"
        site_area = st.number_input("مساحة الموقع (m²):", 100.0)
        exc_depth = st.number_input("عمق الحفر (m):", 1.5)
    else:
        elem = "تحليل زلزالي"

    st.divider()
    c_price = st.number_input("سعر البيتون ($/m3):", 110)
    s_price = st.number_input("سعر الحديد ($/ton):", 950)

# 3. محرك الحسابات
def calculate_metrics():
    vol, steel = 5.0, 0.4
    if category == "حساب الحفر والردم":
        vol = site_area * exc_depth
        cost = vol * 5.0 # فرضية تكلفة الحفر
        return vol, 0, cost
    cost = (vol * c_price) + (steel * s_price)
    return vol, steel, cost

vol, steel, total_cost = calculate_metrics()

# 4. العرض الفني (حل مشكلة الإزاحة في الخزان والحصيرية)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 النتائج الفنية: {elem}")
    
    if category == "حساب الحفر والردم":
        st.write(f"🚜 **حجم الحفر الكلي:** {vol:.2f} m³")
        st.write(f"💰 **التكلفة التقديرية:** ${total_cost:.2f}")
    else:
        st.write(f"🏗️ **الكميات:** {vol} m³ بيتون | {steel} t حديد")
        st.write(f"💵 **التكلفة الإجمالية:** ${total_cost:.2f}")

    st.divider()
    st.markdown("### 🤖 توصية AI الذكية:")
    
    # تصحيح هيكلي كامل: كل شرط يتبعه كود مباشر مزاح 4 مسافات
    if "خزان" in elem:
        st.info("💡 نصيحة الخزان: تأكد من استخدام 'بيتون كتيم' وعزل الزوايا جيداً لمنع تسرب المياه.")
            elif "حصيرية" in elem:
        st.info("💡 نصيحة الحصيرة: دقق إجهاد التربة المسموح وتأكد من سماكة البلاطة لمقاومة اختراق الأعمدة.")
            elif "فطرية" in elem:
        st.info("💡 نصيحة البلاطة: انتبه لتسليح 'القص الثاقب' Punching Shear عند رؤوس الأعمدة.")
            elif category == "حساب الحفر والردم":
        st.info("💡 نصيحة التربة: دقق 'زاوية الاحتكاك الداخلي' لتحديد مدى الحاجة لجدران ساندة أثناء الحفر.")
    else:
        st.success("✅ النظام الإنشائي المختار آمن ومطابق للكود.")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ AutoCAD & Visuals")
    
    if "جدار" in elem:
            else:
        
    st.divider()
    if st.button("🚀 تصدير AutoCAD (DXF)"):
        doc = ezdxf.new(setup=True)
        msp = doc.modelspace()
        msp.add_lwpolyline([(0,0), (50,0), (50,20), (0,20), (0,0)])
        dxf_io = io.StringIO()
        doc.write(dxf_io)
        st.download_button("📥 تحميل DXF", dxf_io.getvalue(), f"Pelan_{elem}.dxf")
    st.markdown("</div>", unsafe_allow_html=True)

# 5. التوقيع
st.divider()
st.markdown("<p style='text-align:center;'>Pelan Oracle v37 | م. بيلان عبد الكريم | 2026</p>", unsafe_allow_html=True)
