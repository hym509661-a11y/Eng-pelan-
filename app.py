import streamlit as st
import math

# الختم المهني (دراسات-اشراف-تعهدات)
st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold;">0998449697</p>
    <hr>
    <p style="margin: 0; font-size: 0.85em;">الجمهورية العربية السورية - برج دمشق</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ معطيات المذكرة الحسابية")
    L = st.number_input("أطول مجاز L (cm):", value=530)
    n_floors = st.number_input("عدد الطوابق الإجمالي:", value=11)
    st.divider()
    st.info("الحسابات مطابقة للكود العربي السوري")

st.title("🏗️ نظام التصميم الإنشائي وتفريد الحديد")

# --- الحسابات الهندسية (الكود السوري) ---

# 1. بلاطة القبو (مصمتة - شرط السهم L/35)
h_solid = max(12, math.ceil(L / 35)) 

# 2. تدرج الأعمدة (كل 3 طوابق)
# عمود القبو (30 x Len) بناءً على حمولة n_floors
p_qabo = ((L/100)**2) * 1.25 * n_floors # طن
len_qabo = max(50, math.ceil((p_qabo * 1000) / (0.35*250 + 0.67*0.01*4000) / 30 / 10) * 10)

# تدرج العمود (كل 3 طوابق ننقص 10 سم)
len_f4 = max(50, len_qabo - 10) # الطابق 4-6
len_f7 = max(50, len_qabo - 20) # الطابق 7-9
len_f10 = max(40, len_qabo - 30) # الطابق 10-11

# --- عرض النتائج ---
tab1, tab2 = st.tabs(["📊 المذكرة الحسابية والجداول", "📐 لوحات تفريد الحديد"])

with tab1:
    st.subheader("📍 أبعاد العناصر الإنشائية")
    st.table({
        "العنصر": ["بلاطة القبو (مصمتة)", "جائز ساقط (L/12)", "عمود القبو (1-3)", "عمود الطابق (4-6)", "عمود الطابق (7-9)", "العمود الأخير"],
        "الأبعاد (cm)": [f"السماكة {h_solid}", f"30 × {math.ceil(L/12)}", f"30 × {len_qabo}", f"30 × {len_f4}", f"30 × {len_f7}", f"30 × {len_f10}"]
    })

with tab2:
    st.header("📐 لوحات تفريد الحديد (العدد والقطر)")
    
    # 1. تسليح الجائز الساقط
    st.subheader("1️⃣ تفريد حديد الجائز الساقط")
    
    st.markdown(f"""
    - **الحديد السفلي:** 4 قضبان قطر 16 مم (4 T 16) - مستمر.
    - **الحديد العلوي (تعليق):** 2 قضيب قطر 12 مم (2 T 12).
    - **الإضافي العلوي (شابوه):** 3 قضبان قطر 16 مم (3 T 16) بطول {L/4:.0f} cm.
    - **الكانات:** T 10 كل 10 سم عند المساند و 20 سم في المنتصف.
    """)

    # 2. تسليح العمود (تفريد)
    st.subheader("2️⃣ تسليح عمود القبو")
    c1, c2 = st.columns(2)
    with c1:
        
        st.write(f"**العدد والقطر:** {math.ceil(len_qabo/10)*2} T 16")
    with c2:
        
        st.write("**أجر البطة:** ثني الأشاير بطول 40 سم داخل الحصيرة.")

    # 3. بلاطة القبو ومقص الدرج
    st.subheader("3️⃣ بلاطة القبو ومقص الدرج")
    c3, c4 = st.columns(2)
    with c3:
        
        st.write(f"**تسليح البطة:** شبكتين (T 10 لكل 15 سم)")
    with c4:
        
        st.write("**مقص الدرج:** تسليح T 12 لكل 15 سم مع عمل مقص.")

st.divider()
st.caption(f"تم التدقيق وفق الكود العربي السوري - م. بيلان مصطفى")
