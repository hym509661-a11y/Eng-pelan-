import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المصمم الإنشائي المتكامل v8.0", layout="wide")

# --- دالة الطباعة (تعديل لضمان العمل بنسبة 100%) ---
def add_print_button():
    st.markdown("""
        <style>
        @media print {
            .stButton, .stSelectbox, .stNumberInput, .sidebar, .stRadio, .stTabs, .stHeader, header, .stMarkdown button { 
                display: none !important; 
            }
            .main { width: 100% !important; }
            .block-container { padding: 1rem !important; }
        }
        </style>
        <button onclick="window.print()" style="
            background-color: #1565c0; color: white; padding: 14px 28px;
            border: none; border-radius: 10px; cursor: pointer; font-weight: bold; width: 100%; font-size: 18px;">
            🖨️ طباعة المخطط الهندسي والتقرير
        </button>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية: محرك الأحمال والمواد ---
with st.sidebar:
    st.header("⚖️ حساب الأحمال (Loading)")
    dead_load = st.number_input("الحمولة الميتة DL (kg/m2)", value=250)
    live_load = st.number_input("الحمولة الحية LL (kg/m2)", value=200)
    st.divider()
    st.header("⚙️ معطيات المواد")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)
    st.divider()
    add_print_button()

menu = ["البلاطات (Slabs)", "الجوائز (Beams)", "الأساسات (Footings)", "الأعمدة (Columns)"]
choice = st.selectbox("🎯 اختر العنصر المراد تصميمه:", menu)

# ---------------------------------------------------------
# 1. قسم البلاطات (تركيز على الهوردي والتفاصيل)
# ---------------------------------------------------------
if choice == "البلاطات (Slabs)":
    st.header("🧱 تفاصيل البلاطات الهوردي (Ribbed Slab)")
    
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

    if st.button("تحديث الرسم الهندسي وحصر الكميات"):
        # حسابات الأحمال
        spacing_m = (b_rib + b_block) / 100
        wu_slab = (1.4 * (dead_load + (h_total/100 * 2500)) + 1.6 * live_load) / 1000 # t/m2
        wu_rib = wu_slab * spacing_m # t/m'
        
        # الرسم الهندسي للمقطع
        st.subheader("📐 المقطع العرضي الإنشائي (Cross Section)")
        
        fig, ax = plt.subplots(figsize=(12, 4))
        # الخرسانة الأساسية
        ax.add_patch(patches.Rectangle((0, 0), 3*(b_rib+b_block), h_total, color='#eeeeee', ec='black', lw=2))
        
        for i in range(3):
            x_s = i * (b_rib + b_block) + b_rib
            # رسم البلوك
            ax.add_patch(patches.Rectangle((x_s, 0), b_block, h_block, color='white', ec='black', hatch='//'))
            ax.text(x_s + b_block/2, h_block/2, f"Block\n{b_block}x{h_block}", ha='center', fontsize=8)
            # رسم حديد التسليح
            ax.add_patch(patches.Circle((i*(b_rib+b_block) + b_rib/2, 5), 1.2, color='red'))
            ax.add_patch(patches.Circle((i*(b_rib+b_block) + b_rib/2, 10), 1.2, color='red'))

        # خطوط الأبعاد
        ax.annotate('', xy=(b_rib/2, h_total+4), xytext=((b_rib+b_block)+b_rib/2, h_total+4), arrowprops=dict(arrowstyle='<->'))
        ax.text((b_rib+b_block)/2 + b_rib/2, h_total+6, f"S = {b_rib+b_block} cm (c/c)", ha='center', fontweight='bold')
        
        ax.set_xlim(-5, 3*(b_rib+b_block)+5); ax.set_ylim(-15, h_total+15); ax.axis('off')
        st.pyplot(fig)

        # جدول الكميات والنتائج
        st.subheader("📊 حصر الكميات والنتائج (لكل 100 متر مربع)")
        area_100 = 100
        n_blocks = (area_100 / (spacing_m * 0.2)) # طول البلوك 20سم
        conc_vol = (area_100 * h_total/100) - (n_blocks * (b_block/100 * h_block/100 * 0.2))
        
        c1, c2, c3 = st.columns(3)
        c1.metric("عدد البلوك المطلوبة", f"{int(n_blocks)} بلوكة")
        c2.metric("حجم الخرسانة", f"{conc_vol:.2f} m³")
        c3.metric("حمل العصب التصميمي", f"{wu_rib:.2f} t/m")

        st.table({
            "المعلمة": ["تباعد المحاور (S)", "تسليح العصب", "عزم العصب (M_max)", "سمك بلاطة التغطية"],
            "القيمة": [f"{b_rib + b_block} cm", f"2 T{rib_bar}", f"{(wu_rib * L_span**2 / 8):.2f} t.m", f"{h_total - h_block} cm"]
        })

# ---------------------------------------------------------
# 2. قسم الأساسات (Footings)
# ---------------------------------------------------------
elif choice == "الأساسات (Footings)":
    st.header("📐 تصميم الأساسات المنفردة والمشتركة")
    
    f_type = st.radio("نوع الأساس", ["منفرد Isolated", "مشترك Combined"])
    col1, col2 = st.columns(2)
    with col1:
        P_val = st.number_input("حمل العمود (Ton)", value=120.0)
        q_soil = st.number_input("تحمل التربة (kg/cm2)", value=2.0)
    with col2:
        f_bar = st.selectbox("قطر الحديد", [14, 16, 18], index=1)
        f_thick = st.number_input("سماكة القاعدة (cm)", value=60)

    if st.button("عرض المخطط الإنشائي"):
        area = (P_val * 1.1) / (q_soil * 10)
        side = math.sqrt(area)
        
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.add_patch(patches.Rectangle((0, 0), side, side, color='#e0e0e0', ec='black', lw=2))
        # رسم شبكة الحديد
        for i in np.linspace(0.15, side-0.15, 10):
            ax.plot([i, i], [0.1, side-0.1], 'red', lw=1.5, alpha=0.6)
            ax.plot([0.1, side-0.1], [i, i], 'red', lw=1.5, alpha=0.6)
        ax.set_title(f"Plan View: {side:.2f} x {side:.2f} m", pad=20)
        ax.axis('off'); st.pyplot(fig)
        
        st.table({"المواصفات": ["الأبعاد", "التسليح", "الخرسانة"], "النتائج": [f"{side:.2f} m", f"T{f_bar} @ 15cm", f"{area * f_thick/100:.2f} m³"]})

# ---------------------------------------------------------
# 3. الجوائز والأعمدة (تكملة بنفس الفلسفة)
# ---------------------------------------------------------
else:
    st.info("أدخل المعطيات في القائمة الجانبية لتحديث الأحمال، ثم اضغط على زر العرض.")
    if choice == "الجوائز (Beams)":
        
        st.write("تفاصيل الجوائز تظهر هنا مع توزيع الكانات.")
    else:
        
        st.write("تفاصيل الأعمدة تظهر هنا مع جداول BBS.")

