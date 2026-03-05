import streamlit as st
import math

# إعدادات الواجهة المهنية
st.set_page_config(page_title="المكتب الهندسي - م. بيلان", layout="wide")

# الختم الرسمي حسب طلبك
st.sidebar.markdown(f"""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center; font-family: 'Arial';">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold; color: #333;">دراسات - إشراف - تعهدات</p>
    <p style="margin: 5px 0; color: #ef4444; font-size: 1.2em;">0998449697</p>
</div>
""", unsafe_allow_html=True)

# محرك المتغيرات في الشريط الجانبي
with st.sidebar:
    st.markdown("---")
    st.header("⚙️ معطيات التصميم الديناميكية")
    L = st.number_input("أدخل طول المجاز L (cm):", value=530, step=10)
    n_floors = st.slider("عدد طوابق البرج:", 1, 15, 11)
    st.info("تنبيه: تغيير المجاز يؤدي لإعادة حساب كامل المنشأ تلقائياً.")

st.title("🏗️ نظام التصميم الإنشائي المتكامل - إصدار 2026")

# --- 1. الحسابات الهندسية المرتبطة كلياً بالمجاز L ---

# البلاطات
h_qabo = max(12, math.ceil(L / 35)) # بلاطة القبو المصمتة (L/35)
h_horidi = max(30, math.ceil(L / 20)) # بلاطة الهوردي (L/20)

# الجوائز
h_beam_drop = math.ceil(L / 14) + 10 # الجائز الساقط (L/14 + 10cm)
b_beam_hidden = max(105, math.ceil(L / 4)) # الجائز المخفي (عرض L/4)

# الأعمدة (مساحة التحميل مرتبطة بـ L^2)
area_load = (L/100) * (L/100) # مساحة التحميل التقريبية بالامتار
total_load = area_load * 1.2 * n_floors # الحمولة الكلية (طن)
col_length = max(50, math.ceil((total_load * 1000 / (0.35*250 + 0.67*0.01*4000)) / 30 / 10) * 10)

# الأساسات
h_raft = max(90, math.ceil(L / 6)) # الحصيرة (L/6)

# --- 2. عرض النتائج والرسوم ---
tab1, tab2 = st.tabs(["📊 جداول الأبعاد والتسليح", "📐 اللوحات الإنشائية التفصيلية"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📍 الأبعاد الخرسانية المعتمدة")
        st.success(f"• **بلاطة القبو (L/35):** {h_qabo} cm")
        st.success(f"• **بلاطة الهوردي (L/20):** {h_horidi} cm")
        st.success(f"• **جائز ساقط:** 30 × {h_beam_drop} cm")
        st.success(f"• **جائز مخفي:** {b_beam_hidden} × {h_horidi} cm")
        st.success(f"• **عمود القبو:** 30 × {col_length} cm")

    with col_b:
        st.subheader("📍 تفاصيل حديد التسليح")
        st.write(f"• **سفلي مستمر (جائز):** 4 T 16")
        st.write(f"• **إضافي علوي (شابوه):** 3 T 16 يمتد {L/4:.0f} cm")
        st.write(f"• **حديد بلاطة القبو:** شبكة T10 كل 15cm")
        st.write(f"• **تسليح الحصيرة:** شبكتين T20 كل 15cm")

with tab2:
    st.header("📐 لوحات الـ Shop Drawings")
    
    # 1. تفصيلة الجائز
    st.subheader("1️⃣ تفريد حديد الجائز (العلوي والسفلي)")
    
    st.markdown(f"**الشابويات:** حديد إضافي علوي لمقاومة العزم السالب، يمتد لمسافة **{L/4:.0f} cm** من وجه العمود.")

    # 2. أجر البطة ومقص الدرج
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.subheader("2️⃣ تفصيلة أجر البطة")
        
        st.write("ثني أشاير الأعمدة داخل الحصيرة لضمان نقل الأحمال.")

    with col_d2:
        st.subheader("3️⃣ مقص الدرج (Scissor Joint)")
        
        st.write("يمنع انفصال الخرسانة عند البسطة. السماكة: 15 cm.")

    # 4. كراسي الحصيرة
    st.subheader("4️⃣ كراسي الحصيرة (Chairs)")
    
    st.write(f"توزع الكراسي لحمل الشبكة العلوية بارتفاع **{h_raft-15} cm**.")

st.divider()
st.caption(f"تصميم ديناميكي مربوط بالمجاز {L} cm - المهندس بيلان مصطفى")
