import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

# --- إعدادات الصفحة والطباعة ---
st.set_page_config(page_title="المصمم الإنشائي - نظام الأقطار", layout="wide")

st.markdown("""
    <style>
    @media print { .stButton, .sidebar, header, .stSelectbox, .stNumberInput, .stRadio { display: none !important; } 
    .main { width: 100% !important; } }
    </style>
""", unsafe_allow_html=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.title("🏗️ التصميم باختيار القطر")
    choice = st.radio("اختر العنصر الإنشائي:", 
                     ["البلاطة الهوردي", "الجوائز (Beams)", "الأعمدة (Columns)", "الأساسات المنفردة"])
    st.divider()
    fcu = st.number_input("إجهاد الخرسانة fcu (MPa)", value=25)
    fy = st.number_input("إجهاد الحديد fy (MPa)", value=400)
    st.divider()
    st.button("🖨️ طباعة التقرير (Ctrl+P)")

# ---------------------------------------------------------
# 1. البلاطة الهوردي (Ribbed Slab)
# ---------------------------------------------------------
if choice == "البلاطة الهوردي":
    st.header("🧱 تفاصيل البلاطة الهوردي")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📝 مدخلات العصب")
        b_rib = st.number_input("عرض العصب b (cm)", value=12)
        h_all = st.number_input("السماكة الكلية (cm)", value=30)
        # اختيار القطر بدلاً من العدد
        rib_bar_phi = st.selectbox("اختر قطر سيخ العصب (mm)", [12, 14, 16, 18], index=1)
        spacing = b_rib + 40 # عرض البلوك الافتراضي 40
        
    with col2:
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.add_patch(patches.Rectangle((0, 0), 3*spacing, h_all, color='#f0f0f0', ec='black', lw=2))
        for i in range(3):
            x_s = i * spacing + b_rib
            ax.add_patch(patches.Rectangle((x_s, 0), 40, 24, color='white', ec='black', hatch='///'))
            # رسم سيخين (العدد المعتاد للعصب) بالقطر المختار
            ax.add_patch(patches.Circle((i*spacing + b_rib/2, 5), rib_bar_phi/10, color='red'))
            ax.add_patch(patches.Circle((i*spacing + b_rib/2, 10), rib_bar_phi/10, color='red'))
        ax.axis('off'); st.pyplot(fig)

    st.subheader("📊 جدول الكميات وتفاصيل العصب")
    st.table({
        "البيان": ["قطر حديد العصب", "عدد الأسياخ/عصب", "تباعد المحاور", "حديد البلاطة (T.S)"],
        "القيمة": [f"T {rib_bar_phi}", "2 أسياخ", f"{spacing} cm", "T8 @ 20cm"]
    })

# ---------------------------------------------------------
# 2. الجوائز (Beams) - حساب العدد من القطر
# ---------------------------------------------------------
elif choice == "الجوائز (Beams)":
    st.header("🔗 تصميم الجائز (حساب العدد بناءً على القطر)")
    col1, col2 = st.columns([1, 2])
    with col1:
        mu = st.number_input("العزم التصميمي Mu (t.m)", value=15.0)
        b_b = st.number_input("العرض b (cm)", value=25)
        h_b = st.number_input("الارتفاع h (cm)", value=60)
        phi_main = st.selectbox("اختر قطر الحديد الرئيسي (mm)", [14, 16, 18, 20, 25], index=1)
        
    with col2:
        # حساب المساحة المطلوبة والعدد
        as_req = (mu * 10**5) / (0.87 * fy * (h_b - 5))
        bar_area = (math.pi * (phi_main**2)) / 400 # cm2
        n_bars = math.ceil(as_req / bar_area)
        if n_bars < 2: n_bars = 2
        
        
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot([0, 5], [0, 0], color='lightgrey', lw=40, alpha=0.4)
        ax.plot([0.1, 4.9], [-0.15, -0.15], 'red', lw=3)
        ax.axis('off'); st.pyplot(fig)
        
        st.success(f"العدد المطلوب للقطر T{phi_main} هو: {n_bars} أسياخ")

    st.subheader("📊 جدول تفريد حديد الجائز (BBS)")
    st.table({
        "المنطقة": ["الحديد السفلي", "الحديد العلوي", "الكانات"],
        "التفصيل المختار": [f"{n_bars} T {phi_main}", "2 T 12", "T 8 @ 15cm"],
        "مساحة الحديد (cm²)": [f"{n_bars * bar_area:.2f}", "2.26", "-"]
    })

# ---------------------------------------------------------
# 3. الأعمدة (Columns)
# ---------------------------------------------------------
elif choice == "الأعمدة (Columns)":
    st.header("🏢 تصميم مقطع العمود")
    col1, col2 = st.columns([1, 2])
    with col1:
        c_w = st.number_input("العرض b (cm)", value=30)
        c_h = st.number_input("الارتفاع h (cm)", value=60)
        phi_col = st.selectbox("قطر سيخ العمود (mm)", [14, 16, 18, 20, 25], index=1)
        # حساب عدد الأسياخ التقريبي لنسبة 1% خرسانة
        as_min = 0.01 * c_w * c_h
        n_col = math.ceil(as_min / ((math.pi * phi_col**2)/400))
        if n_col % 2 != 0: n_col += 1 # تقريب لعدد زوجي
        
    with col2:
        
        fig, ax = plt.subplots(figsize=(4, 5))
        ax.add_patch(patches.Rectangle((0, 0), c_w, c_h, color='#f9f9f9', ec='black', lw=3))
        for i in [4, c_w-4]:
            for j in np.linspace(4, c_h-4, int(n_col/2)):
                ax.add_patch(patches.Circle((i, j), phi_col/10, color='red'))
        ax.axis('off'); st.pyplot(fig)

    st.table({"المقطع": [f"{c_w}x{c_h} cm"], "القطر المختار": [f"T{phi_col}"], "العدد المحسوب": [f"{n_col} أسياخ"]})

# ---------------------------------------------------------
# 4. الأساسات المنفردة
# ---------------------------------------------------------
elif choice == "الأساسات المنفردة":
    st.header("📐 تسليح الأساسات (قطر محدد)")
    col1, col2 = st.columns([1, 2])
    with col1:
        P_f = st.number_input("حمل العمود (Ton)", value=120.0)
        phi_foot = st.selectbox("قطر حديد القاعدة (mm)", [12, 14, 16, 18], index=1)
    
    with col2:
        dim = math.sqrt((P_f*1.1)/(2.0*10))
        
        fig, ax = plt.subplots(); ax.add_patch(patches.Rectangle((0, 0), dim, dim, color='grey', alpha=0.2, ec='black'))
        for x in np.linspace(0.1, dim-0.1, 10):
            ax.plot([x, x], [0, dim], 'red', lw=1.2)
            ax.plot([0, dim], [x, x], 'red', lw=1.2)
        ax.set_aspect('equal'); ax.axis('off'); st.pyplot(fig)
        
    st.table({"الأبعاد": [f"{dim:.2f} m"], "القطر المختار": [f"T{phi_foot}"], "التوزيع": [f"T{phi_foot} @ 15cm"]})
