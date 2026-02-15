import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المصمم الإنشائي الاحترافي", layout="wide")

# --- دالة الطباعة المتوافقة ---
def add_print_button():
    st.markdown("""
        <style>
        @media print {
            .stButton, .stSelectbox, .stNumberInput, .sidebar, .stRadio, .stTabs { display: none !important; }
            .main { width: 100% !important; }
        }
        </style>
        <button onclick="window.print()" style="
            background-color: #d32f2f; color: white; padding: 12px 24px;
            border: none; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%;">
            🖨️ طباعة المخطط والنتائج
        </button>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("⚙️ المعطيات العامة")
    fcu = st.number_input("إجهاد البيتون fcu (MPa)", value=25)
    fy = st.number_input("إجهاد الحديد fy (MPa)", value=400)
    st.divider()
    add_print_button()

menu = ["البلاطات (Slabs)", "الجوائز (Beams)", "الأساسات (Footings)", "الأعمدة (Columns)"]
choice = st.selectbox("🎯 اختر العنصر:", menu)

# ---------------------------------------------------------
# 1. البلاطات (Slabs) - تركيز خاص على الهوردي
# ---------------------------------------------------------
if choice == "البلاطات (Slabs)":
    st.header("🧱 تصميم وتفاصيل البلاطات")
    s_type = st.radio("نوع البلاطة", ["هوردي (Ribbed Slab)", "مصمتة (Solid Slab)"])
    
    if s_type == "هوردي (Ribbed Slab)":
        col1, col2, col3 = st.columns(3)
        with col1:
            b_rib = st.number_input("عرض العصب b (cm)", value=12)
            h_slab = st.number_input("السماكة الكلية h (cm)", value=30)
        with col2:
            b_block = st.number_input("عرض البلوك (cm)", value=40)
            h_block = st.number_input("ارتفاع البلوك (cm)", value=24)
        with col3:
            rib_bar = st.selectbox("حديد العصب", [12, 14, 16], index=1)
            ts_bar = st.number_input("تباعد حديد البلاطة (cm)", value=20)

        if st.button("رسم المقطع العرضي للهوردي"):
            spacing = b_rib + b_block # تباعد الأعصاب من المركز للمركز
            
            # رسم المقطع العرضي للهوردي
            fig, ax = plt.subplots(figsize=(10, 4))
            # رسم البلوكات
            for i in range(3):
                x_start = i * spacing + b_rib
                ax.add_patch(patches.Rectangle((x_start, 0), b_block, h_block, color='#eeeeee', ec='black', hatch='/'))
                ax.text(x_start + b_block/2, h_block/2, f"Block\n{b_block}x{h_block}", ha='center', va='center', fontsize=8)
            
            # رسم الأعصاب والخرسانة
            ax.add_patch(patches.Rectangle((0, 0), 3*spacing, h_slab, color='lightgrey', alpha=0.3, ec='black', lw=2))
            
            # تظليل الأعصاب
            for i in range(4):
                ax.add_patch(patches.Rectangle((i*spacing, 0), b_rib, h_slab, color='grey', alpha=0.2))
                # رسم الحديد داخل العصب
                ax.add_patch(patches.Circle((i*spacing + b_rib/2, 5), 1.5, color='red'))
                ax.add_patch(patches.Circle((i*spacing + b_rib/2, 8), 1.5, color='red'))

            # أبعاد وتوضيحات
            ax.annotate('', xy=(0, -5), xytext=(spacing, -5), arrowprops=dict(arrowstyle='<->'))
            ax.text(spacing/2, -10, f"Rib Spacing: {spacing} cm", ha='center')
            
            ax.set_xlim(-10, 3*spacing + 10); ax.set_ylim(-15, h_slab + 10); ax.axis('off')
            st.pyplot(fig)

            st.table({
                "العنصر": ["تباعد الأعصاب (c/c)", "تسليح العصب الواحد", "تسليح بلاطة التغطية", "وزن المتر المربع التقديري"],
                "القيمة": [f"{spacing} cm", f"2 T{rib_bar}", f"T8 @ {ts_bar} cm", "380 - 450 kg/m2"]
            })

    else: # المصمتة
        Lx = st.number_input("الطول Lx (m)", value=4.0)
        Ly = st.number_input("العرض Ly (m)", value=5.0)
        if st.button("عرض تفاصيل البلاطة المصمتة"):
            st.table({"التسليح": ["فرش T12 @ 15cm", "غطاء T10 @ 15cm"], "السماكة": ["15 cm"]})

# ---------------------------------------------------------
# 2. الأساسات (Footings) - شامل
# ---------------------------------------------------------
elif choice == "الأساسات (Footings)":
    st.header("📐 تصميم الأساسات")
    f_mode = st.radio("النوع", ["منفرد Isolated", "مشترك Combined", "جار Strap"])
    
    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input("الحمل (Ton)", value=120.0)
        q = st.number_input("تحمل التربة (kg/cm2)", value=2.0)
    with col2:
        f_h = st.number_input("سمك القاعدة (cm)", value=60)
        f_bar = st.selectbox("القطر", [14, 16, 18])

    if st.button("عرض المخطط"):
        area = (P * 1.1) / (q * 10)
        L = math.sqrt(area)
        
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.add_patch(patches.Rectangle((0, 0), L, L, color='lightgrey', ec='black'))
        # رسم شبكة التسليح
        for i in np.linspace(0.2, L-0.2, 8):
            ax.plot([i, i], [0.1, L-0.1], 'red', lw=1)
            ax.plot([0.1, L-0.1], [i, i], 'red', lw=1)
        ax.axis('off'); st.pyplot(fig)
        st.success(f"الأبعاد: {L:.2f} x {L:.2f} m | الحديد: T{f_bar} @ 15cm")

# ---------------------------------------------------------
# 3. الجوائز والأعمدة (تكملة)
# ---------------------------------------------------------
else:
    st.info("أدخل المعطيات واضغط على الزر لعرض التفاصيل الإنشائية.")
    if st.button("عرض التفاصيل"):
        st.write("سيتم عرض الجداول والرسومات هنا بناءً على المدخلات.")
