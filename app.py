import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المصمم الإنشائي الشامل v6.0", layout="wide")

# --- دالة الطباعة المتوافقة ---
def add_print_button():
    st.markdown("""
        <style>
        @media print {
            .stButton, .stSelectbox, .stNumberInput, .sidebar, .stRadio, .stTabs, .stHeader { display: none !important; }
            .main { width: 100% !important; }
            .block-container { padding: 0 !important; }
        }
        </style>
        <button onclick="window.print()" style="
            background-color: #1a237e; color: white; padding: 12px 24px;
            border: none; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%;">
            🖨️ طباعة التقرير الفني (Print / Save PDF)
        </button>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("🏗️ ثوابت المشروع")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)
    st.divider()
    add_print_button()

menu = ["البلاطات (Slabs)", "الجوائز (Beams)", "الأساسات (Footings)", "الأعمدة (Columns)"]
choice = st.selectbox("🎯 اختر العنصر المطلوب:", menu)

# ---------------------------------------------------------
# 1. قسم البلاطات (الهوردي والمصمتة)
# ---------------------------------------------------------
if choice == "البلاطات (Slabs)":
    st.header("🧱 تصميم البلاطات وتفاصيل الهوردي")
    s_type = st.radio("نوع البلاطة", ["بلاطة هوردي (Ribbed Slab)", "بلاطة مصمتة (Solid Slab)"])
    
    if s_type == "بلاطة هوردي (Ribbed Slab)":
        col1, col2, col3 = st.columns(3)
        with col1:
            b_rib = st.number_input("عرض العصب b (cm)", value=12)
            h_total = st.number_input("السماكة الكلية h (cm)", value=30)
        with col2:
            b_block = st.number_input("عرض البلوك (cm)", value=40)
            h_block = st.number_input("ارتفاع البلوك (cm)", value=24)
        with col3:
            rib_bar = st.selectbox("تسليح العصب", [12, 14, 16], index=1)
            ts_thick = st.number_input("سمك بلاطة التغطية (cm)", value=6)

        if st.button("رسم وتفصيل الهوردي"):
            spacing = b_rib + b_block # التباعد c/c
            
            
            # رسم المقطع العرضي للهوردي
            fig, ax = plt.subplots(figsize=(12, 5))
            # رسم الخرسانة الشاملة
            ax.add_patch(patches.Rectangle((0, 0), 3*spacing, h_total, color='lightgrey', alpha=0.2, ec='black', lw=2))
            
            # رسم البلوكات والأعصاب
            for i in range(3):
                x_start = i * spacing + b_rib
                # البلوك
                ax.add_patch(patches.Rectangle((x_start, 0), b_block, h_block, color='white', ec='black', hatch='...'))
                ax.text(x_start + b_block/2, h_block/2, f"Block\n{b_block}x{h_block}", ha='center', fontsize=9)
                # الحديد داخل الأعصاب
                ax.add_patch(patches.Circle((i*spacing + b_rib/2, 5), 1.2, color='red'))
                ax.add_patch(patches.Circle((i*spacing + b_rib/2, 10), 1.2, color='red'))
            
            # أبعاد توضيحية
            ax.annotate('', xy=(0, -5), xytext=(spacing, -5), arrowprops=dict(arrowstyle='<->'))
            ax.text(spacing/2, -12, f"Rib Spacing: {spacing} cm", ha='center', fontweight='bold')
            
            ax.set_xlim(-10, 3*spacing + 10); ax.set_ylim(-20, h_total + 10); ax.axis('off')
            st.pyplot(fig)

            # --- حساب الكميات لكل 100 متر مربع ---
            area_m2 = 100
            num_blocks = (area_m2 / ((spacing/100) * 0.2)) # بفرض طول البلوكة 20سم
            conc_vol = (area_m2 * (h_total/100)) - (num_blocks * (b_block/100 * h_block/100 * 0.2))

            st.subheader("📊 كميات المواد التقديرية (لكل 100 متر مربع)")
            c_q1, c_q2 = st.columns(2)
            c_q1.metric("عدد البلوك (تقريباً)", f"{int(num_blocks)} بلوكة")
            c_q2.metric("حجم الخرسانة", f"{conc_vol:.2f} m³")

            st.table({
                "العنصر": ["عرض العصب الفعلي", "تباعد الأعصاب", "تسليح العصب", "بلاطة التغطية"],
                "التفاصيل": [f"{b_rib} cm", f"{spacing} cm", f"2 T{rib_bar}", f"{ts_thick} cm (T8@20cm)"]
            })

    else:
        st.subheader("📊 تفاصيل البلاطة المصمتة")
        Lx = st.number_input("Lx (m)", value=4.0)
        Ly = st.number_input("Ly (m)", value=5.0)
        
        if st.button("تحديث الحسابات"):
            st.table({"الاتجاه": ["الفرش (Lx)", "الغطاء (Ly)"], "التسليح": ["T12 @ 15cm", "T10 @ 15cm"]})

# ---------------------------------------------------------
# 2. قسم الأساسات (منفرد، مشترك، جار)
# ---------------------------------------------------------
elif choice == "الأساسات (Footings)":
    st.header("📐 تصميم الأساسات بمختلف أنواعها")
    f_type = st.radio("نوع القاعدة", ["منفردة Isolated", "مشتركة Combined", "أساس جار Strap"])
    
    col1, col2 = st.columns(2)
    with col1:
        P_load = st.number_input("الحمل الكلي (Ton)", value=120.0)
        q_allow = st.number_input("إجهاد التربة (kg/cm2)", value=2.0)
    with col2:
        f_bar = st.selectbox("قطر الحديد", [14, 16, 18], index=1)
        f_thick = st.number_input("سماكة القاعدة (cm)", value=60)

    if st.button("رسم المخطط الإنشائي"):
        area = (P_load * 1.1) / (q_allow * 10)
        side = math.sqrt(area)
        
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.add_patch(patches.Rectangle((0, 0), side, side, color='lightgrey', ec='black', lw=2))
        # رسم شبكة التسليح
        for i in np.linspace(0.2, side-0.2, 10):
            ax.plot([i, i], [0.1, side-0.1], 'red', lw=1.5, alpha=0.7)
            ax.plot([0.1, side-0.1], [i, i], 'red', lw=1.5, alpha=0.7)
        ax.set_title(f"Footing: {side:.2f} x {side:.2f} m", pad=20)
        ax.axis('off'); st.pyplot(fig)
        
        
        
        st.table({
            "المعلمة": ["الأبعاد النهائية", "التسليح", "السماكة h", "الوزن التقديري"],
            "القيمة": [f"{side:.2f} x {side:.2f} m", f"T{f_bar} @ 15cm", f"{f_thick} cm", f"{area*f_thick*0.025:.2f} Ton"]
        })

# ---------------------------------------------------------
# 3. قسم الجوائز والأعمدة
# ---------------------------------------------------------
else:
    st.header(f"🏗️ تصميم {choice}")
    st.info("أدخل المعطيات لعرض المخططات التنفيذية وجدول تفريد الحديد (BBS).")
    if choice == "الجوائز (Beams)":
        
        st.write("استخدم قسم الجوائز لحساب العزم والقص وتوزيع الكانات.")
    else:
        
        st.write("تفاصيل تسليح الأعمدة والكانات تظهر هنا.")
