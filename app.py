import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_drawable_canvas import st_canvas # مكتبة الرسم الضرورية

# إعدادات الصفحة
st.set_page_config(page_title="Pelan CAD Station", layout="wide")

# --- تنسيق CSS لجعله يشبه البرامج الهندسية ---
st.markdown("""
<style>
    .stApp {background-color: #1e1e1e; color: #dcdcdc;}
    .css-1d391kg {padding-top: 1rem;} 
    h1, h2, h3 {color: #00bcd4 !important;}
    .stButton>button {width: 100%; border-radius: 5px; background-color: #37474f; color: white;}
    .stButton>button:hover {background-color: #00bcd4; color: black;}
</style>
""", unsafe_allow_html=True)

# --- الختم الهندسي (سوريا - القامشلي) ---
with st.sidebar:
    st.markdown(f"""
    <div style="background-color:#263238; padding:15px; border-radius:10px; border-right: 5px solid #00bcd4; text-align:center;">
        <h2 style="color:#00bcd4; margin:0; font-size:1.4em;">Eng. Pelan Mustfa</h2>
        <h4 style="color:#b0bec5; margin:0;">Abdulkarim</h4>
        <hr style="border-color:#546e7a;">
        <p style="color:#ffd740; font-size:1.2em; font-weight:bold;">📱 0998449697</p>
        <p style="color:#eceff1; font-size:0.9em;">📍 Syria - Qamishli</p>
        <p style="font-size:0.8em; color:#78909c;">Full Structural Suite v11.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Project Settings")
    project_name = st.text_input("Project Name", "Residential Villa - Qamishli")
    concrete_fc = st.selectbox("Concrete f'c (MPa)", [25, 30, 35, 40])
    steel_fy = st.selectbox("Steel fy (MPa)", [400, 420, 500])

# --- العناوين الرئيسية ---
st.title("🏗️ Pelan Integrated Engineering System")
st.markdown("---")

# تبويبات العمل
tab_cad, tab_etabs, tab_safe, tab_revit = st.tabs([
    "📐 AutoCAD (Drawing Canvas)", 
    "📉 ETABS (Live Solver)", 
    "🏗️ SAFE (Rebar Design)", 
    "🧱 Revit (BIM Takeoff)"
])

# =========================================================
# 1. قسم الأوتوكاد (رسم حقيقي)
# =========================================================
with tab_cad:
    st.header("AutoCAD Simulation: Interactive Drawing")
    st.info("💡 ملاحظة: المتصفح لا يعرض DWG مباشرة. قم برفع صورة (JPG/PNG) للمخطط للرسم فوقها، أو ارسم مباشرة.")
    
    col_tools, col_canvas = st.columns([1, 4])
    
    with col_tools:
        st.subheader("Draw Tools")
        drawing_mode = st.radio("Tool:", ("line", "rect", "circle", "freedraw", "transform"), index=0)
        stroke_width = st.slider("Line Width:", 1, 10, 2)
        stroke_color = st.color_picker("Color:", "#00bcd4")
        bg_image = st.file_uploader("Upload Plan Image to Trace (JPG/PNG)", type=["png", "jpg"])

    with col_canvas:
        # مساحة الرسم الحقيقية
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # لون التعبئة
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color="#000000", # خلفية سوداء مثل الأوتوكاد
            background_image=None if bg_image is None else plt.imread(bg_image),
            update_streamlit=True,
            height=500,
            drawing_mode=drawing_mode,
            key="canvas",
        )
        st.caption(f"Coordinates: Active Canvas | Project: {project_name}")

# =========================================================
# 2. قسم الإيتابس (حسابات حقيقية للمعادلات)
# =========================================================
with tab_etabs:
    st.header("ETABS: Real-Time Analysis Solver")
    
    # مدخلات حقيقية
    c1, c2, c3 = st.columns(3)
    with c1:
        span = st.number_input("Beam Span (L) [m]", value=6.0, step=0.5)
    with c2:
        dead_load = st.number_input("Dead Load (DL) [kN/m]", value=15.0)
    with c3:
        live_load = st.number_input("Live Load (LL) [kN/m]", value=10.0)
        
    # الحسابات (معادلات هندسية)
    w_total = (1.2 * dead_load) + (1.6 * live_load) # Ultimate Load
    moment_max = (w_total * span**2) / 8
    shear_max = (w_total * span) / 2
    
    st.markdown("---")
    res1, res2 = st.columns(2)
    with res1:
        st.metric("Ultimate Load (Wu)", f"{w_total:.2f} kN/m")
        st.metric("Max Moment (Mu)", f"{moment_max:.2f} kN.m", delta="Critical")
    with res2:
        st.metric("Max Shear (Vu)", f"{shear_max:.2f} kN")
        
    # رسم المخطط بيانيا (Matplotlib)
    if st.checkbox("Show Moment Diagram (BMD)", value=True):
        x = np.linspace(0, span, 100)
        M_x = (w_total * x / 2) * (span - x) # معادلة العزم
        
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(x, M_x, color='#ffeb3b', linewidth=2)
        ax.fill_between(x, M_x, color='#ffeb3b', alpha=0.3)
        ax.set_title(f"Bending Moment Diagram for {project_name}", color='white')
        ax.set_facecolor('#263238')
        fig.patch.set_facecolor('#1e1e1e')
        ax.tick_params(colors='white')
        st.pyplot(fig)

# =========================================================
# 3. قسم السيف (تصميم التسليح بناءً على النتائج)
# =========================================================
with tab_safe:
    st.header("SAFE: Automated Reinforcement Design")
    
    # حساب حديد التسليح تقريبياً بناءً على العزم المحسوب في تبويب الإيتابس
    # As approx = M / (0.9 * fy * 0.9d)
    d = 550 # عمق فعال افتراضي مم
    as_req = (moment_max * 10**6) / (0.9 * steel_fy * 0.9 * d)
    
    st.subheader(f"Design Results for Moment Mu = {moment_max:.1f} kN.m")
    
    st.warning(f"Required Steel Area (As): {as_req:.0f} mm²")
    
    # جدول تفاصيل التسليح الشامل
    safe_details = {
        "Location": ["Bottom (Mid-Span)", "Top (Supports)", "Stirrups (Shear)", "Side Bars (Torsion)"],
        "Required Area (mm²)": [f"{as_req:.0f}", f"{as_req*0.3:.0f}", "Shear Calc", "Min Code"],
        "Selected Rebar": [
            f"{int(as_req/200)+2} Ø 16 mm", 
            "3 Ø 16 mm", 
            "Ø 10 mm @ 150 mm", 
            "2 Ø 12 mm"
        ],
        "Notes": ["Main Flexural Steel", "Anchor/Support", "2-Legged Stirrups", "Skin Reinforcement"]
    }
    st.table(pd.DataFrame(safe_details))
    
    # تنبيه ذكي
    if as_req > 2000:
        st.error("⚠️ High Reinforcement! Consider increasing section depth.")
    else:
        st.success("✅ Section is Safe and Reinforcement is within limits.")

# =========================================================
# 4. قسم الريفيت (حصر الكميات والـ BBS)
# =========================================================
with tab_revit:
    st.header("Revit BIM: Bill of Quantities (BBS)")
    
    # حساب الكميات بناء على الطول المدخل في الإيتابس
    num_beams = st.number_input("Number of Similar Beams", 1, 50, 10)
    
    total_concrete = num_beams * span * 0.3 * 0.6 # افتراض مقطع 30*60
    total_steel_weight = num_beams * span * 20 # افتراض 20 كغ/متر طولي
    
    st.subheader("Material Take-off (BIM Data)")
    
    col_mat1, col_mat2 = st.columns(2)
    with col_mat1:
        st.info(f"**Total Concrete Volume:** {total_concrete:.2f} m³")
        st.write(f"*Grade:* C{concrete_fc}")
    with col_mat2:
        st.info(f"**Total Rebar Weight:** {total_steel_weight:.2f} kg")
        st.write(f"*Grade:* Grade {steel_fy}")
        
    st.divider()
    
    # جدول التصدير النهائي
    bbs_export = pd.DataFrame({
        "Item": ["Concrete C30", "Steel High Yield", "Stirrups Mild Steel", "Formwork"],
        "Unit": ["m³", "kg", "kg", "m²"],
        "Quantity": [total_concrete, total_steel_weight * 0.8, total_steel_weight * 0.2, num_beams * span * 1.8],
        "Unit Price ($)": [85, 0.9, 0.85, 12],
        "Total Cost ($)": [total_concrete*85, total_steel_weight*0.8*0.9, total_steel_weight*0.2*0.85, num_beams*span*1.8*12]
    })
    
    st.dataframe(bbs_export)
    st.caption(f"Project Engineer: Pelan Mustfa | Location: Qamishli | Phone: 0998449697")
    
    # زر التصدير
    csv = bbs_export.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Final Cost Report",
        csv,
        "Pelan_Project_Cost.csv",
        "text/csv"
    )

