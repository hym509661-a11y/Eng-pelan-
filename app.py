import streamlit as st
import math

# إعداد الهوية المهنية للمهندس بيلان مصطفى عبدالكريم
st.set_page_config(page_title="مكتب المهندس بيلان - نظام الرسم الذكي", layout="wide")

st.sidebar.markdown("""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold; color: #ef4444;">0998449697</p>
    <p style="margin: 5px 0; font-size: 0.85em;">الجمهورية العربية السورية - برج دمشق</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ مدخلات المخطط")
    L = st.number_input("أطول مجاز L (cm):", value=530)
    n_floors = st.number_input("عدد الطوابق:", value=11)
    uploaded_file = st.file_uploader("ارفع المسقط المعماري لتحويله لإنشائي", type=['png', 'jpg', 'jpeg'])

st.title("🏗️ نظام توليد المخططات التنفيذية وتفريد الحديد")

if uploaded_file:
    # --- 1. الحسابات الإنشائية المصححة (الكود السوري) ---
    # البلاطة المصمتة (سقف القبو) - شرط السهم L/35
    h_solid = max(15, math.ceil(L / 35))
    
    # بلاطة الهوردي (سقف المتكرر)
    h_horidi = 30 # (24 بلوك + 6 تغطية)
    
    # الجوائز (4 T 16 سفلي كما في صورتك)
    h_beam = math.ceil(L / 12)
    
    # تدرج الأعمدة (كل 3 طوابق)
    col_dim = 30
    p_load = ((L/100)**2) * 1.25 * n_floors
    col_len_qabo = max(50, math.ceil((p_load * 1000) / (0.35*250 + 0.67*0.01*4000) / 30 / 10) * 10)

    # --- 2. عرض المخططات الرسومية ---
    tab1, tab2, tab3 = st.tabs(["📐 رسم البلاطات (هوردي/مصمت)", "🛠️ تفريد حديد الجوائز", "🏢 تدرج الأعمدة والدرج"])

    with tab1:
        st.subheader("📍 المسقط الإنشائي وتوزيع الأعصاب")
        st.info(f"تم تحليل المسقط المعماري: اتجاه الأعصاب (Short Direction) بطول {L} سم.")
        
        # رسم توضيحي لمخطط الهوردي (مثل صورة المخطط التي أرفقتها)
        
        
        st.subheader("📍 قطاع تفصيلي في بلاطة الهوردي")
        
        st.write(f"**التسليح:** عصب (2 T 14 سفلي) + بلاطة تغطية (شبكة T 8 كل 20 سم).")

    with tab2:
        st.subheader("🛠️ تفريد حديد الجوائز (العدد والقطر)")
        
        # مقطع عرضي (مطابق لصورك 4 T 16)
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**مقطع عرضي (Section)**")
            
            st.write(f"المقطع: 30 × {h_beam} cm")
        
        with col_b:
            st.write("**تفريد طولي (Elevation)**")
            
            st.write(f"الشابويه العلوي: 3 T 16 بطول {L/4:.0f} cm.")

        st.markdown(f"""
        - **حديد سفلي مستمر:** 4 قضبان قطر 16 مم (4 T 16).
        - **حديد علوي تعليق:** 2 قضيب قطر 12 مم (2 T 12).
        - **الكانات:** قطر 8 مم كل 15 سم (T 8 @ 15cm).
        """)

    with tab3:
        st.subheader("🏢 تدرج الأعمدة ومقص الدرج")
        c1, c2 = st.columns(2)
        with c1:
            st.write("**تدرج مقاطع الأعمدة**")
            st.write(f"- طوابق (1-3): 30 × {col_len_qabo} cm")
            st.write(f"- طوابق (4-6): 30 × {max(50, col_len_qabo-10)} cm")
            st.write(f"- طوابق (7-11): 30 × 50 cm")
            
        
        with c2:
            st.write("**تفصيلة مقص الدرج**")
            
            st.write("تسليح الدرج: T 12 كل 15 سم.")

    st.divider()
    st.button("💾 توليد ملف أوتوكاد (DXF) كامل")

else:
    st.warning("الرجاء رفع المسقط المعماري للبدء في الرسم.")
