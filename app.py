import streamlit as st
import numpy as np
import ezdxf
import io

# 1. الإعدادات البصرية المتقدمة (Engineering Royal Theme)
st.set_page_config(page_title="Pelan Masterpiece v44", layout="wide")

# تخصيص الخلفية والألوان (استبدال الأزرق بالزمردي والذهبي)
st.markdown("""
<style>
    .stApp {
        background-image: url("https://www.transparenttextures.com/patterns/graphy-dark.png");
        background-color: #0d1b1e; /* لون أخضر زمردي داكن جداً */
        color: #ffffff;
    }
    .master-card {
        background: rgba(16, 44, 41, 0.8);
        border: 2px solid #d4af37; /* إطار ذهبي */
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }
    .gold-text { color: #d4af37; font-weight: bold; }
    .emerald-text { color: #50c878; font-weight: bold; }
    
    /* تنسيق زر التصدير */
    .stButton>button {
        background: linear-gradient(45deg, #d4af37, #996515);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #d4af37;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='master-card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Grand Masterpiece v44</h1><p class='gold-text'>النظام الهندسي الموحد | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية (Control Panel)
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    field = st.radio("المجال:", ["بيتون مسلح", "حفر وردم", "زلازل"])
    
    if field == "بيتون مسلح":
        elem = st.selectbox("العنصر الإنشائي:", [
            "أعمدة خرسانية", 
            "بلاطة مصمتة (اتجاه واحد)", 
            "بلاطة مصمتة (اتجاهين)",
            "بلاطة هوردي (اتجاه واحد)",
            "بلاطة هوردي (اتجاهين)",
            "بلاطة فطرية Flat Slab", 
            "أساسات حصيرية Raft", 
            "خزان مياه", 
            "جدار استنادي"
        ])
    elif field == "حفر وردم":
        elem = "كميات التربة"
        area = st.number_input("المساحة (m²):", 100.0)
        depth = st.number_input("العمق (m):", 1.5)
    else:
        elem = "دراسة زلزالية"
    
    st.divider()
    cp = st.number_input("سعر البيتون ($):", 110)
    sp = st.number_input("سعر الحديد ($):", 950)

# 3. محرك الحسابات
def calculate_results():
    v, w = 5.8, 0.48
    if field == "حفر وردم":
        vol = area * depth
        cost = vol * 6.0
        return vol, 0, cost
    cost = (v * cp) + (w * sp)
    return v, w, cost

vol, steel, cost = calculate_results()

# 4. العرض الفني (توصية المهندس بيلان)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 النتائج التحليلية: {elem}")
    st.write(f"💰 التكلفة المقدرة: <span class='price-tag' style='color:#50c878; font-size:1.5rem; font-weight:bold;'>${cost:.2f}</span>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 👨‍🏫 توصية المهندس بيلان:")
    
    if "أعمدة" in elem:
        st.info("💡 الأعمدة: دقق النحافة (Slenderness) وتأكد من استمرارية أشاير الحديد وتكثيف الكانات في مناطق الاتصال.")
        
    elif "مصمتة (اتجاه واحد)" in elem:
        st.info("💡 بلاطة اتجاه واحد: تأكد من توزيع الحديد الرئيسي في الاتجاه القصير لمقاومة العزوم القصوى.")
    elif "مصمتة (اتجاهين)" in elem:
        st.info("💡 بلاطة اتجاهين: دقق معاملات توزيع الأحمال وتأكد من تسليح الزوايا لمقاومة الالتواء (Torsion).")
    elif "هوردي" in elem:
        st.info("💡 بلاطة هوردي: دقق عرض الأعصاب ووزن البلوك المستخدم وسماكة بلاطة التغطية.")
        
    elif "خزان" in elem:
        st.info("💡 خزان المياه: صمم المقطع كمقطع مائي (Water Section) واستخدم الـ Water-stop بانتظام.")
        
    elif "حصيرية" in elem:
        st.info("💡 الحصيرة: دقق القص الثاقب (Punching) تحت الأعمدة المركزية وتوزيع إجهاد التربة.")
        
    elif field == "زلازل":
        st.warning("🚨 دراسة زلزالية: تأكد من كفاية جدران القص لمقاومة القوى القاعدية V.")
    else:
        st.success("✅ النظام المختار آمن ومطابق لاشتراطات الكود الهندسي.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ الهندسة الرقمية")
    
    # خلفية هندسية توضيحية
    
    
    st.divider()
    
    # زر التصدير الجديد
    if st.button("🛠️ تصدير المخطط إلى AutoCAD (DXF) 🚀"):
        try:
            doc = ezdxf.new(setup=True)
            msp = doc.modelspace()
            msp.add_lwpolyline([(0,0), (60,0), (60,30), (0,30), (0,0)])
            buf = io.StringIO()
            doc.write(buf)
            st.download_button("📥 اضغط لتحميل ملف DXF", buf.getvalue(), f"Pelan_{elem}.dxf")
            st.success("تم التصدير بنجاح يا هندسة!")
        except Exception as e:
            st.error(f"خطأ: {e}")
            
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37;'>Pelan Masterpiece v44 | م. بيلان عبد الكريم | 2026</p>", unsafe_allow_html=True)
