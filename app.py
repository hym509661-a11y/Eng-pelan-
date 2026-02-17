import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Professional Structural Suite v3.0", layout="wide")
st.title("🏗️ المحرك الإنشائي المتقدم (التسليح المتغير والدقيق)")

# --- المدخلات العامة ---
with st.sidebar:
    st.header("⚙️ معايير التصميم")
    n_stories = st.number_input("عدد الطوابق", min_value=1, value=3)
    fc = st.number_input("f'c (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)
    L_span = st.number_input("طول البحر (m)", value=6.0)
    zone_z = st.slider("معامل المنطقة Z", 0.075, 0.30, 0.15)

# --- إدخال بيانات الطوابق ---
st.header("📑 بيانات الطوابق المخصصة")
input_data = []
cols = st.columns(4)
titles = ["الطابق", "الارتفاع (m)", "أبعاد العمود (mm)", "الحمل الحي (kN/m²)"]
for i, t in enumerate(titles): cols[i].write(f"**{t}**")

for i in range(n_stories, 0, -1):
    c = st.columns(4)
    with c[0]: st.write(f"Story {i}")
    with c[1]: h = c[1].number_input(f"H_{i}", value=3.0, label_visibility="collapsed")
    with c[2]: dim_c = c[2].number_input(f"C_{i}", value=400, label_visibility="collapsed")
    with c[3]: ll = c[3].number_input(f"LL_{i}", value=3.0, label_visibility="collapsed")
    input_data.append({"story": i, "h": h, "dim_c": dim_c, "ll": ll})

# --- محرك التحليل الديناميكي والتسليح ---
if st.button("🚀 تشغيل التحليل وتوليد المخططات"):
    results = []
    # حساب الوزن الكلي وقص القاعدة
    w_dead = 7.0 # kN/m2
    total_w = sum([(w_dead + 0.25 * s['ll']) * L_span**2 for s in input_data])
    v_base = zone_z * (2.5 / 5.5) * total_w
    
    # حساب العزوم والتسليح لكل طابق بشكل منفصل
    for idx, s in enumerate(input_data):
        # 1. العزم الناتج عن الأحمال الشاقولية (Gravity Moment)
        w_ult = 1.2 * w_dead + 1.6 * s['ll']
        m_gravity = (w_ult * (L_span/2) * L_span**2) / 10 # عزم تقريبي لجسر مستمر
        
        # 2. العزم الناتج عن القوى الجانبية (Seismic Moment - يزداد للأسفل)
        # القوة الجانبية عند الطابق i تزداد حسب ارتفاعه
        floor_level = sum([x['h'] for x in input_data[idx:]])
        m_seismic = (v_base * (idx + 1) / n_stories) * s['h'] / 4 # توزيع القوى
        
        # العزم التصميمي الكلي
        m_total = m_gravity + m_seismic
        
        # 3. حساب التسليح (SAFE Method)
        d = 550 # العمق الفعال لجسر 600 مم
        rn = (m_total * 10**6) / (0.9 * 300 * d**2)
        rho = (0.85 * fc / fy) * (1 - np.sqrt(1 - (2 * rn / (0.85 * fc))))
        as_req = max(rho * 300 * d, 0.0033 * 300 * d)
        
        # تحويل المساحة إلى عدد أسياخ (قطر 14مم)
        n_bars = int(np.ceil(as_req / 154))
        
        results.append({
            "الطابق": f"Story {s['story']}",
            "العزم الكلي (kNm)": round(m_total, 1),
            "التسليح السفلي (mm²)": int(as_req),
            "التسليح (قطر 14)": f"{n_bars} T14",
            "الانزياح (mm)": round((n_stories - idx) * 1.4, 2)
        })

    st.subheader("📊 النتائج النهائية (التسليح المتغير حسب الطابق)")
    st.table(pd.DataFrame(results))
    
    
    st.success("لاحظ الآن كيف يتغير التسليح والعزوم بناءً على موقع الطابق والقوى المؤثرة.")

# التذييل المطلوب
st.markdown("---")
st.write("للتواصل والدعم الفني: **0998449697**")
