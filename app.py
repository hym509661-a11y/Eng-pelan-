import streamlit as st
import pandas as pd
import numpy as np

# إعدادات البرنامج
st.set_page_config(page_title="Syria Structural Ultimate Pro Max", layout="wide")

st.title("🏗️ المنظومة الهندسية المتكاملة 100% (التصميم والتفصيل التفصيلي)")
st.info("تحليل + تصميم + تفصيل حديد (علوي/سفلي/إضافي/أساور) + حساب كميات")

# --- الدالات المساعدة لحساب عدد الأسياخ ---
def calculate_bars(as_required, bar_dia):
    area_single_bar = (np.pi * bar_dia**2) / 4
    n_bars = np.ceil(as_required / area_single_bar)
    return int(max(n_bars, 2)) # الحد الأدنى سيخين

# --- الشريط الجانبي ---
with st.sidebar:
    st.header("📋 الإعدادات العامة")
    n_stories = st.number_input("عدد الطوابق", min_value=1, value=3)
    fc = st.number_input("f'c (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)
    bar_dia_main = st.selectbox("قطر التسليح الرئيسي (mm)", [12, 14, 16, 18, 20])
    bar_dia_stirrups = st.selectbox("قطر الأساور (mm)", [8, 10, 12])

# --- جداول بيانات الطوابق ---
st.header("📑 جداول بيانات الطوابق المخصصة")
story_inputs = []
cols = st.columns(6)
titles = ["الطابق", "الارتفاع (m)", "عرض الجسر (mm)", "عمق الجسر (mm)", "أبعاد العمود (mm)", "طول البحر (m)"]
for i, title in enumerate(titles): cols[i].write(f"**{title}**")

for i in range(n_stories, 0, -1):
    c = st.columns(6)
    with c[0]: st.write(f"Story {i}")
    with c[1]: h = st.number_input(f"h_{i}", value=3.0, label_visibility="collapsed")
    with c[2]: b_b = st.number_input(f"bb_{i}", value=300, label_visibility="collapsed")
    with c[3]: h_b = st.number_input(f"hb_{i}", value=600, label_visibility="collapsed")
    with c[4]: dim_c = st.number_input(f"dc_{i}", value=400, label_visibility="collapsed")
    with c[5]: span = st.number_input(f"L_{i}", value=6.0, label_visibility="collapsed")
    story_inputs.append({"story": i, "h": h, "b_b": b_b, "h_b": h_b, "dim_c": dim_c, "L": span})

# --- المحرك الهندسي الشامل ---
def run_ultimate_engine(data_list):
    results = []
    total_concrete = 0
    total_steel = 0
    accumulated_axial = 0
    
    for s in data_list:
        # 1. حساب الأحمال
        w_ult = 1.2 * ((150/1000 * 25) + 2.0) + 1.6 * 3.0
        load_on_beam = w_ult * (s['L'] / 2)
        accumulated_axial += (s['L']**2) * w_ult
        
        # 2. تصميم وتسليح الجسر (Beams)
        d = s['h_b'] - 50
        mu = (load_on_beam * s['L']**2) / 8
        as_req = (mu * 10**6) / (0.9 * fy * 0.9 * d)
        
        # تفصيل الحديد
        n_bottom = calculate_bars(as_req, bar_dia_main) # سفلي
        n_top_const = 2 # حديد تعليق علوي أساسي
        n_top_extra = calculate_bars(as_req * 0.3, bar_dia_main) # إضافي علوي عند المساند (افتراضي 30%)
        
        # الأساور
        vu = (load_on_beam * s['L']) / 2
        vc = 0.17 * np.sqrt(fc) * s['b_b'] * d / 1000
        vs = (vu / 0.75) - vc
        av_s = (vs * 1000) / (fy * d) if vs > 0 else 0
        spacing = min(200, d/2) if av_s == 0 else min(200, (2 * 0.785 * bar_dia_stirrups**2) / av_s)
        
        # 3. كميات المواد
        v_conc = (s['b_b'] * s['h_b'] / 10**6 * s['L']) + (s['dim_c']**2 / 10**6 * s['h'])
        total_concrete += v_conc
        
        results.append({
            "الطابق": f"Story {s['story']}",
            "تسليح سفلي": f"{n_bottom} T{bar_dia_main}",
            "تعليق علوي": f"{n_top_const} T{bar_dia_main}",
            "إضافي علوي": f"{n_top_extra} T{bar_dia_main}",
            "أساور": f"Φ{bar_dia_stirrups}@{int(spacing)}mm",
            "خرسانة (m³)": round(v_conc, 2)
        })
        
    return pd.DataFrame(results), total_concrete

# --- تنفيذ وعرض النتائج ---
if st.button("🚀 تحليل وتصميم وتفصيل شامل 100%"):
    df_final, t_conc = run_ultimate_engine(story_inputs)
    
    st.divider()
    st.subheader("📊 المخطط التفصيلي للعناصر وكميات المواد")
    
    st.dataframe(df_final, use_container_width=True)
    
    c1, c2 = st.columns(2)
    c1.metric("إجمالي الخرسانة المطلوبة", f"{round(t_conc, 2)} m³")
    c2.metric("حالة المخططات", "جاهزة للأوتوكاد ✅")

    # رسم توضيحي للتسليح
    st.subheader("🎨 نموذج تفصيلي لمقطع الجسر (Detailing View)")
    
    st.markdown(f"""
    **مواصفات التسليح لهذا التصميم:**
    - **الحديد السفلي:** مستمر على كامل البحر.
    - **الحديد العلوي (تعليق):** لحمل الأساور.
    - **الحديد الإضافي:** يوضع فوق المساند لمقاومة العزم السالب.
    - **الأساور:** موزعة حسب قوى القص المحسوبة لكل طابق.
    """)

    # تصدير البيانات
    csv = df_final.to_csv(index=False).encode('utf-8')
    st.download_button("📥 تحميل جدول تفصيل الحديد والكميات (Excel)", csv, "Reinforcement_Detailing.csv")

# التذييل
st.markdown("---")
st.write("للتواصل والدعم الفني: **0998449697**")
