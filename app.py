import streamlit as st
import pandas as pd
import numpy as np

# إعدادات البرنامج
st.set_page_config(page_title="Syria Structural Enterprise v2.0", layout="wide")

st.title("🏗️ المنظومة الهندسية الشاملة 100% (جميع العناصر + الانزياح + التكاليف)")
st.info("بلاطات، جسور، أعمدة، قواعد، انزياح طابقي، وحساب كميات وتكاليف")

# --- الشريط الجانبي ---
with st.sidebar:
    st.header("⚙️ الإعدادات العامة")
    n_stories = st.number_input("عدد الطوابق", min_value=1, value=3)
    fc = st.number_input("f'c (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)
    st.divider()
    st.subheader("💰 تقدير التكاليف")
    price_conc = st.number_input("سعر متر الخرسانة", value=1500000)
    price_steel = st.number_input("سعر طن الحديد", value=12000000)
    st.divider()
    st.subheader("🌍 معاملات الزلازل")
    zone_val = st.slider("معامل المنطقة Z", 0.075, 0.30, 0.15)

# --- إدخال بيانات الطوابق المخصصة ---
st.header("📑 مدخلات الطوابق المترابطة")
story_inputs = []
cols = st.columns(6)
titles = ["الطابق", "الارتفاع H (m)", "عرض الجسر (mm)", "عمق الجسر (mm)", "العمود (mm)", "البحر L (m)"]
for i, title in enumerate(titles): cols[i].write(f"**{title}**")

for i in range(n_stories, 0, -1):
    c = st.columns(6)
    with c[0]: st.write(f"Story {i}")
    with c[1]: h = st.number_input(f"H_{i}", value=3.0, label_visibility="collapsed")
    with c[2]: b_b = st.number_input(f"BB_{i}", value=300, label_visibility="collapsed")
    with c[3]: h_b = st.number_input(f"HB_{i}", value=600, label_visibility="collapsed")
    with c[4]: dim_c = st.number_input(f"DC_{i}", value=400, label_visibility="collapsed")
    with c[5]: span = st.number_input(f"L_{i}", value=6.0, label_visibility="collapsed")
    story_inputs.append({"story": i, "h": h, "b_b": b_b, "h_b": h_b, "dim_c": dim_c, "L": span})

# --- المحرك الإنشائي الكلي ---
def run_master_engine(data_list):
    results = []
    total_conc = 0
    total_steel_kg = 0
    accumulated_load = 0
    total_weight_seismic = 0
    
    # حساب الوزن للزلازل
    for s in data_list:
        total_weight_seismic += (s['L']**2) * 8.5 # Load approx
    v_base = zone_val * (2.5/5.5) * total_weight_seismic
    
    for s in data_list:
        # 1. الأحمال والتسليح (Beams)
        w_ult = 13.5 # kN/m2 approx
        load_on_beam = w_ult * (s['L'] / 2)
        accumulated_load += (s['L']**2) * w_ult
        d = s['h_b'] - 50
        mu = (load_on_beam * s['L']**2) / 8
        as_req = (mu * 10**6) / (0.9 * fy * 0.9 * d)
        
        # 2. حساب الانزياح الطابقي (Story Drift)
        # الانزياح يتناسب طردياً مع القوة وعكسياً مع الجساءة (Inertia)
        inertia = (s['dim_c']**4) / 12
        calculated_drift = (v_base * (s['h']**3)) / (3 * 25000 * inertia / 10**6) * 1000
        drift_limit = s['h'] * 1000 * 0.005
        drift_status = "✅ محقق" if calculated_drift <= drift_limit else "❌ فشل"
        
        # 3. الكميات
        vol_c = (s['b_b']*s['h_b']*s['L']/10**6) + (s['dim_c']**2*s['h']/10**6)
        total_conc += vol_c
        steel_beam = (as_req * 7850 / 10**6) * s['L'] * 1.2 # تقريبي مع الأساور
        total_steel_kg += steel_beam
        
        results.append({
            "الطابق": f"Story {s['story']}",
            "تسليح الجسر (T14)": f"{int(np.ceil(as_req/154))} سفلي / 2 علوي",
            "الانزياح (mm)": round(calculated_drift, 2),
            "حالة الانزياح": drift_status,
            "الخرسانة (m³)": round(vol_c, 2)
        })
        
    # 4. تصميم القاعدة (Foundation) للطابق الأرضي
    footing_dim = np.sqrt((accumulated_load * 1.1) / 200) # إجهاد التربة 200
    
    return pd.DataFrame(results), total_conc, total_steel_kg, footing_dim

# --- العرض والنتائج ---
if st.button("🚀 تشغيل النظام المتكامل 100%"):
    df, t_c, t_s, f_dim = run_master_engine(story_inputs)
    
    st.divider()
    st.subheader("📊 مخرجات التحليل والتصميم الشامل")
    st.table(df)
    
    

    st.subheader("🏗️ تصميم القواعد والكميات الكلية")
    c1, c2, c3 = st.columns(3)
    c1.metric("أبعاد القاعدة المنفردة", f"{round(f_dim, 2)} x {round(f_dim, 2)} m")
    c2.metric("إجمالي الخرسانة", f"{round(t_c, 2)} m³")
    c3.metric("إجمالي الحديد", f"{round(t_s/1000, 2)} Ton")

    # حساب التكلفة
    total_cost = (t_c * price_conc) + (t_s/1000 * price_steel)
    st.success(f"💰 التكلفة التقديرية الإجمالية للمشروع: {total_cost:,.0f} ليرة سورية")

    

    # تصدير
    st.download_button("📥 تصدير المذكرة الحسابية", df.to_csv().encode('utf-8'), "Full_Project_Data.csv")

st.markdown("---")
st.write("للتواصل والدعم الفني: **0998449697**")
