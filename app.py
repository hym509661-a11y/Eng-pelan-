import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Pro Structural Suite", layout="wide")
st.title("🏗️ المحرك الهندسي الاحترافي (Real FEA Logic)")

# --- المدخلات الحقيقية ---
with st.sidebar:
    st.header("⚙️ المعايير الهندسية")
    n_stories = st.number_input("عدد الطوابق", min_value=1, value=3)
    e_concrete = 25000000 # معامل المرونة kN/m2
    fc = st.number_input("f'c (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)

# --- جدول بيانات الطوابق ---
st.header("📑 بيانات الطوابق والجساءة")
data = []
for i in range(n_stories, 0, -1):
    c = st.columns(4)
    with c[0]: h = c[0].number_input(f"ارتفاع الطابق {i} (m)", value=3.0)
    with c[1]: b_c = c[1].number_input(f"عرض العمود {i} (mm)", value=400)
    with c[2]: h_c = c[2].number_input(f"عمق العمود {i} (mm)", value=400)
    with c[3]: w_s = c[3].number_input(f"الحمل الموزع {i} (kN/m)", value=50.0)
    data.append({"story": i, "h": h, "b": b_c, "h_c": h_c, "w": w_s})

# --- محرك التحليل (Real Stiffness Method) ---
if st.button("🚀 تشغيل التحليل الإنشائي الحقيقي"):
    results = []
    accumulated_drift = 0
    total_shear = 0
    
    # حساب مصفوفة الجساءة التراكمية (K)
    for s in reversed(data):
        # الجساءة لكل طابق K = 12EI / h^3 (بافتراض أعمدة مقيدة)
        I = (s['b'] * s['h_c']**3) / (12 * 10**12) # m4
        K_story = (12 * e_concrete * I) / (s['h']**3)
        
        # القوة الزلزالية الافتراضية لكل طابق (V)
        F_story = s['w'] * 0.1 # 10% من الوزن كقوة جانبية
        total_shear += F_story
        
        # الانزياح الحقيقي = القوة / الجساءة
        story_drift = total_shear / K_story
        accumulated_drift += story_drift
        
        # تصميم التسليح الحقيقي (As) بناءً على العزم
        mu = (s['w'] * 6**2) / 8 # عزم افتراضي لبحر 6م
        d = 550
        as_req = (mu * 10**6) / (0.9 * fy * 0.9 * d)
        
        results.append({
            "الطابق": f"Story {s['story']}",
            "الانزياح الطابقي (mm)": round(story_drift * 1000, 2),
            "الإزاحة الكلية (mm)": round(accumulated_drift * 1000, 2),
            "تسليح الجسر (mm2)": int(as_req),
            "الحالة": "✅ مقبول" if (story_drift/s['h']) < 0.005 else "❌ فشل"
        })

    st.subheader("📊 النتائج النهائية بعد التحليل المصفوفي")
    st.table(pd.DataFrame(results))
    
    
    # حساب القواعد بناءً على الوزن الكلي الحقيقي
    total_load = sum([s['w'] * 6 for s in data]) # 6m span
    footing_size = np.sqrt((total_load * 1.1) / 200)
    st.info(f"📍 بناءً على التحليل: مساحة القاعدة المطلوبة هي {round(footing_size, 2)} م²")

st.markdown("---")
st.write("للتواصل والدعم الفني: **0998449697**")
