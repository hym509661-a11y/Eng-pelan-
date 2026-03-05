import streamlit as st
import math

# إعدادات الصفحة والختم المهني
st.set_page_config(page_title="مكتب المهندس بيلان - برج دمشق", layout="wide")

st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 10px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 5px 0; font-weight: bold; color: #ef4444;">0998449697</p>
    <p style="margin: 0; font-size: 0.9em;">دراسات - إشراف - تعهدات</p>
</div>
""", unsafe_allow_html=True)

# مدخلات التحكم (المحرك الأساسي)
with st.sidebar:
    st.header("⚙️ متغيرات المشروع")
    L = st.number_input("طول أكبر مجاز L (cm):", value=530, step=10)
    n_floors = st.slider("عدد الطوابق:", 1, 15, 11)
    st.divider()
    st.info("تتغير الحسابات والرسوم تلقائياً بتغير المجاز L")

st.title("🏗️ النظام المتكامل للتصميم ورسم التسليح")

# --- الحسابات المرتبطة بالمجاز L (حسب تقريرك) ---

# 1. البلاطات
h_qabo = max(12, math.ceil(L / 35))  # بلاطة مصمتة (شرط السهم L/35)
h_horidi = max(30, math.ceil(L / 20)) # بلاطة هوردي (شرط السهم L/20)

# 2. الجوائز
h_beam_drop = math.ceil((L / 14) + 10) # جائز ساقط (L/14 + أمان)
b_beam_hidden = max(105, math.ceil(L / 4)) # جائز مخفي (عرضه L/4)

# 3. الأعمدة (مساحة التحميل مرتبطة بـ L)
# فرض مساحة تحميل العمود = (L/100 * L/100) متر مربع
p_total = ((L/100)**2) * 1.2 * n_floors 
col_len = max(50, math.ceil((p_total * 1000) / (0.35*250 + 0.67*0.01*4000) / 30 / 10) * 10)

# --- عرض النتائج والحسابات ---
tab1, tab2 = st.tabs(["📊 جداول البيانات الديناميكية", "📐 لوحات التسليح التفصيلية"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📍 الأبعاد الخرسانية")
        st.table({
            "العنصر": ["بلاطة القبو", "بلاطة الهوردي", "جائز ساقط", "جائز مخفي (عرض)", "عمود القبو"],
            "المعادلة": ["L / 35", "L / 20", "L / 14 + 10", "L / 4", "P / (0.35fc)"],
            "النتيجة (cm)": [h_qabo, h_horidi, f"30 × {h_drop}", b_beam_hidden, f"30 × {col_len}"]
        })
    with c2:
        st.subheader("📍 تقدير كميات الحديد")
        st.write(f"• **حديد الجائز السفلي:** 4 T 16")
        st.write(f"• **حديد الشابويات (علوي):** 3 T 16 (بطول {L/4:.0f} cm)")
        st.write(f"• **أشاير الأعمدة:** {math.ceil(col_len/10)*2} T 16")

with tab2:
    st.header("📐 التفاصيل الإنشائية الرسمية")
    
    st.markdown("### 1. تفصيلة الجائز والشابويات (Beam Reinforcement)")
    
    st.write(f"توزع الشابويات عند المساند لمسافة **{L/4:.0f} cm** من وجه العمود.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 2. أجر البطة (Base Hook)")
        
        st.write("ثني الحديد داخل القاعدة لضمان التثبيت (Anchorage).")

    with col_b:
        st.markdown("### 3. مقص الدرج (Scissor Joint)")
        
        st.write(f"سماكة الشاحط المعتمدة: 15 cm (بناءً على 290/20).")

    st.markdown("### 4. كراسي الحصيرة والشبكتين")
    
    st.write(f"توضع الكراسي لحمل الشبكة العلوية بارتفاع {max(90, math.ceil(L/6))-15} cm.")

st.divider()
st.caption(f"تم الربط البرمجي الكامل بناءً على المجاز L = {L} cm - م. بيلان")
