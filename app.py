import streamlit as st
import numpy as np

# إعداد الصفحة لتكون بعرض كامل وتصميم هندسي
st.set_page_config(page_title="Jawad Structural System - Syrian Code", layout="wide")

# تخصيص الألوان لتشبه نظام ويندوز الكلاسيكي الذي يفضله الجواد
st.markdown("""
    <style>
    .main { background-color: #f0f0f0; }
    .stButton>button { width: 100%; background-color: #004a99; color: white; border-radius: 0px; }
    .stTextInput>div>div>input { background-color: #ffffff; }
    .report-box { border: 1px solid #000; padding: 20px; background-color: white; font-family: 'Courier New', Courier, monospace; }
    </style>
    """, unsafe_allow_index=True)

# --- القائمة الجانبية (مثل قوائم الجواد) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1048/1048953.png", width=80)
    st.title("نظام الجواد")
    st.write("الإصدار الهندسي 2026")
    st.divider()
    menu = st.radio("اختر المهمة:", [
        "دراسة جائز مستمر مع أعمدة",
        "تصميم جدران استنادية",
        "أساسات منفردة ومشتركة",
        "تفريد حديد الأدراج"
    ])
    st.divider()
    st.info("الكود المعتمد: الكود العربي السوري")

# --- الواجهة الرئيسية حسب اختيار القائمة ---
if menu == "دراسة جائز مستمر مع أعمدة":
    st.header("📋 دراسة الجوائز المترابطة مع الأعمدة")
    
    # تقسيم المدخلات لمجموعات (مثل تبويبات الجواد)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🏗️ أبعاد العناصر")
        L = st.number_input("طول البحر (L) م", value=6.0)
        b = st.number_input("عرض الجائز (b) مم", value=300)
        h = st.number_input("ارتفاع الجائز (h) مم", value=600)
        
    with col2:
        st.subheader("⚖️ الأحمال (kN/m)")
        g = st.number_input("الحمولات الميتة (g)", value=25.0)
        p = st.number_input("الحمولات الحية (p)", value=12.0)
        
    with col3:
        st.subheader("🔩 الأعمدة والارتباط")
        c_dim = st.number_input("بعد العمود (D) مم", value=400)
        h_story = st.number_input("ارتفاع الطابق (H) م", value=3.0)
        fixity = st.selectbox("نوع الاتصال", ["اتصال صلب (Frame)", "استناد بسيط"])

    st.divider()
    
    if st.button("إجراء التحليل الإنشائي والتصميم"):
        # محرك الحساب (بناءً على الجساءة)
        wu = 1.2 * g + 1.6 * p
        # حساب العزوم مع أخذ جساءة العمود بعين الاعتبار (تبسيط لمنطق الجواد)
        k_beam = (b * h**3 / 12) / L
        k_col = (c_dim**4 / 12) / h_story
        df = k_beam / (k_beam + 2 * k_col) # معامل التوزيع
        
        mu_neg = (wu * L**2 / 12) * df # العزم السالب عند المسند
        mu_pos = (wu * L**2 / 8) - (mu_neg) # العزم الموجب
        
        # عرض النتائج بطريقة المذكرة الحسابية
        st.subheader("📄 المذكرة الحسابية الناتجة")
        
        with st.container():
            st.markdown('<div class="report-box">', unsafe_allow_index=True)
            res1, res2 = st.columns(2)
            with res1:
                st.write(f"**الحمل التصميمي:** {wu} kN/m")
                st.write(f"**العزم السالب (المسند):** {round(mu_neg, 2)} kNm")
                st.write(f"**العزم الموجب (الفتحة):** {round(mu_pos, 2)} kNm")
            with res2:
                # تفريد الحديد (الناتج الذي يشتهر به الجواد)
                as_neg = int((mu_neg * 10**6) / (0.9 * 400 * 0.9 * (h-50)))
                as_pos = int((mu_pos * 10**6) / (0.9 * 400 * 0.9 * (h-50)))
                st.write(f"**تسليح المساند:** {as_neg} mm²")
                st.write(f"**تسليح الفتحة:** {as_pos} mm²")
            
            st.markdown('</div>', unsafe_allow_index=True)

        st.divider()
        st.subheader("🎨 تفريد الحديد (Reinforcement Detailing)")
        
        # هنا تظهر الرسومات التي تطلبها
        
        
        st.write("**الجدول المقترح لتفريد الأسياخ:**")
        df_bars = pd.DataFrame({
            "المكان": ["علوي (مساند)", "سفلي (فتحة)", "أساور (عقدة)", "أساور (فتحة)"],
            "التسليح": [f"{int(as_neg/154)+1} T14", f"{int(as_pos/154)+1} T14", "Φ8 @ 100mm", "Φ8 @ 200mm"],
            "الطول (m)": [round(L/3, 2), round(L+0.4, 2), "-", "-"]
        })
        st.table(df_bars)

# التوقيع الثابت (الختم)
st.markdown("---")
st.write("للتواصل والدعم الفني: **0998449697**")
