import streamlit as st
import math

# إعدادات الواجهة المهنية
st.set_page_config(page_title="مكتب المهندس بيلان - التصميم الإنشائي", layout="wide")

# الختم الرسمي حسب المعطيات المحفوظة
st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center; font-family: 'Arial';">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold; color: #333;">دراسات - إشراف - تعهدات</p>
    <p style="margin: 5px 0; color: #ef4444; font-size: 1.2em;">0998449697</p>
</div>
""", unsafe_allow_html=True)

# مدخلات التحكم (الديناميكية)
with st.sidebar:
    st.markdown("---")
    st.header("⚙️ معطيات الكود السوري")
    L = st.number_input("أطول مجاز L (cm):", value=530, step=10)
    n_floors = st.slider("عدد الطوابق الإجمالي:", 1, 15, 11)
    st.divider()
    fc = 25 # MPa
    fy = 400 # MPa

st.title("🏗️ نظام التصميم الإنشائي المتكامل - برج دمشق")

# --- الحسابات المرتبطة بالمجاز L وفق الكود السوري ---

# 1. البلاطات (شرط السهم)
h_solid = max(12, math.ceil(L / 35)) # بلاطة القبو (L/35)
h_horidi = max(30, math.ceil(L / 20)) # بلاطة الهوردي (L/20 للمستمرة)

# 2. الجوائز
h_drop = math.ceil(L / 14) + 10 # الجائز الساقط (L/14 + 10cm أمان)
b_hidden = max(105, math.ceil(L / 4)) # الجائز المخفي (عرض L/4)

# 3. الأعمدة (تدرج منطقي حسب الطوابق والحمل التراكمي)
# مساحة التحميل A = L*L | الحمولة P = A * 1.2 * n
load_area = (L/100)**2 
p_ton = load_area * 1.2 * n_floors
# المقطع (العرض ثابت 30): الطول = P / (0.35*fc + 0.67*0.01*fy)
col_len = max(50, math.ceil((p_ton * 1000) / (0.35*fc + 0.67*0.01*fy) / 30 / 10) * 10)

# 4. الحصيرة
h_raft = max(90, math.ceil(L / 6))

# --- عرض النتائج ولوحات الرسم ---
tab1, tab2 = st.tabs(["📊 البيانات والحسابات", "📐 لوحات التسليح التفصيلية"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📍 الأبعاد الخرسانية")
        st.write(f"• **بلاطة القبو:** {h_solid} cm")
        st.write(f"• **بلاطة الهوردي:** {h_horidi} cm")
        st.write(f"• **جائز ساقط:** 30 × {h_drop} cm")
        st.write(f"• **جائز مخفي:** {b_hidden} × {h_horidi} cm")
        st.write(f"• **عمود القبو:** 30 × {col_len} cm")

    with c2:
        st.subheader("📍 حساب الحديد (BBS)")
        st.write(f"• **سفلي مستمر:** 4 T 16")
        st.write(f"• **علوي (شابوه):** 3 T 16 (بطول {L/4:.0f} cm من الوجه)")
        st.write(f"• **كانات الجائز:** T10 @ 10cm (تكثيف المساند)")
        st.write(f"• **تسليح العمود:** {math.ceil(col_len/10)*2} T 16")

with tab2:
    st.header("📐 الرسوم التفصيلية (Shop Drawings)")
    
    st.subheader("1️⃣ تفريد حديد الجائز والشابويات")
    
    st.markdown(f"**الشابويات:** حديد إضافي علوي يمتد لمسافة **{L/4:.0f} cm** لمقاومة العزم السالب.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("2️⃣ تفصيلة أجر البطة (Base Hook)")
        
        st.write("ثني أشاير العمود داخل الحصيرة لضمان نقل القوى الشاقولية والزلزالية.")

    with col_b:
        st.subheader("3️⃣ مقص الدرج (Scissor Joint)")
        
        st.write("ضروري جداً لمنع انفصال الخرسانة عند البسطة. سماكة الشاحط: 15 cm.")

    st.subheader("4️⃣ كراسي الحصيرة (Chairs)")
    
    st.write(f"توزع الكراسي بارتفاع **{h_raft-15} cm** لحمل الشبكة العلوية الثقيلة (7 T 20).")

st.divider()
st.caption(f"تم الربط البرمجي للمجاز L = {L} cm وفق معايير الكود السوري - المهندس بيلان")
