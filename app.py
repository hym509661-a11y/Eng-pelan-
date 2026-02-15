import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المصمم الإنشائي المتكامل v7.0", layout="wide")

# --- دالة الطباعة الاحترافية ---
def add_print_button():
    st.markdown("""
        <style>
        @media print {
            .stButton, .stSelectbox, .stNumberInput, .sidebar, .stRadio, .stTabs { display: none !important; }
            .main { width: 100% !important; }
        }
        </style>
        <button onclick="window.print()" style="
            background-color: #004d40; color: white; padding: 12px 24px;
            border: none; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%;">
            🖨️ طباعة المخطط الهندسي والتقرير
        </button>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية: حساب الأحمال (Load Engine) ---
with st.sidebar:
    st.header("⚖️ محرك حساب الأحمال")
    dead_load = st.number_input("الحمولة الميتة DL (kg/m2)", value=250)
    live_load = st.number_input("الحمولة الحية LL (kg/m2)", value=200)
    gamma_c = 2500 # كثافة الخرسانة kg/m3
    st.divider()
    st.header("⚙️ معطيات المواد")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)
    st.divider()
    add_print_button()

menu = ["البلاطات (Slabs)", "الجوائز (Beams)", "الأساسات (Footings)", "الأعمدة (Columns)"]
choice = st.selectbox("🎯 اختر العنصر المراد تصميمه:", menu)

# ---------------------------------------------------------
# 1. قسم البلاطات (الهوردي والمصمتة)
# ---------------------------------------------------------
if choice == "البلاطات (Slabs)":
    st.header("🧱 تفاصيل البلاطات الهوردي (Ribbed Slab Design)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        b_rib = st.number_input("عرض العصب b (cm)", value=12)
        h_total = st.number_input("السماكة الكلية h (cm)", value=30)
    with col2:
        b_block = st.number_input("عرض البلوك (cm)", value=40)
        h_block = st.number_input("ارتفاع البلوك (cm)", value=24)
    with col3:
        rib_bar = st.selectbox("قطر حديد العصب", [12, 14, 16], index=1)
        L_span = st.number_input("طول مجاز العصب (m)", value=5.0)

    if st.button("تحديث الرسم وحساب الكميات"):
        # حساب الأحمال التصميمية للعصب
        spacing = (b_rib + b_block) / 100 # m (من المركز للمركز)
        wu_slab = 1.4 * (dead_load + (h_total/100 * gamma_c)) + 1.6 * live_load
        wu_rib = wu_slab * spacing / 1000 # t/m
        
        # رسم المقطع العرضي للهوردي
        st.subheader("📐 المقطع العرضي وتفاصيل البلوك")
        fig, ax = plt.subplots(figsize=(12, 4))
        # رسم الخرسانة
        ax.add_patch(patches.Rectangle((0, 0), 3*(b_rib+b_block), h_total, color='#f0f0f0', ec='black', lw=2))
        
        # رسم البلوكات والأعصاب
        for i in range(3):
            x_start = i * (b_rib + b_block) + b_rib
            ax.add_patch(patches.Rectangle((x_start, 0), b_block, h_block, color='white', ec='black', hatch='\\\\'))
            ax.text(x_start + b_block/2, h_block/2, f"Block\n{b_block}x{h_block}", ha='center', fontsize=8)
            # حديد التسليح
            ax.add_patch(patches.Circle((i*(b_rib+b_block) + b_rib/2, 5), 1.2, color='red'))
            ax.add_patch(patches.Circle((i*(b_rib+b_block) + b_rib/2, 10), 1.2, color='red'))

        # توضيح تباعد المحاور
        ax.annotate('', xy=(b_rib/2, h_total+5), xytext=((b_rib+b_block)+b_rib/2, h_total+5), arrowprops=dict(arrowstyle='<->'))
        ax.text((b_rib+b_block)/2 + b_rib/2, h_total+7, f"S = {b_rib+b_block} cm", ha='center', fontweight='bold')
        
        ax.set_xlim(-5, 3*(b_rib+b_block)+5); ax.set_ylim(-10, h_total+15); ax.axis('off')
        st.pyplot(fig)
        
        

        # جداول الكميات والنتائج
        st.subheader("📊 نتائج التحليل وحصر الكميات")
        q1, q2, q3 = st.columns(3)
        q1.metric("حمل العصب التصميمي", f"{wu_rib:.2f} t/m")
        
        area_100 = 100
        n_blocks = (area_100 / (spacing * 0.2)) # طول البلوكة 20سم
        conc_vol = (area_100 * h_total/100) - (n_blocks * (b_block/100 * h_block/100 * 0.2))
        
        q2.metric("عدد البلوك / 100m²", f"{int(n_blocks)} Pcs")
        q3.metric("حجم الخرسانة / 100m²", f"{conc_vol:.2f} m³")

        st.table({
            "المعلمة": ["تباعد المحاور c/c", "تسليح العصب المقترح", "العزم الأقصى للعصب", "تسليح البلاطة العلوية"],
            "القيمة": [f"{b_rib + b_block} cm", f"2 T{rib_bar}", f"{(wu_rib * L_span**2 / 8):.2f} t.m", "T8 @ 20cm"]
        })

# ---------------------------------------------------------
# 2. قسم الأساسات (Footings)
# ---------------------------------------------------------
elif choice == "الأساسات (Footings)":
    st.header("📐 تصميم الأساسات المنفردة والمشتركة")
    f_type = st.radio("نوع الأساس", ["منفرد Isolated", "مشترك Combined"])
    col1, col2 = st.columns(2)
    with col1:
        P_col = st.number_input("حمل العمود (Ton)", value=120.0)
        q_soil = st.number_input("تحمل التربة (kg/cm2)", value=2.0)
    with col2:
        f_bar = st.selectbox("قطر الحديد", [14, 16, 18], index=1)
        f_thick = st.number_input("سماكة القاعدة (cm)", value=60)

    if st.button("عرض المخطط الإنشائي"):
        area = (P_col * 1.1) / (q_soil * 10)
        side = math.sqrt(area)
        
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.add_patch(patches.Rectangle((0, 0), side, side, color='#e0e0e0', ec='black', lw=2))
        # شبكة التسليح
        for i in np.linspace(0.15, side-0.15, 10):
            ax.plot([i, i], [0.1, side-0.1], 'red', lw=1.5, alpha=0.6)
            ax.plot([0.1, side-0.1], [i, i], 'red', lw=1.5, alpha=0.6)
        ax.set_title(f"Plan View: {side:.2f} x {side:.2f} m", pad=20)
        ax.axis('off'); st.pyplot(fig)
        
        
        
        st.table({"المواصفات": ["الأبعاد", "التسليح", "حجم الخرسانة"], "النتائج": [f"{side:.2f} m", f"T{f_bar} @ 15cm", f"{area * f_thick/100:.2f} m³"]})

# ---------------------------------------------------------
# 3. الجوائز والأعمدة (تكملة بنفس الفلسفة)
# ---------------------------------------------------------
else:
    st.info("أدخل المعطيات في القائمة الجانبية لتحديث الأحمال، ثم اضغط على زر العرض.")
    if choice == "الجوائز (Beams)":
        
    else:
        
