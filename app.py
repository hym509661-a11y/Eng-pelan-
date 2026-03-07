import streamlit as st
import math
from PIL import Image

# إعداد الهوية المهنية للمهندس بيلان مصطفى عبدالكريم
st.set_page_config(page_title="المكتب الهندسي - م. بيلان", layout="wide")

# الختم المهني الثابت
st.sidebar.markdown("""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold; color: #ef4444;">0998449697</p>
    <p style="margin: 5px 0; font-size: 0.85em; font-weight: bold;">دراسات - إشراف - تعهدات</p>
</div>
""", unsafe_allow_html=True)

# واجهة المدخلات
with st.sidebar:
    st.header("📋 معطيات المخطط")
    uploaded_file = st.file_uploader("ارفع المسقط المعماري", type=['png', 'jpg', 'jpeg'])
    L = st.number_input("أطول مجاز صافي L (cm):", value=530)
    n_floors = st.number_input("عدد الطوابق:", value=11)
    soil_pressure = st.number_input("تحمل التربة (kg/cm²):", value=2.0)

st.title("🏗️ نظام التصميم الإنشائي المتكامل (مسمط - هوردي - أساسات)")

if uploaded_file:
    # الحسابات الإنشائية (الكود السوري)
    h_solid = max(15, math.ceil(L / 35)) # بلاطة القبو
    h_horidi = 30 # بلاطة المتكرر
    h_beam = math.ceil(L / 12) # الجوائز الساقطة
    
    # حسابات الأساسات وتداخلها
    p_load = ((L/100)**2) * 1.25 * n_floors # حمولة العمود (T)
    area_f = (p_load * 1.1) / (soil_pressure * 10) # مساحة القاعدة (m2)
    overlap_idx = (area_f / ((L/100)**2)) * 100

    # عرض النتائج
    t1, t2, t3 = st.tabs(["📐 المساقط الإنشائية", "🛠️ تفريد الحديد", "🧱 الأساسات والإنذار"])

    with t1:
        st.subheader("📍 لوحة سقف المتكرر (بلاطة هوردي)")
        
        st.write(f"**اتجاه الأعصاب:** الاتجاه القصير ({L} سم).")
        
        st.subheader("📍 لوحة سقف القبو (بلاطة مصمتة)")
        
        st.write(f"**سماكة البلاطة:** {h_solid} سم | **التسليح:** شبكتين T 10 @ 15cm.")

    with t2:
        st.subheader("🛠️ تفريد حديد الجوائز (مطابق للصور)")
        col1, col2 = st.columns(2)
        with col1:
            
            st.markdown(f"**مقطع الجائز:** 30x{h_beam} سم\n- سفلي: **4 T 16**\n- علوي: **2 T 12**")
        with col2:
            
            st.write(f"**طول الشابويه:** {L/4:.0f} سم.")

    with t3:
        st.subheader("🧱 دراسة تداخل الأساسات")
        if overlap_idx > 75:
            st.error(f"🚨 إنذار تداخل: نسبة المساحة المطلوبة {overlap_idx:.1f}%")
            st.warning("القرار: تم التحويل تلقائياً لنظام **الحصيرة العامة (Raft Foundation)**.")
            
        else:
            st.success(f"القرار: نظام **قواعد منفردة**. نسبة التداخل آمنة ({overlap_idx:.1f}%)")
            

    st.divider()
    st.button("💾 تصدير المخططات والمذكرة الحسابية")
else:
    st.info("الرجاء رفع المسقط المعماري للبدء.")
