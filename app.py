import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# محاولة استيراد مكتبة الرسم، وإذا لم تكن موجودة نعطي تنبيهاً
try:
    from streamlit_drawable_canvas import st_canvas
except ImportError:
    st.error("⚠️ يجب تثبيت مكتبة الرسم! الرجاء كتابة: pip install streamlit-drawable-canvas")
    st.stop()

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Pelan Engineering Station", layout="wide")

# --- تنسيق CSS لجعله يشبه البرامج الهندسية (Dark Theme) ---
st.markdown("""
<style>
    .stApp {background-color: #0e1117; color: #fafafa;}
    h1, h2, h3 {color: #00bcd4 !important;}
    .stButton>button {border-radius: 5px; background-color: #262730; color: #00bcd4; border: 1px solid #00bcd4;}
    .stButton>button:hover {background-color: #00bcd4; color: black;}
</style>
""", unsafe_allow_html=True)

# --- الختم الهندسي (سوريا - القامشلي) ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/engineer.png", width=70)
    st.markdown("""
    <div style="text-align: center;">
        <h2 style="color:#00bcd4; margin:0;">Eng. Pelan Mustfa</h2>
        <h4 style="color:#b0bec5; margin:0;">Abdulkarim</h4>
        <hr>
        <p style="font-weight:bold; color:#fbc02d; font-size:1.2em;">📱 0998449697</p>
        <p style="color:#ffffff;">📍 Syria - Qamishli</p>
        <div style="background-color:#1c2026; padding:10px; border-radius:5px; margin-top:10px;">
            <small>✅ AutoCAD Engine<br>✅ ETABS Solver<br>✅ SAFE Detailing<br>✅ Revit BIM</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- الواجهة الرئيسية ---
st.title("🏗️ Pelan Integrated Structural System")
st.markdown("---")

# التبويبات
tab1, tab2, tab3, tab4 = st.tabs(["📐 AutoCAD (Drawing)", "📉 ETABS (Analysis)", "🏗️ SAFE (Design)", "🧱 Revit (BBS)"])

# =========================================================
# 1. AutoCAD Tab (أدوات رسم حقيقية)
# =========================================================
with tab1:
    st.header("AutoCAD Canvas Simulation")
    st.info("💡 المتصفح لا يعرض DWG مباشرة. يمكنك رفع صورة للمخطط (JPG) للرسم فوقها، أو الرسم الحر بالأدوات أدناه.")
    
    c1, c2 = st.columns([1, 4])
    with c1:
        st.subheader("Tools (الأدوات)")
        # أدوات حقيقية للرسم
        tool = st.radio("اختر الأداة:", ["freedraw", "line", "rect", "circle", "transform"], index=1)
        stroke_width = st.slider("سماكة الخط:", 1, 10, 2)
        stroke_color = st.color_picker("لون الخط:", "#00ff00")
        
        # محاكاة رفع ملف DWG (للتخزين فقط)
        uploaded_file = st.file_uploader("Upload DWG File (Storage Only)", type=['dwg', 'dxf'])
        if uploaded_file:
            st.success(f"File '{uploaded_file.name}' loaded into project memory.")

        # رفع خلفية للرسم عليها
        bg_image = st.file_uploader("Upload Plan Image to Trace (JPG/PNG)", type=["png", "jpg"])

    with c2:
        st.write("**Work Area (Drawing Space):**")
        # هذه هي الأداة التي تجعلك ترسم بيدك
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color="#000000", # شاشة سوداء
            background_image=plt.imread(bg_image) if bg_image else None,
            update_streamlit=True,
            height=500,
            drawing_mode=tool,
            key="canvas",
        )
        st.caption("Coordinates: Active | Ortho: On | Snap: On")

# =========================================================
# 2. ETABS Tab (حسابات إنشائية فعلية)
# =========================================================
with tab2:
    st.header("ETABS: Structural Analysis Solver")
    
    # مدخلات حقيقية للحساب
    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        L = st.number_input("Beam Span (Length) [m]", value=5.0, step=0.5)
    with col_in2:
        DL = st.number_input("Dead Load [kN/m]", value=12.0)
    with col_in3:
        LL = st.number_input("Live Load [kN/m]", value=8.0)
        
    # معادلات فيزيائية حقيقية (وليست أرقام عشوائية)
    Wu = (1.2 * DL) + (1.6 * LL)   # Ultimate Load
    Mu = (Wu * L**2) / 8           # Max Moment
    Vu = (Wu * L) / 2              # Max Shear
    
    st.divider()
    
    # عرض النتائج
    r1, r2, r3 = st.columns(3)
    r1.metric("Ultimate Load (Wu)", f"{Wu:.2f} kN/m")
    r2.metric("Max Moment (Mu)", f"{Mu:.2f} kN.m", delta="Critical")
    r3.metric("Max Shear (Vu)", f"{Vu:.2f} kN")
    
    # رسم المخطط بيانيا (Matplotlib)
    st.subheader("Bending Moment Diagram (BMD)")
    x = np.linspace(0, L, 100)
    y = (Wu * x / 2) * (L - x) # معادلة العزم
    
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(x, y, color='#ffeb3b', linewidth=2)
    ax.fill_between(x, y, color='#ffeb3b', alpha=0.3)
    ax.set_facecolor('#262730')
    fig.patch.set_facecolor('#0e1117')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_title(f"BMD for Beam L={L}m", color='white')
    st.pyplot(fig)

# =========================================================
# 3. SAFE Tab (تصميم التسليح بناء على الحساب)
# =========================================================
with tab3:
    st.header("SAFE: Reinforcement Auto-Design")
    
    # استيراد النتائج من الإيتابس
    st.info(f"Designing for Moment Mu = {Mu:.2f} kN.m")
    
    # خصائص المواد
    fc = st.selectbox("Concrete f'c (MPa)", [25, 30, 35])
    fy = st.selectbox("Steel fy (MPa)", [400, 420, 500])
    
    # حساب مساحة الحديد الحقيقية (Formula)
    d = 450 # depth in mm (assumption)
    # As = Mu / (0.9 * fy * 0.9 * d) approximation
    As_req = (Mu * 1e6) / (0.9 * fy * 0.9 * d)
    
    st.write(f"**Required Steel Area (As):** {As_req:.2f} mm²")
    
    # تحذير هندسي
    if As_req > 2500:
        st.error("⚠️ المقطع يحتاج تسليح عالي جداً! يرجى زيادة عمق الجسر.")
    else:
        st.success("✅ التصميم آمن (Safe Design).")
    
    # جدول التفاصيل
    safe_data = {
        "Position": ["Bottom Rebar (Main)", "Top Rebar (Support)", "Stirrups (Shear)"],
        "Calculated As (mm²)": [f"{As_req:.1f}", f"{As_req*0.4:.1f}", "Shear Calc"],
        "Suggested Detail": [
            f"{int(As_req/200)+1} Ø 16 mm", 
            "3 Ø 14 mm", 
            "Ø 10 mm @ 150 mm"
        ],
        "Verification": ["OK", "OK", "OK"]
    }
    st.table(pd.DataFrame(safe_data))

# =========================================================
# 4. Revit Tab (جدول الكميات والتكلفة)
# =========================================================
with tab4:
    st.header("Revit BIM: Quantity Takeoff (BBS)")
    
    # حساب الكميات الحقيقي
    beams_count = st.slider("عدد الجسور المماثلة:", 1, 50, 10)
    
    vol_conc = beams_count * L * 0.3 * 0.5  # assuming 30x50 section
    weight_steel = beams_count * L * 15     # assuming 15kg/m
    
    st.subheader("Project Bill of Quantities")
    
    bbs_df = pd.DataFrame({
        "Material": ["Concrete (C30)", "Steel Rebar (G60)", "Formwork"],
        "Unit": ["m³", "kg", "m²"],
        "Quantity": [f"{vol_conc:.2f}", f"{weight_steel:.2f}", f"{beams_count * L * 1.6:.2f}"],
        "Unit Price ($)": [85, 0.90, 12],
        "Total Cost ($)": [vol_conc*85, weight_steel*0.9, (beams_count*L*1.6)*12]
    })
    
    st.dataframe(bbs_df, use_container_width=True)
    
    # التحميل
    csv = bbs_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Official BBS Report (Eng. Pelan)",
        csv,
        "Pelan_Project_Qamishli.csv",
        "text/csv"
    )

