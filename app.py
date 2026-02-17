import streamlit as st
import pandas as pd

# إعداد الواجهة
st.set_page_config(page_title="Syrian Code Analysis", layout="wide")
st.title("🏗️ نظام التحليل المتكامل - التدقيق وفق الكود السوري")

# مدخلات الكود السوري
st.sidebar.header("📋 معايير الكود السوري")
h_story = st.sidebar.number_input("ارتفاع الطابق الواحد (mm)", value=3000)
drift_limit_ratio = st.sidebar.slider("نسبة الإزاحة المسموحة (مثلاً 0.005)", 0.001, 0.010, 0.005, format="%.3f")

def analyze_with_syrian_code(stories, load):
    drift_limit = h_story * drift_limit_ratio
    results = []
    
    for s in range(1, stories + 1):
        # محاكاة إزاحة تزداد مع الارتفاع (في التحليل الحقيقي تأتي من مصفوفة الجساءة)
        calculated_drift = s * 2.2  # ملم (مثال)
        
        status = "✅ مقبول" if calculated_drift <= drift_limit else "❌ غير مقبول"
        
        results.append({
            "الطابق": s,
            "الإزاحة المحسوبة (mm)": calculated_drift,
            "الإزاحة المسموحة (mm)": drift_limit,
            "التحقق (Status)": status
        })
    return pd.DataFrame(results)

# المدخلات الأساسية
col1, col2 = st.columns(2)
with col1:
    stories = st.number_input("عدد الطوابق", min_value=1, value=5)
with col2:
    live_load = st.number_input("الحمل الحي (kN/m²)", value=3.0)

if st.button("تشغيل التحليل والتدقيق"):
    df = analyze_with_syrian_code(stories, live_load)
    
    st.subheader("📊 نتائج تدقيق الإزاحة (Drift Check)")
    
    # تنسيق الجدول لتلوين النتائج
    def color_status(val):
        color = 'green' if '✅' in val else 'red'
        return f'color: {color}; font-weight: bold'

    st.table(df.style.applymap(color_status, subset=['التحقق (Status)']))

    # تنبيه في حال وجود فشل
    if "❌ غير مقبول" in df["التحقق (Status)"].values:
        st.error("تنبيه: توجد طوابق تجاوزت الإزاحة المسموحة وفق الكود السوري. يرجى زيادة جساوة الجدران القصية (Shear Walls).")
    else:
        st.success("جميع الطوابق تحقق شروط الإزاحة وفق الكود السوري.")

st.markdown("---")
st.write("للتواصل والدعم الفني: **0998449697**")
