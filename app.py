import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المصمم الإنشائي - النسخة المتكاملة", layout="wide")

# --- تنسيق الطباعة ---
st.markdown("""
    <style>
    @media print { .stButton, .sidebar, header, .stSelectbox, .stNumberInput, .stRadio { display: none !important; } }
    </style>
""", unsafe_allow_html=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.title("🏗️ المكتب الهندسي")
    choice = st.radio("اختر العنصر للتصميم:", 
                     ["البلاطة الهوردي", "البلاطة المصمتة", "الجوائز (Beams)", "الأعمدة (Columns)", "الأساسات"])
    st.divider()
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)
    st.divider()
    st.button("🖨️ طباعة التقرير (Ctrl+P)")

# ---------------------------------------------------------
# 1. البلاطة الهوردي (Ribbed Slab)
# ---------------------------------------------------------
if choice == "البلاطة الهوردي":
    st.header("🧱 تفاصيل البلاطة الهوردي")
    c1, c2 = st.columns([1, 2])
    with c1:
        b_rib = st.number_input("عرض العصب b (cm)", value=12)
        h_all = st.number_input("السماكة الكلية h (cm)", value=30)
        phi_rib = st.selectbox("قطر حديد العصب (mm)", [12, 14, 16], index=1)
    with c2:
        spacing = b_rib + 40
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.add_patch(patches.Rectangle((0, 0), 3*spacing, h_all, color='#f0f0f0', ec='black', lw=2))
        for i in range(3):
            x_s = i * spacing + b_rib
            ax.add_patch(patches.Rectangle((x_s, 0), 40, h_all-6, color='white', ec='black', hatch='///'))
            # التسليح السفلي (سيخان في قاع العصب)
            ax.add_patch(patches.Circle((i*spacing + b_rib/2 - 2, 4), phi_rib/12, color='red'))
            ax.add_patch(patches.Circle((i*spacing + b_rib/2 + 2, 4), phi_rib/12, color='red'))
        ax.axis('off'); st.pyplot(fig)
    st.table({"البيان": ["تسليح العصب السفلي", "تباعد المحاور c/c", "البلوك المستخدم"], "القيمة": [f"2 T{phi_rib}", f"{spacing} cm", f"40x{h_all-6}x20 cm"]})

# ---------------------------------------------------------
# 2. البلاطة المصمتة (Solid Slab) - مضافة الآن
# ---------------------------------------------------------
elif choice == "البلاطة المصمتة":
    st.header("💠 تفاصيل البلاطة المصمتة (Solid Slab)")
    c1, c2 = st.columns([1, 2])
    with c1:
        h_s = st.number_input("سماكة البلاطة (cm)", value=15)
        phi_s = st.selectbox("قطر حديد التسليح (mm)", [10, 12, 14], index=0)
        spacing_s = st.slider("التباعد بين الأسياخ (cm)", 10, 25, 15)
    with c2:
        fig, ax = plt.subplots(figsize=(8, 3))
        # رسم مقطع البلاطة
        ax.add_patch(patches.Rectangle((0, 0), 100, h_s, color='#e0e0e0', ec='black', lw=2))
        # رسم التسليح السفلي (نقاط)
        for x in np.linspace(10, 90, 7):
            ax.add_patch(patches.Circle((x, 3), phi_s/10, color='red'))
        # رسم التسليح الطولي السفلي
        ax.plot([5, 95], [2.5, 2.5], color='red', lw=2)
        ax.set_title("مقطع عرضي في البلاطة (Slab Section)")
        ax.set_xlim(-5, 105); ax.set_ylim(-5, h_s+10); ax.axis('off'); st.pyplot(fig)
    st.table({"البيان": ["التسليح السفلي (فرش)", "التسليح السفلي (غطاء)", "السماكة"], "القيمة": [f"T{phi_s} @ {spacing_s} cm", f"T10 @ {spacing_s} cm", f"{h_s} cm"]})

# ---------------------------------------------------------
# 3. الجوائز (Beams) - ضبط التسليح السفلي
# ---------------------------------------------------------
elif choice == "الجوائز (Beams)":
    st.header("🔗 تفاصيل تسليح الجائز (Beam Details)")
    c1, c2 = st.columns([1, 2])
    with c1:
        L_b = st.number_input("طول الجائز (m)", value=5.0)
        h_b = st.number_input("الارتفاع h (cm)", value=60)
        b_b = st.number_input("العرض b (cm)", value=25)
        phi_b = st.selectbox("قطر الحديد السفلي (mm)", [14, 16, 18, 20], index=1)
        n_b = st.number_input("عدد الأسياخ السفلية", value=4, step=1)
    with c2:
        fig, ax = plt.subplots(figsize=(10, 4))
        # الجائز
        ax.add_patch(patches.Rectangle((0, 0), L_b, h_b/100, color='lightgrey', alpha=0.3))
        # التسليح السفلي (مع جنشات)
        ax.plot([0.05, L_b-0.05], [0.05, 0.05], color='red', lw=3, label="Bottom Steel")
        ax.plot([0.05, 0.05], [0.05, 0.15], color='red', lw=3)
        ax.plot([L_b-0.05, L_b-0.05], [0.05, 0.15], color='red', lw=3)
        # الكانات
        for x in np.linspace(0.2, L_b-0.2, 15):
            ax.plot([x, x], [0.05, h_b/100-0.05], color='black', lw=1)
        ax.set_title("التفريد الطولي للجائز")
        ax.axis('off'); st.pyplot(fig)
    
    st.subheader("📊 جدول تفريد حديد الجائز")
    st.table({"العنصر": ["حديد سفلي رئيسي", "حديد علوي (علاقات)", "كانات"], "التفصيل": [f"{n_b} T{phi_b}", "2 T12", "T8 @ 15cm"]})

# ---------------------------------------------------------
# 4. الأعمدة والأساسات (مدمجة)
# ---------------------------------------------------------
else:
    st.info("قم باختيار القطر من القائمة الجانبية أو أدخل المعطيات مباشرة لتحديث الجداول والرسوم.")
    if choice == "الأعمدة (Columns)":
        phi_c = st.selectbox("قطر حديد العمود", [14, 16, 18, 20])
        st.table({"المقطع": ["30x60 cm"], "التسليح": [f"8 T{phi_c}"], "الكانات": ["T8 @ 15cm"]})
    elif choice == "الأساسات":
        phi_f = st.selectbox("قطر حديد القاعدة", [12, 14, 16])
        st.table({"الأبعاد": ["2.00x2.00 m"], "التسليح": [f"T{phi_f} @ 15cm"]})
