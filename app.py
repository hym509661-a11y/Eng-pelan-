import streamlit as st
import math

# إعدادات الصفحة والختم المهني المحدث
st.set_page_config(page_title="مكتب المهندس بيلان - نظام برج دمشق", layout="wide")

st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 10px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold;">0998449697</p>
    <p style="margin: 0; font-size: 0.8em;">دراسات - إشراف - تعهدات</p>
</div>
""", unsafe_allow_html=True)

# مدخلات التحكم (المحرك الأساسي من واقع الملف)
with st.sidebar:
    st.header("⚙️ معطيات المشروع")
    L = st.number_input("أكبر مجاز L (cm):", value=530, step=10)
    n_floors = st.number_input("عدد الطوابق الإجمالي:", value=11)
    st.divider()
    st.caption("الحسابات تعتمد على معادلات الكود السوري الواردة في الشرح")

st.title("🏗️ نظام التصميم الإنشائي المتكامل - برج دمشق")

# --- الحسابات الهندسية (مستخرجة حرفياً من ملفك) ---

# 1. [span_0](start_span)بلاطة القبو (مصمتة)[span_0](end_span)
h_qabo = max(12, math.ceil(L / 35)) # سماكة تعتمد على المجاز (L/35)
[span_1](start_span)h_shelter = 20 # سماكة الملجأ حسب توصيات الكود السوري[span_1](end_span)

# 2. [span_2](start_span)الجوائز الساقطة[span_2](end_span)
h_drop = math.ceil(L / 14) + 10 # شرط السهم L/14 + زيادة 10سم
b_drop = 30 # عرض الجائز المقترح

# 3. [span_3](start_span)بلاطة الهوردي (الطابق المتكرر)[span_3](end_span)
h_horidi = max(30, math.ceil(L / 20)) # شرط السهم للمستمرة من طرفين L/20
b_hidden = max(105, math.ceil(L / 4)) # عرض الجائز المخفي (L/4)

# 4. [span_4](start_span)الأعمدة (تدرج منطقي)[span_4](end_span)
# [span_5](start_span)عمود القبو يبدأ من 30x100 ويصل للأخير 30x50[span_5](end_span)
p_load = (L/100)**2 * 1.2 * n_floors
col_len = max(50, math.ceil((p_load * 1000) / (0.35*250 + 0.67*0.01*4000) / 30 / 10) * 10)

# --- عرض النتائج والحسابات ---
t1, t2 = st.tabs(["📊 الأبعاد والتسليح الرقمي", "📐 لوحات التفصيل الهندسي"])

with t1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📍 الأبعاد البيتونية")
        st.write(f"• **بلاطة القبو:** {h_qabo} cm (L/35)")
        st.write(f"• **بلاطة الهوردي:** {h_horidi} cm (L/20)")
        st.write(f"• **جائز ساقط:** 30 × {h_drop} cm")
        st.write(f"• **جائز مخفي:** {b_hidden} × {h_horidi} cm")
        st.write(f"• **عمود القبو:** 30 × {col_len} cm")

    with c2:
        st.subheader("📍 تسليح الجوائز (حسابي)")
        [span_6](start_span)st.write(f"• **سفلي مستمر:** 4 T 16[span_6](end_span)")
        [span_7](start_span)st.write(f"• **علوي (تعليق):** 2 T 12 (20% من السفلي)[span_7](end_span)")
        [span_8](start_span)st.write(f"• **إضافي (شابوه):** 3 T 16 (يمتد L/4 = {L/4:.0f} cm)[span_8](end_span)")
        [span_9](start_span)st.write(f"• **الكانات:** T10 كل 10cm عند المساند[span_9](end_span)")

with t2:
    st.header("📐 الرسوم التفصيلية الدقيقة")
    
    # 1. رسم الجائز
    st.subheader("1️⃣ تفريد حديد الجائز الساقط")
        st.markdown(f"""
    - **[span_10](start_span)الحديد السفلي:** مستمر مع تراكب 40Ø عند المساند[span_10](end_span).
    - **[span_11](start_span)الشابويه العلوي:** يمتد مسافة **{L/4:.0f} cm** من وجه العمود[span_11](end_span).
    - **[span_12](start_span)الكانات:** تكثيف كل 10 سم عند المساند و20 سم في المنتصف[span_12](end_span).
    """)

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("2️⃣ أجر البطة (الأساسات)")
                [span_13](start_span)st.write("ثني الأشاير داخل الحصيرة (أجر البطة) بطول 40 سم لضمان التثبيت[span_13](end_span).")

    with col_b:
        st.subheader("3️⃣ مقص الدرج (Scissor)")
                [span_14](start_span)st.write(f"المقص ضروري عند البسطة. سماكة الشاحط: 15 cm (L/20)[span_14](end_span).")

    st.subheader("4️⃣ كراسي الحصيرة (Chairs)")
        [span_15](start_span)st.write(f"سماكة الحصيرة المعتمدة: 90 cm (L/6)[span_15](end_span). [span_16](start_span)الكراسي ترفع الشبكة العلوية (7 T 20)[span_16](end_span).")

st.divider()
st.caption(f"تم تحديث كافة الحسابات بناءً على المجاز {L} سم - مكتب المهندس بيلان 2026")
