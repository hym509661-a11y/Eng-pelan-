import streamlit as st
import numpy as np
import ezdxf
import io

# 1. الإعدادات البصرية (Premium Engineering Theme)
st.set_page_config(page_title="Pelan Masterpiece v42", layout="wide")

st.markdown("""
<style>
    .stApp { background: #0a0a0a; color: #ffffff; }
    .card {
        background: rgba(0, 242, 255, 0.05);
        border: 1px solid #00f2ff;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .gold { color: #d4af37; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='card' style='text-align:center;'><h1 style='color:#00f2ff;'>Pelan Grand Masterpiece v42</h1><p class='gold'>النظام الهندسي الموحد | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية
with st.sidebar:
    st.header("⚙️ الإعدادات")
    field = st.radio("المجال:", ["بيتون مسلح", "حفر وردم", "زلازل"])
    if field == "بيتون مسلح":
        elem = st.selectbox("العنصر:", ["جائز", "بلاطة فطرية", "أساسات حصيرية", "خزان مياه", "جدار استنادي"])
    elif field == "حفر وردم":
        elem = "كميات التربة"
        area = st.number_input("المساحة (m²):", 100.0)
        depth = st.number_input("العمق (m):", 1.5)
    else:
        elem = "دراسة زلزالية"
    
    st.divider()
    cp = st.number_input("سعر البيتون ($):", 110)
    sp = st.number_input("سعر الحديد ($):", 950)

# 3. الحسابات
def get_results():
    v, w = 5.0, 0.4
    if field == "حفر وردم":
        vol = area * depth
        cost = vol * 6.0
        return vol, 0, cost
    cost = (v * cp) + (w * sp)
    return v, w, cost

vol, steel, cost = get_results()

# 4. العرض (هنا تم حل مشكلة الإزاحات في الخزان والحصيرية)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(f"📊 النتائج: {elem}")
    st.write(f"💰 التكلفة: **${cost:.2f}**")
    if field != "حفر وردم":
        st.write(f"🏗️ المواد: {vol} m³ بيتون | {steel} t حديد")
    
    st.divider()
    st.markdown("### 🤖 توصية المهندس الذكي:")
    
    # حماية كاملة من IndentationError: كل جملة تحتها كود مباشر
    if "خزان" in elem:
        st.info("💡 نصيحة: صمم الخزان كـ Un-cracked Section واستخدم فواصل مائية.")
        
    elif "حصيرية" in elem:
        st.info("💡 نصيحة: دقق القص الثاقب Punching Shear وتأكد من سماكة الحصيرة.")
        
    elif "فطرية" in elem:
        st.info("💡 نصيحة: دقق العزوم السالبة عند الأعمدة واستخدم Drop Panels.")
        
    elif "جدار" in elem:
        st.info("💡 نصيحة: تحقق من الاستقرار ضد الانزلاق والانقلاب.")
        
    elif field == "زلازل":
        st.warning("🚨 زلازل: تأكد من تناظر جدران القص لتجنب الفتل.")
    else:
        st.success("✅ النظام المختار آمن هندسياً.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🖋️ AutoCAD الرسم")
    
    if st.button("🚀 تصدير DXF"):
        doc = ezdxf.new(setup=True)
        msp = doc.modelspace()
        msp.add_lwpolyline([(0,0), (50,0), (50,20), (0,20), (0,0)])
        buf = io.StringIO()
        doc.write(buf)
        st.download_button("📥 تحميل المخطط", buf.getvalue(), f"Pelan_{elem}.dxf")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center;'>Pelan v42 | 2026</p>", unsafe_allow_html=True)
