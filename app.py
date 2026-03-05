import streamlit as st
import math

# إعدادات الواجهة المهنية والختم
st.set_page_config(page_title="مكتب المهندس بيلان - التصميم الإنشائي", layout="wide")

st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold;">دراسات - إشراف - تعهدات</p>
    <p style="margin: 5px 0; color: #ef4444; font-size: 1.1em;">0998449697</p>
</div>
""", unsafe_allow_html=True)

# مدخلات التحكم (المحرك الأساسي)
with st.sidebar:
    st.header("⚙️ مدخلات المذكرة الحسابية")
    L = st.number_input("أطول مجاز بين الأعمدة L (cm):", value=530, step=10)
    n_floors = st.slider("عدد الطوابق الإجمالي:", 1, 15, 11)
    st.divider()
    st.info("الحسابات أدناه مربوطة كلياً بالمجاز L وفق معايير الكود السوري")

st.title("🏗️ النظام الإنشائي المتكامل - إصدار برج دمشق")

# --- الحسابات الهندسية (مربوطة بـ L وفق الكود) ---

# 1. البلاطات (Slabs)
h_qabo = max(15, math.ceil(L / 30))  # بلاطة القبو (باعتبارها مسندة أو ملجأ)
h_horidi = max(30, math.ceil(L / 20)) # بلاطة هوردي (L/20)

# 2. الجوائز (Beams)
h_drop = math.ceil(L / 12) # الجائز الساقط (L/12 للمجالات الكبيرة)
b_hidden = max(100, math.ceil(L / 4)) # الجائز المخفي (العرض L/4)

# 3. الأعمدة (Columns) - تدرج منطقي (30 × طول)
# حمل المتر المربع (1.2 طن) * مساحة تحميل (L/100 * L/100) * عدد الطوابق
load_p = ((L/100)**2) * 1.2 * n_floors
# المعادلة: P = 0.35*fc*Ac + 0.67*fy*As | مع fc=25, fy=400, As=0.01Ac
col_length = max(50, math.ceil((load_p * 1000) / (0.35*250 + 0.67*0.01*4000) / 30 / 10) * 10)

# 4. الأساسات (Foundations)
h_raft = max(90, math.ceil(L / 6)) # سماكة الحصيرة (L/6)

# --- عرض النتائج ولوحات التسليح ---
tab1, tab2 = st.tabs(["📊 البيانات الحسابية", "📐 الرسوم وتفاصيل التسليح"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📍 الأبعاد الخرسانية")
        st.write(f"• **سماكة بلاطة القبو:** {h_qabo} cm")
        st.write(f"• **سماكة بلاطة الهوردي:** {h_horidi} cm")
        st.write(f"• **أبعاد الجائز الساقط:** 30 × {h_drop} cm")
        st.write(f"• **عرض الجائز المخفي:** {b_hidden} cm")
        st.write(f"• **عمود القبو:** 30 × {col_length} cm")
    
    with c2:
        st.subheader("📍 تفاصيل حديد التسليح")
        st.write(f"• **السفلي:** 4 T 16 مستمر")
        st.write(f"• **الإضافي العلوي (شابوه):** 3 T 16 (يمتد {L/4:.0f} cm)")
        st.write(f"• **الكانات:** T10 @ 10cm (تكثيف عند المساند)")
        st.write(f"• **تسليح العمود:** {math.ceil(col_length/10)*2} T 16")

with tab2:
    st.header("📐 اللوحات التفصيلية (Shop Drawings)")
    
    st.subheader("1️⃣ تسليح الجائز (علوي وسفلي)")
    
    st.markdown(f"**تنبيه:** يتم تمديد الشابويات (الحديد الإضافي) لمسافة **{L/4:.0f} cm** من وجه المسند.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("2️⃣ أجر البطة (Base Anchors)")
        
        st.write("تشريك أعمدة القبو مع الحصيرة باستخدام (أجر البطة) بطول 40-50 سم.")

    with col_b:
        st.subheader("3️⃣ مقص الدرج (Scissor Joint)")
        
        st.write("تفصيلة المقص ضرورية عند التقاء الشاحط بالبسطة لمنع الانفصال.")

    st.subheader("4️⃣ كراسي الحصيرة (Chairs)")
    
    st.write(f"توزع الكراسي بارتفاع **{h_raft-15} cm** لحمل الشبكة العلوية (T20).")

st.divider()
st.caption(f"تصميم مربوط بالمجاز L = {L} cm - الكود السوري - م. بيلان")
