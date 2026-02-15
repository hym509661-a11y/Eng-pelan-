import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المصمم الإنشائي - تحديث فوري", layout="wide")

# --- دالة الطباعة ---
def add_print_button():
    st.markdown("""
        <style>
        @media print { .stButton, .stSelectbox, .stNumberInput, .sidebar, header { display: none !important; } }
        </style>
        <button onclick="window.print()" style="background-color: #007bff; color: white; padding: 10px; border-radius: 5px; width: 100%; border: none; cursor: pointer;">
            🖨️ طباعة النتائج / حفظ PDF
        </button>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("📋 اختيار العنصر")
    choice = st.radio("العنصر المراد تصميمه:", ["البلاطات (Slabs)", "الجوائز (Beams)", "الأساسات (Footings)"])
    st.divider()
    st.header("⚖️ أحمال عامة")
    dl = st.number_input("الحمل الميت (kg/m2)", value=250)
    ll = st.number_input("الحمل الحي (kg/m2)", value=200)
    st.divider()
    add_print_button()

# ---------------------------------------------------------
# 1. تصميم البلاطات الهوردي (Ribbed Slab)
# ---------------------------------------------------------
if choice == "البلاطات (Slabs)":
    st.header("🧱 تصميم وتفاصيل البلاطة الهوردي")
    
    # تقسيم الشاشة: معطيات على اليمين ورسم على اليسار
    col_in, col_res = st.columns([1, 2])
    
    with col_in:
        st.subheader("📝 المعطيات")
        b_rib = st.number_input("عرض العصب b (cm)", value=12, step=1)
        b_block = st.number_input("عرض البلوك (cm)", value=40, step=1)
        h_total = st.number_input("السماكة الكلية h (cm)", value=30, step=1)
        h_block = st.number_input("ارتفاع البلوك (cm)", value=24, step=1)
        rib_bar = st.selectbox("قطر حديد العصب", [12, 14, 16], index=1)
        
    with col_res:
        # حسابات فورية
        spacing = b_rib + b_block
        wu = (1.4 * (dl + (h_total/100 * 2500)) + 1.6 * ll) / 1000 # t/m2
        wu_rib = wu * (spacing / 100) # t/m'
        
        st.subheader("📐 المقطع العرضي وتوزيع الأعصاب")
        
        fig, ax = plt.subplots(figsize=(10, 4))
        # رسم الخرسانة والبلوكات
        ax.add_patch(patches.Rectangle((0, 0), 3*spacing, h_total, color='#f5f5f5', ec='black', lw=2))
        for i in range(3):
            x_s = i * spacing + b_rib
            ax.add_patch(patches.Rectangle((x_s, 0), b_block, h_block, color='white', ec='black', hatch='///'))
            ax.add_patch(patches.Circle((i*spacing + b_rib/2, 5), 1.2, color='red')) # حديد سفلي
        
        # خط البعد (تباعد المحاور)
        ax.annotate('', xy=(b_rib/2, h_total+3), xytext=(spacing+b_rib/2, h_total+3), arrowprops=dict(arrowstyle='<->'))
        ax.text(spacing/2 + b_rib/2, h_total+5, f"S = {spacing} cm", ha='center', fontweight='bold')
        
        ax.set_xlim(-5, 3*spacing+5); ax.set_ylim(-10, h_total+15); ax.axis('off')
        st.pyplot(fig)

        # جداول النتائج
        st.table({
            "المعلمة": ["حمل العصب (wu)", "تباعد المحاور (c/c)", "حجم الخرسانة / 100m²", "عدد البلوك / 100m²"],
            "القيمة": [f"{wu_rib:.2f} t/m", f"{spacing} cm", f"{(100*h_total/100 - (100/(spacing/100*0.2) * b_block/100*h_block/100*0.2)):.2f} m³", f"{int(100/(spacing/100*0.2))} بلوكة"]
        })

# ---------------------------------------------------------
# 2. تصميم الأساسات (Footings)
# ---------------------------------------------------------
elif choice == "الأساسات (Footings)":
    st.header("📐 تصميم الأساسات المنفردة")
    c_in, c_res = st.columns([1, 2])
    
    with c_in:
        P = st.number_input("حمل العمود (Ton)", value=120.0)
        q = st.number_input("تحمل التربة (kg/cm2)", value=2.0)
        f_bar = st.selectbox("قطر الحديد", [14, 16, 18], index=1)
        
    with c_res:
        area = (P * 1.1) / (q * 10)
        side = math.sqrt(area)
        
        st.subheader("🖼️ المسقط الأفقي للقاعدة")
        
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.add_patch(patches.Rectangle((0, 0), side, side, color='#eeeeee', ec='black', lw=2))
        for i in np.linspace(0.15, side-0.15, 10):
            ax2.plot([i, i], [0.1, side-0.1], 'red', lw=1.5, alpha=0.6)
            ax2.plot([0.1, side-0.1], [i, i], 'red', lw=1.5, alpha=0.6)
        ax2.set_title(f"Plan: {side:.2f} x {side:.2f} m")
        ax2.axis('off'); st.pyplot(fig2)
        
        st.success(f"الأبعاد المطلوبة: {side:.2f} m | الحديد: T{f_bar} @ 15cm")

# ---------------------------------------------------------
# 3. الجوائز (Beams)
# ---------------------------------------------------------
elif choice == "الجوائز (Beams)":
    st.header("🔗 تصميم الجوائز")
    
    st.info("قم بتعديل المعطيات في القائمة الجانبية والأقسام لتحديث الرسوم.")
