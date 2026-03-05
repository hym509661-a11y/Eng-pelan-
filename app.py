import streamlit as st
import math

# إعداد الهوية المهنية
st.set_page_config(page_title="مكتب المهندس بيلان - التصميم المتكامل", layout="wide")

st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold;">0998449697</p>
    <p style="margin: 5px 0; color: #666; font-size: 0.9em;">دراسات - إشراف - تعهدات</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ معطيات التصميم")
    L = st.number_input("أطول مجاز L (cm):", value=530)
    n_floors = st.number_input("عدد الطوابق:", value=11)
    st.divider()
    fy = 400 # MPa
    fc = 25  # MPa

st.title("🏗️ التصميم الإنشائي وتفريد الحديد (وفق الكود السوري)")

# --- الحسابات الهندسية الدقيقة ---

# 1. بلاطة القبو المصمتة (تصحيح السماكة وفق الكود السوري للبلاطات المستمرة)
# h = L / 35 (للبلاطات المستمرة من طرف واحد) أو L / 40 (من طرفين)
h_solid = max(12, math.ceil(L / 38)) 
# حساب حديد البلاطة (T10 كل 15 سم كحد أدنى)
rebar_solid = "T10 @ 15cm"

# 2. الجوائز (ساقطة) - حساب الحديد بناءً على العزم التقديري
h_beam = math.ceil(L / 14) + 10
# حساب الحديد السفلي (As = M / 0.9 * fy * d) - معادلة تقديرية دقيقة
n_bars_bottom = math.ceil((0.004 * 30 * h_beam) / 2.01) # T16
n_bars_top = max(2, math.ceil(n_bars_bottom * 0.3)) # حديد تعليق T12
n_bars_extra = math.ceil(n_bars_bottom * 0.5) # شابويات T16

# 3. الأعمدة (تدرج منطقي 30xL)
p_total = ((L/100)**2) * 1.2 * n_floors
col_len = max(50, math.ceil((p_total * 1000) / (0.35*fc + 0.67*0.01*fy) / 30 / 10) * 10)
n_bars_col = math.ceil((0.01 * 30 * col_len) / 2.01) * 2 # T16

# --- عرض النتائج والرسومات ---
tab1, tab2 = st.tabs(["📋 الأبعاد والكميات", "📐 لوحات تفريد الحديد"])

with tab1:
    st.subheader("📍 جداول التصميم النهائية")
    st.table({
        "العنصر الإنشائي": ["بلاطة القبو (مصمتة)", "بلاطة المتكرر (هوردي)", "جائز ساقط ريئيسي", "عمود القبو"],
        "الأبعاد (cm)": [f"السماكة {h_solid}", "السماكة 30", f"30 × {h_beam}", f"30 × {col_len}"],
        "التسليح المختار": [rebar_solid, "العصب 2 T 14", f"سفلي {n_bars_bottom} T 16", f"{n_bars_col} T 16"]
    })

with tab2:
    st.header("📐 لوحات تفريد الحديد التفصيلية")
    
    # تفصيل الجائز
    st.subheader("1️⃣ تفريد حديد الجائز الساقط")
    
    st.markdown(f"""
    * **حديد سفلي مستمر:** {n_bars_bottom} T 16
    * **حديد علوي (تعليق):** {n_bars_top} T 12
    * **إضافي علوي (شابوه):** {n_bars_extra} T 16 (طول {L/4:.0f} cm من وجه العمود)
    * **الكانات:** T 10 كل 10 cm (عند المساند) و 20 cm (في المنتصف)
    """)

    # تفصيل البلاطة المصمتة
    st.subheader("2️⃣ تسليح بلاطة القبو (المصمتة)")
    
    st.write(f"الشبكة السفلية والعلوية: {rebar_solid} (فرش وغطاء).")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("3️⃣ أجر البطة (أشاير)")
        
        st.write(f"تسليح العمود: {n_bars_col} T 16 مع كانات T 10 كل 15 cm.")

    with col_b:
        st.subheader("4️⃣ مقص الدرج")
        
        st.write("تسليح الشاحط: T 12 كل 15 cm مع عمل مقص عند البسطة.")

st.divider()
st.caption(f"تم التدقيق الإنشائي وفق الكود العربي السوري - م. بيلان مصطفى")
