import streamlit as st
import math

# إعداد الصفحة والختم المهني المعتمد
st.set_page_config(page_title="مكتب المهندس بيلان مصطفى", layout="wide")

st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 10px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold;">دراسات-اشراف-تعهدات</p>
    <p style="margin: 5px 0; color: #ef4444; font-size: 1.1em;">0998449697</p>
</div>
""", unsafe_allow_html=True)

# مدخلات التحكم (المحرك الأساسي لجميع العناصر)
with st.sidebar:
    st.header("⚙️ معطيات المجاز والتحكم")
    L = st.number_input("طول المجاز L (cm):", value=530, step=10)
    n_floors = st.number_input("عدد الطوابق الإجمالي:", value=11)
    st.divider()
    st.caption("كافة الحسابات والرسوم أدناه مرتبطة ديناميكياً بالمجاز L")

st.title("🏗️ النظام الإنشائي المتكامل - برج دمشق")

# --- الحسابات المرتبطة بالمجاز L (وفق المذكرة الحسابية) ---

# 1. البلاطات
h_solid = max(12, math.ceil(L / 35))   # البلاطة المصمتة (سقف القبو)
h_horidi = max(30, math.ceil(L / 20))  # البلاطة الهوردي (المتكرر)

# 2. الجوائز
h_drop = math.ceil(L / 14) + 10        # الجائز الساقط (L/14 + 10)
b_hidden = max(105, math.ceil(L / 4))  # الجائز المخفي (عرضه L/4)

# 3. الأعمدة (تدرج 30xL بناءً على حمولة المجاز وعدد الطوابق)
# مساحة تحميل العمود A = L*L | الحمولة P = A * 1.2 * n_floors
p_total = ((L/100)**2) * 1.2 * n_floors
col_len = max(50, math.ceil((p_total * 1000) / (0.35*250 + 0.67*0.01*4000) / 30 / 10) * 10)

# --- عرض النتائج ولوحات التسليح ---
tab1, tab2 = st.tabs(["📊 جداول الأبعاد والحديد", "📐 لوحات التفصيل والرسم الهندسي"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📍 الأبعاد البيتونية النهائية")
        st.info(f"• **بلاطة القبو (مصمتة):** {h_solid} cm")
        st.info(f"• **بلاطة المتكرر (هوردي):** {h_horidi} cm")
        st.info(f"• **جائز ساقط:** 30 × {h_drop} cm")
        st.info(f"• **جائز مخفي (عرض):** {b_hidden} cm")
        st.info(f"• **عمود القبو:** 30 × {col_len} cm")
    
    with c2:
        st.subheader("📍 جداول تسليح العناصر")
        st.write(f"• **حديد الجائز السفلي:** 4 T 16 مستمر")
        st.write(f"• **إضافي علوي (شابوه):** 3 T 16 يمتد {L/4:.0f} cm")
        st.write(f"• **الكانات:** T10 كل 10cm عند المساند")
        st.write(f"• **تسليح العمود:** {math.ceil(col_len/10)*2} T 16")

with tab2:
    st.header("📐 الرسوم التفصيلية الدقيقة للحديد")
    
    # 1. رسم تفريد حديد الجائز
    st.subheader("1️⃣ تفريد حديد الجائز (علوي، سفلي، إضافي)")
    st.image("https://raw.githubusercontent.com/EngineeringIcons/Files/main/beam_detail.png", caption="رسم تفصيلي للجائز يوضح الشابويات والحديد المستمر")
    st.markdown(f"- **الشابويات:** حديد إضافي علوي يمتد مسافة **{L/4:.0f} cm** من وجه العمود.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("2️⃣ أجر البطة (أشاير الأعمدة)")
        st.image("https://raw.githubusercontent.com/EngineeringIcons/Files/main/duck_foot.png", caption="تفصيلة أجر البطة في الحصيرة")
        st.write("ثني الأشاير داخل القاعدة بطول لا يقل عن 40 cm لضمان التثبيت.")

    with col_b:
        st.subheader("3️⃣ مقص الدرج (Scissor Joint)")
        st.image("https://raw.githubusercontent.com/EngineeringIcons/Files/main/stair_scissor.png", caption="تفصيلة المقص في تسليح الدرج")
        st.write("ضروري عند التقاء الشاحط بالبسطة لمنع انفصال الخرسانة.")

    st.subheader("4️⃣ كراسي الحصيرة (Chairs)")
    st.image("https://raw.githubusercontent.com/EngineeringIcons/Files/main/raft_chairs.png", caption="توزيع الكراسي لحمل الشبكة العلوية")
    st.write(f"ارتفاع الكرسي المعتمد: {max(90, math.ceil(L/6))-15} cm.")

st.divider()
st.caption(f"تم التقيد حرفياً بمعايير المذكرة الحسابية لبرج دمشق - المجاز الحالي {L} cm")
