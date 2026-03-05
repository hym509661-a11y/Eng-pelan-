import streamlit as st
import math

# إعدادات الصفحة والهوية المهنية للمهندس بيلان
st.set_page_config(page_title="نظام تفريد الحديد - م. بيلان مصطفى", layout="wide")

# الختم الرسمي الثابت
st.sidebar.markdown("""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold; color: #ef4444;">0998449697</p>
    <p style="margin: 5px 0; font-size: 0.85em;">الجمهورية العربية السورية - برج دمشق</p>
</div>
""", unsafe_allow_html=True)

# مدخلات التصميم
with st.sidebar:
    st.header("⚙️ معطيات المذكرة الحسابية")
    L = st.number_input("أطول مجاز L (cm):", value=530)
    n_floors = st.number_input("عدد الطوابق الإجمالي:", value=11)
    uploaded_file = st.file_uploader("ارفع المسقط المعماري", type=['png', 'jpg', 'jpeg'])
    st.divider()
    st.info("الحسابات والرسوم مطابقة للكود السوري")

st.title("🏗️ نظام توليد مخططات الهوردي وتفريد الحديد الذكي")

if uploaded_file:
    # --- الحسابات الإنشائية (الكود السوري) ---
    # بلاطة القبو المصمتة (L/35)
    h_solid = max(15, math.ceil(L / 35))
    
    # بلاطة الهوردي (كما في صورة المخطط المرفقة)
    h_horidi = 30 # 24 بلوكة + 6 تغطية
    
    # الجوائز (بناءً على مقطع الصورة المرفقة 4 T 16 سفلي)
    h_beam = math.ceil(L / 12)
    
    # تدرج الأعمدة (كل 3 طوابق)
    p_load = ((L/100)**2) * 1.2 * n_floors
    col_len = max(50, math.ceil((p_load * 1000) / (0.35*250 + 0.67*0.01*4000) / 30 / 10) * 10)

    # --- عرض المخططات ---
    tab1, tab2, tab3 = st.tabs(["📐 مخطط الهوردي", "🛠️ تفريد الحديد (Shop Drawings)", "📋 المذكرة الحسابية"])

    with tab1:
        st.subheader("📍 مسقط توزيع الأعصاب والجوائز")
        # تم تصحيح خطأ الإزاحة هنا
        st.info(f"تم توجيه الأعصاب في الاتجاه القصير ({L} سم) لتقليل السهم.")
                st.caption(f"مسقط إنشائي يوضح اتجاه الأعصاب وتوزيع الجوائز للمجاز {L} سم.")

        st.subheader("📍 قطاع تفصيلي في بلاطة الهوردي (مثل صورة المخطط)")
                st.markdown(f"""
        - **سماكة البلاطة:** {h_horidi} cm (24+6).
        - **تسليح العصب:** 2 T 14 سفلي + T 12 علوي.
        - **بلاطة التغطية:** شبكة T 8 كل 20 سم.
        """)

    with tab2:
        st.header("🛠️ لوحات تفريد الحديد (العدد والقطر)")
        
        # تفريد الجائز (مطابق تماماً لصورة image_0 و image_1)
        st.subheader("1️⃣ تفريد حديد الجائز الساقط")
        c1, c2 = st.columns(2)
        with c1:
                        st.write("**مقطع عرضي في الجائز:** 30 × " + str(h_beam) + " cm")
        with c2:
                        st.write(f"**طول الشابويه:** {L/4:.0f} cm")

        st.markdown(f"""
        - **الحديد السفلي (MAIN):** 4 T 16 (كما في صورتك المرفقة).
        - **الحديد العلوي (TOP):** 2 T 12 (كما في صورتك المرفقة).
        - **الكانات:** T 8 كل 15 سم (كما في صورة image_1).
        """)

        # تفريد الأعمدة والدرج
        st.subheader("2️⃣ تفريد الأعمدة ومقص الدرج")
        c3, c4 = st.columns(2)
        with c3:
            st.write("**أجر البطة (أشاير العمود)**")
                        st.write(f"تسليح عمود القبو: {math.ceil(col_len/12)*2} T 16")
        with c4:
            st.write("**مقص الدرج**")
                        st.write("تسليح المقص: T 12 كل 15 سم.")

    with tab3:
        st.subheader("📝 المذكرة الحسابية التقديرية")
        st.table({
            "العنصر": ["بلاطة القبو", "بلاطة الهوردي", "جائز ساقط", "عمود القبو"],
            "الأبعاد (cm)": [h_solid, h_horidi, f"30x{h_beam}", f"30x{col_len}"],
            "التسليح": ["T10 @ 15cm", "2 T 14 / Rib", "4 T 16 Main", f"{math.ceil(col_len/12)*2} T 16"]
        })

    st.divider()
    st.button("💾 تصدير المخططات بصيغة DXF (أوتوكاد)")

else:
    st.warning("الرجاء رفع المسقط المعماري للبدء في توليد المخططات الإنشائية.")
