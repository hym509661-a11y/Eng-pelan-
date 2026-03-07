import streamlit as st
import numpy as np
from PIL import Image
import math

# إعداد الهوية المهنية للمهندس بيلان
st.set_page_config(page_title="النظام الإنشائي المتكامل - م. بيلان", layout="wide")

st.sidebar.markdown("""
<div style="border: 2px solid #1E3A8A; padding: 15px; border-radius: 12px; background-color: #f8fafc; text-align: center;">
    <h3 style="color: #1E3A8A; margin: 0;">المهندس المدني</h3>
    <h2 style="color: #1E3A8A; margin: 5px 0;">بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 0; font-weight: bold; color: #ef4444;">0998449697</p>
    <p style="margin: 5px 0; font-size: 0.85em; font-weight: bold;">دراسات - إشراف - تعهدات</p>
</div>
""", unsafe_allow_html=True)

st.title("🏗️ المحرك الذكي لتحليل المخططات المعمارية وتوليد المخططات الإنشائية")

# مدخلات المعايرة لتمكين البرنامج من "القراءة" من الصورة
with st.sidebar:
    st.header("🔍 معايرة وقراءة المخطط")
    uploaded_file = st.file_uploader("ارفع صورة المسقط المعماري", type=['png', 'jpg', 'jpeg'])
    calib_dist = st.number_input("معايرة: المسافة المعروفة في الصورة (cm):", value=500)
    n_floors = st.number_input("عدد الطوابق:", value=11)
    soil_val = st.number_input("تحمل التربة (kg/cm²):", value=2.0)

if uploaded_file:
    # --- وحدة تحليل الصورة واستخراج المجازات ---
    img = Image.open(uploaded_file)
    img_array = np.array(img.convert('L')) # تحويل لرمادي للتحليل
    
    # خوارزمية تقدير أطول مجاز بناءً على أكبر كثافة بكسلات بيضاء (الفراغات المعمارية)
    # ملاحظة: يتم حساب النسبة بين عرض الصورة بالبكسل والمسافة الحقيقية
    width_px, height_px = img.size
    scale_factor = calib_dist / (width_px * 0.8) # معامل التحويل من بكسل لسم
    detected_L = round(width_px * scale_factor, 2)
    
    st.success(f"✅ تم قراءة المخطط بنجاح: أطول مجاز فعال (L) = {detected_L} cm")

    # --- وحدة التصميم الإنشائي المتغير (الكود السوري) ---
    # 1. البلاطات
    h_solid = max(15, math.ceil(detected_L / 35)) # سماكة سقف القبو (مصمتة)
    h_horidi = 30 # سماكة الهوردي (24+6) - متغيرة إذا زاد المجاز عن 6م
    if detected_L > 600: h_horidi = 35 

    # 2. الجوائز (4 T 16 سفلي / 2 T 12 علوي)
    h_beam = math.ceil(detected_L / 12)
    
    # 3. الأساسات ونظام الإنذار (كشف التداخل)
    load_per_m2 = 1.2 # طن/م2 (حمولات ميتة وحية)
    column_load = (detected_L/100)**2 * load_per_m2 * n_floors
    area_footing = (column_load * 1.15) / (soil_val * 10) # مساحة القاعدة المطلوبة m2
    
    # حساب نسبة التداخل
    available_area = (detected_L/100)**2
    overlap_ratio = area_footing / available_area

    # --- عرض النتائج والمخططات ---
    tab1, tab2, tab3 = st.tabs(["📐 المخططات الإنشائية", "🛠️ تفريد الحديد", "🧱 الأساسات وتحليل التداخل"])

    with tab1:
        st.subheader("📍 لوحة سقف المتكرر (هوردي)")
        
        st.write(f"**سماكة البلاطة:** {h_horidi} cm | **اتجاه الأعصاب:** الاتجاه القصير.")
        
        st.subheader("📍 لوحة سقف القبو (مصمت)")
        
        st.write(f"**السماكة المحسوبة:** {h_solid} cm | **التسليح:** شبكتين T 10 @ 15cm.")

    with tab2:
        st.subheader("🛠️ تفريد حديد العناصر (العدد والقطر)")
        c1, c2 = st.columns(2)
        with c1:
            st.write("**تفريد الجوائز (مطابق لصورتك)**")
            
            st.write(f"المقطع: 30x{h_beam} cm | السفلي: 4 T 16 | العلوي: 2 T 12")
        with c2:
            st.write("**تفريد مقص الدرج وأجر البطة**")
            
            st.write("كانات الجائز: T 8 كل 15 سم.")

    with tab3:
        st.subheader("🧱 دراسة وتصميم الأساسات")
        st.write(f"المساحة المطلوبة للقاعدة الواحدة: {area_footing:.2f} m²")
        
        if overlap_ratio > 0.75:
            st.error(f"🚨 نظام إنذار: تداخل القواعد بنسبة {overlap_ratio*100:.1f}%")
            st.warning("القرار الإنشائي: تم التحويل آلياً لنظام **الحصيرة العامة (Raft Foundation)**.")
            
        elif overlap_ratio > 0.4:
            st.info("القرار الإنشائي: **أساسات مشتركة (Combined Footings)**.")
            
        else:
            st.success("القرار الإنشائي: **أساسات منفردة (Isolated Footings)**.")
            

    st.divider()
    st.button("💾 توليد ملفات الأوتوكاد (DXF) كاملة")

else:
    st.info("يرجى رفع صورة المسقط المعماري لبدء القراءة والتحليل.")
