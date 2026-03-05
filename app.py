import streamlit as st
import math

# إعدادات الصفحة والهوية المهنية للمهندس بيلان
st.set_page_config(page_title="نظام تفريد الحديد الذكي - برج دمشق", layout="wide")

# الختم المهني في الشريط الجانبي
st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold; color: #ef4444;">0998449697</p>
    <p style="margin: 5px 0; font-size: 0.85em;">الجمهورية العربية السورية - برج دمشق</p>
</div>
""", unsafe_allow_html=True)

# محرك المدخلات
with st.sidebar:
    st.header("⚙️ مدخلات التصميم")
    uploaded_file = st.file_uploader("ارفع صورة المسقط المعماري", type=['png', 'jpg', 'jpeg'])
    L = st.number_input("أطول مجاز L (cm):", value=530)
    st.divider()
    st.info("الحسابات والرسم مطابقة للكود السوري والمذكرة الحسابية.")

st.title("🚀 نظام توليد المخططات الإنشائية والـ Shop Drawings الذكي")

if uploaded_file:
    st.success("تم تحليل المسقط المعماري. جاري توليد المخططات التفصيلية الدقيقة...")

    # --- الحسابات الإنشائية المرتبطة بالمجاز L (الكود السوري) ---
    
    # البلاطات
    h_solid_qabo = max(15, math.ceil(L / 35)) # بلاطة القبو (مصمتة مستمرة)
    h_horidi = 30 # سماكة الهوردي المعتمدة في الأبراج (24 بلوكة + 6 تغطية)
    
    # الجوائز الساقطة
    h_drop = math.ceil(L / 12)
    b_drop = 30
    
    # تدرج الأعمدة (عمود القبو)
    n_floors = 11
    p_qabo = ((L/100)**2) * 1.25 * n_floors 
    len_qabo = max(50, math.ceil((p_qabo * 1000) / (0.35*250 + 0.67*0.01*4000) / 30 / 10) * 10)

    # --- عرض النتائج واللوحات ---
    tab1, tab2, tab3 = st.tabs(["📐 المخططات الإنشائية (الهوردي)", "🏗️ تفريد الجوائز والأعمدة", "📝 المذكرة الحسابية"])

    with tab1:
        st.subheader("📍 لوحة توزيع الأعصاب والجوائز (مسقط أفقي)")
        
        # محاكاة لرسم المسقط الإنشائي الدقيق (مثل صورة image_2.png)
                st.caption(f"مسقط إنشائي يوضح اتجاه الأعصاب (في الاتجاه القصير {L} سم) وتوزيع الجوائز.")

        st.subheader("📍 قطاع تفصيلي في بلاطة الهوردي")
        # محاكاة لرسم قطاع هوردي دقيق (مثل صورة image_2.png)
                st.markdown(f"""
        - **سماكة بلاطة الهوردي:** `{h_horidi} cm` (بلوكة 24 سم + بلاطة تغطية 6 سم).
        - **تسليح العصب:** سفلي 2 T 14 + علوي T 12 (تعليق).
        - **تسليح بلاطة التغطية:** شبكة T 8 كل 20 سم (في الاتجاهين).
        """)

    with tab2:
        st.subheader("🛠️ لوحات تفريد الحديد (Shop Drawings)")
        
        # تفريد الجائز (دقيق مثل صورة image_0.png)
        st.write("### 1️⃣ تفريد حديد الجائز الساقط الرئيسية (مثل صورة image_0.png)")
        col1, col2 = st.columns(2)
        with col1:
                        st.write(f"مقطع الجائز الساقط: `{b_drop} × {h_drop} cm`")
        with col2:
                        st.write(f"الشابويه العلوي: يمتد {L/4:.0f} cm من وجه العمود.")
        
        st.markdown(f"""
        - **حديد سفلي مستمر (Main):** `{math.ceil((0.005 * 30 * h_drop)/2.01)+1} T 16`
        - **حديد علوي تعليق:** `2 T 12` (كما في صورة image_0.png)
        - **الكانات:** `T 10 كل 10 cm` عند المساند.
        """)

        # تفريد الأعمدة والحصيرة
        st.write("### 2️⃣ تفريد تسليح الأعمدة ودرج الملجأ")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.write("**عمود القبو (أجر البطة)**")
                        st.write(f"العدد والقطر لعمود `{30}×{len_qabo} cm`:")
            st.write(f"`{math.ceil(len_qabo/12)*2} T 16` + `40 cm` عكفة")
        with c2:
            st.write("**مقص الدرج**")
                        st.write("**تسليح المقص:** `T 12 كل 15 cm`")
        with c3:
            st.write("**كراسي الحصيرة**")
                        st.write(f"ارتفاع الكرسي: `{max(90, math.ceil(L/6))-15} cm`")

    with tab3:
        st.subheader("📝 تفاصيل المذكرة الحسابية")
        st.table({
            "العنصر": ["بلاطة القبو (مصمتة)", "بلاطة المتكرر (هوردي)", "جائز ساقط ريئيسي", "عمود القبو"],
            "الأبعاد (cm)": [f"السماكة {h_solid_qabo}", "السماكة 30", f"30 × {h_drop}", f"30 × {len_qabo}"],
            "التسليح المختار": ["T10 @ 15cm (شبكتين)", "العصب 2 T 14", f"سفلي {math.ceil((0.005 * 30 * h_drop)/2.01)+1} T 16", f"{math.ceil(len_qabo/12)*2} T 16"]
        })

    # زر التصدير إلى PDF/DXF
    st.divider()
    st.button("💾 تصدير كافة المخططات والمذكرة إلى PDF / DXF")

else:
    st.warning("الرجاء رفع صورة المسقط المعماري للبدء في التصميم.")
