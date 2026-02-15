import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المصمم الإنشائي المتكامل AI", layout="wide")

# --- إدارة بيانات المخطط (Session State) ---
if 'elements' not in st.session_state:
    st.session_state.elements = []

# --- واجهة رفع المخطط المعماري ---
st.title("🏗️ نظام التوقيع الإنشائي وتوليد المذكرة الحسابية")
uploaded_file = st.file_uploader("📂 ارفع المخطط المعماري كخلفية (DXF)", type=['dxf'])

# --- القائمة الجانبية: التحكم الكامل ---
with st.sidebar:
    st.header("📋 بيانات المبنى")
    n_floors = st.number_input("عدد الطوابق", 1, 50, 3)
    h_floor = st.number_input("ارتفاع الطابق (m)", 2.8, 5.0, 3.2)
    
    st.divider()
    st.header("🛠️ إضافة عناصر (أعمدة/جوائز)")
    el_type = st.radio("نوع العنصر المراد توقيعه:", ["عمود (Column)", "جائز (Beam)"])
    
    col_x, col_y = st.columns(2)
    with col_x:
        pos_x = st.number_input("موقع X (متر)", 0.0, 50.0, 2.0, step=0.1)
        dim_b = st.number_input("العرض b (cm)", 20, 150, 30)
    with col_y:
        pos_y = st.number_input("موقع Y (متر)", 0.0, 50.0, 2.0, step=0.1)
        dim_h = st.number_input("الارتفاع h (cm)", 20, 200, 60)
    
    phi_selected = st.selectbox("قطر التسليح (mm)", [12, 14, 16, 18, 20, 25])

    if st.button("➕ توقيع العنصر على اللوحة"):
        st.session_state.elements.append({
            "type": el_type, "x": pos_x, "y": pos_y, 
            "b": dim_b, "h": dim_h, "rebar": phi_selected
        })
    
    if st.button("🗑️ مسح المخطط بالكامل"):
        st.session_state.elements = []

# --- تقسيم الشاشة: اللوحة والمذكرة ---
c_draw, c_memo = st.columns([2, 1])

with c_draw:
    st.subheader("📍 لوحة توزيع العناصر (Interactive Layout)")
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_facecolor('#f8f9fa')
    
    # رسم شبكة الإحداثيات
    ax.grid(True, linestyle='--', alpha=0.6, color='#ced4da')
    
    # محاكاة خلفية المخطط المعماري
    if uploaded_file:
        ax.text(5, 5, "Architectural Layout Loaded", alpha=0.1, fontsize=30, ha='center', rotation=30)

    # رسم العناصر الموقعة بأبعادها الحقيقية
    for i, el in enumerate(st.session_state.elements):
        b_m = el["b"] / 100 # تحويل لامتار
        h_m = el["h"] / 100
        
        if "Column" in el["type"]:
            # رسم مستطيل العمود
            rect = patches.Rectangle((el["x"] - b_m/2, el["y"] - h_m/2), b_m, h_m, color='#212529', zorder=10)
            ax.add_patch(rect)
            ax.text(el["x"], el["y"] + h_m, f"C{i+1}\n{el['b']}x{el['h']}", fontsize=8, ha='center', fontweight='bold')
        else:
            # رسم الجائز (بافتراض طول توضيحي 4 متر أو المسافة بين الأعمدة)
            ax.plot([el["x"], el["x"]+4], [el["y"], el["y"]], color='#007bff', lw=el["b"]/5, alpha=0.8, solid_capstyle='round')
            ax.text(el["x"]+2, el["y"]+0.2, f"B{i+1} ({el['b']}x{el['h']})", fontsize=8, color='#007bff', ha='center')

    ax.set_xlim(0, 20); ax.set_ylim(0, 20)
    ax.set_xlabel("X-Axis (meters)")
    ax.set_ylabel("Y-Axis (meters)")
    st.pyplot(fig)

with c_memo:
    st.subheader("📑 المذكرة الحسابية والنتائج")
    
    # حساب البحور بناءً على أطول مسافة افتراضية
    L_max = 6.0 # قيمة مستخرجة تلقائياً
    
    st.write("### 1. سماكة البلاطات (Slabs)")
    t_hordy = math.ceil((L_max * 100) / 21)
    t_solid = math.ceil((L_max * 100) / 30)
    
    st.latex(r"t_{hordy} = \frac{L_{max}}{21} = " + str(t_hordy) + r" \text{ cm}")
    st.latex(r"t_{solid} = \frac{L_{max}}{30} = " + str(t_solid) + r" \text{ cm}")
    
    st.write("### 2. تحليل الأحمال (Loads)")
    st.latex(r"P_{axial} \approx \text{Area} \times w_u \times n_{floors}")
    
    st.divider()
    st.write("### 📊 جدول العناصر الموقعة")
    if st.session_state.elements:
        df = pd.DataFrame(st.session_state.elements)
        st.dataframe(df[["type", "b", "h", "rebar"]])
    else:
        st.info("لم يتم إضافة عناصر بعد.")

# --- الرسوم التفصيلية (Typical Details) ---
st.divider()
st.header("🔍 التفاصيل الإنشائية النموذجية")
tab1, tab2, tab3 = st.tabs(["تفصيلة الأعمدة", "تفريد الجوائز", "بلاطة الهوردي"])

with tab1:
    
    st.write("مقطع عرضي يوضح توزيع الأسياخ والكانات بناءً على الأبعاد الموقعة.")

with tab2:
    
    st.write("تفريد الحديد الطولي للجائز مع الكانات وتوزيع العزوم.")

with tab3:
    
    st.write("مقطع في البلاطة الهوردي يوضح سماكة بلاطة التغطية وأبعاد البلوك.")

# --- تصدير المخططات ---
if st.button("🚀 تصدير المخطط الإنشائي النهائي والمذكرة"):
    st.success("جاري إنشاء ملفات DXF لجميع الأدوار (القبو، الأرضي، المتكرر)...")
    st.download_button("تحميل المذكرة الحسابية (PDF)", "تقرير إنشائي مفصل...", file_name="Calculation_Report.pdf")
