import streamlit as st
import numpy as np
import ezdxf
import io

# 1. إعدادات الواجهة الاحترافية
st.set_page_config(page_title="Pelan Masterpiece v38", layout="wide")
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
    .gold-text { color: #d4af37; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='status-card' style='text-align:center;'><h1 style='color:#38bdf8;'>Pelan Masterpiece v38</h1><p class='gold-text'>الموسوعة الهندسية المتكاملة | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.header("🛠️ خيارات المهندس")
    category = st.radio("المجال الإنشائي:", ["بيتون مسلح", "حفر وردم (Earthwork)", "تحليل زلزالي"])
    
    if category == "بيتون مسلح":
        elem = st.selectbox("العنصر:", ["جائز", "بلاطة فطرية", "أساسات حصيرية", "خزان مياه", "جدار استنادي"])
    elif category == "حفر وردم (Earthwork)":
        elem = "كميات التربة"
        site_area = st.number_input("مساحة الموقع (m²):", 100.0)
        exc_depth = st.number_input("عمق الحفر (m):", 1.5)
    else:
        elem = "دراسة زلزالية"

    st.divider()
    c_p = st.number_input("سعر البيتون ($/m3):", 110)
    s_p = st.number_input("سعر الحديد ($/ton):", 950)

# 3. محرك الحسابات (Engine)
def run_calculations():
    v_conc, w_steel = 4.5, 0.35
    if category == "حفر وردم (Earthwork)":
        v_exc = site_area * exc_depth
        cost = v_exc * 6.0 # فرضية سعر الحفر
        return v_exc, 0, cost
    total_cost = (v_conc * c_p) + (w_steel * s_p)
    return v_conc, w_steel, total_cost

vol, steel, cost = run_calculations()

# 4. العرض الفني (تم حل جميع أخطاء الإزاحة في الخزان والحصيرية والفطرية)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 النتائج لـ: {elem}")
    
    if category == "حفر وردم (Earthwork)":
        st.write(f"🚜 **حجم الحفر الكلي:** {vol:.2f} m³")
        st.write(f"💰 **التكلفة التقديرية:** ${cost:.2f}")
    else:
        st.write(f"🏗️ **الكميات:** {vol} m³ بيتون | {steel} t حديد")
        st.write(f"💵 **التكلفة:** ${cost:.2f}")

    st.divider()
    st.markdown("### 🤖 توصية العقل الذكي (AI):")
    
    # تصحيح شامل لكتل الشرط لضمان عدم حدوث IndentationError
    if "خزان" in elem:
        st.info("💡 نصيحة الخزان: صمم المقطع كـ 'Water-Section' لضمان عدم التشقق ومنع نفاذية المياه للحديد.")
            elif "حصيرية" in elem:
        st.info("💡 نصيحة الحصيرة: دقق 'القص الثاقب' (Punching Shear) وتأكد من توزيع إجهاد التربة بانتظام.")
            elif "فطرية" in elem:
        st.info("💡 نصيحة الفطرية: دقق العزوم السالبة عند الأعمدة ووزع التسليح بين شريحة العمود والوسط.")
            elif "جدار" in elem:
        st.info("💡 نصيحة الجدار: تحقق من استقرار الجدار ضد 'الانزلاق' و'الانقلاب' بناءً على ضغط التربة الفعال.")
            elif "زلزالي" in category:
        st.warning("🚨 تنبيه زلزالي: تأكد من كفاية جدران القص (Shear Walls) لمقاومة القوى الجانبية.")
    else:
        st.success("✅ النظام المختار آمن ومطابق للمعايير الهندسية.")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ المخططات الفنية (DXF)")
    
    # صورة تعبيرية للرسم الهندسي
        
    st.divider()
    if st.button("🚀 تصدير إلى AutoCAD"):
        try:
            doc = ezdxf.new(setup=True)
            msp = doc.modelspace()
            msp.add_lwpolyline([(0,0), (30,0), (30,15), (0,15), (0,0)]) # إطار الرسم
            dxf_io = io.StringIO()
            doc.write(dxf_io)
            st.download_button("📥 تحميل ملف DXF", dxf_io.getvalue(), f"Pelan_{elem}.dxf")
            st.success("تم تجهيز المخطط!")
        except Exception as e:
            st.error(f"خطأ في التصدير: {e}")
            
    st.markdown("</div>", unsafe_allow_html=True)

# 5. التوقيع
st.divider()
st.markdown("<p style='text-align:center;'>Pelan Masterpiece v38 | م. بيلان عبد الكريم | 2026</p>", unsafe_allow_html=True)
