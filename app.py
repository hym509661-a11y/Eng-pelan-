import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

# --- إعدادات الصفحة والطباعة ---
st.set_page_config(page_title="المكتب الهندسي المتكامل", layout="wide")

st.markdown("""
    <style>
    @media print { .stButton, .sidebar, header, .stSelectbox, .stNumberInput, .stRadio { display: none !important; } 
    .main { width: 100% !important; } }
    </style>
""", unsafe_allow_html=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.title("🏗️ نظام التصميم الشامل")
    choice = st.radio("اختر العنصر الإنشائي:", 
                     ["البلاطة الهوردي", "البلاطة المصمتة", "الجوائز (Beams)", "الأعمدة (Columns)", "الأساسات المنفردة", "أساس الجار (Strap)"])
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
        b_rib = st.number_input("عرض العصب b (cm)", value=12)
        b_blk = st.number_input("عرض البلوك (cm)", value=40)
        h_all = st.number_input("السماكة الكلية (cm)", value=30)
        h_blk = st.number_input("ارتفاع البلوك (cm)", value=24)
        t_bar = st.selectbox("حديد العصب", [12, 14, 16], index=1)
    
    with col2:
        spacing = b_rib + b_blk
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.add_patch(patches.Rectangle((0, 0), 3*spacing, h_all, color='#f0f0f0', ec='black', lw=2))
        for i in range(3):
            x_s = i * spacing + b_rib
            ax.add_patch(patches.Rectangle((x_s, 0), b_blk, h_blk, color='white', ec='black', hatch='///'))
            ax.add_patch(patches.Circle((i*spacing + b_rib/2, 5), 1.2, color='red'))
        ax.annotate('', xy=(b_rib/2, h_all+2), xytext=(spacing+b_rib/2, h_all+2), arrowprops=dict(arrowstyle='<->'))
        ax.text(spacing/2 + b_rib/2, h_all+4, f"S = {spacing} cm", ha='center', fontweight='bold')
        ax.set_xlim(-5, 3*spacing+5); ax.set_ylim(-10, h_all+12); ax.axis('off'); st.pyplot(fig)

    st.subheader("📊 جدول الكميات وتفاصيل العصب")
    st.table({"البيان": ["تباعد المحاور (c/c)", "تسليح العصب", "عدد البلوك / 100m²", "خرسانة / 100m²"],
              "القيمة": [f"{spacing} cm", f"2 T{t_bar}", f"{int(500/spacing * 100)} بلوكة", f"{(100*h_all/100 - (100/(spacing/100*0.2) * b_blk/100*h_blk/100*0.2)):.2f} m³"]})

# ---------------------------------------------------------
# 2. البلاطة المصمتة (Solid Slab)
# ---------------------------------------------------------
elif choice == "البلاطة المصمتة":
    st.header("💠 تفاصيل البلاطة المصمتة")
    col1, col2 = st.columns([1, 2])
    with col1:
        h_s = st.number_input("سماكة البلاطة (cm)", value=15)
        bar_s = st.selectbox("قطر الحديد", [10, 12], index=0)
    with col2:
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.add_patch(patches.Rectangle((0, 0), 100, h_s, color='#e0e0e0', ec='black'))
        for x in np.linspace(10, 90, 6): ax.add_patch(patches.Circle((x, 4), 1.5, color='red'))
        ax.set_xlim(-10, 110); ax.set_ylim(-5, h_s+10); ax.axis('off'); st.pyplot(fig)
    st.table({"العنصر": ["تسليح الفرش", "تسليح الغطاء"], "التفاصيل": [f"T{bar_s} @ 15cm", f"T10 @ 15cm"]})

# ---------------------------------------------------------
# 3. الجوائز (Beams)
# ---------------------------------------------------------
elif choice == "الجوائز (Beams)":
    st.header("🔗 تفاصيل تسليح الجائز")
    col1, col2 = st.columns([1, 2])
    with col1:
        L_b = st.number_input("طول الجائز (m)", value=5.0)
        h_b = st.number_input("الارتفاع h (cm)", value=60)
        b_b = st.number_input("العرض b (cm)", value=25)
    with col2:
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot([0, L_b], [0, 0], color='lightgrey', lw=40, alpha=0.4)
        ax.plot([0.1, L_b-0.1], [-0.15, -0.15], 'red', lw=3, label="Main Steel")
        for x in np.linspace(0.1, L_b-0.1, 15): ax.plot([x, x], [-0.25, 0.25], 'black', lw=1)
        ax.axis('off'); st.pyplot(fig)
    st.subheader("📊 جدول تفريد حديد الجائز (BBS)")
    st.table({"النوع": ["سفلي رئيسي", "علوي", "كانات"], "التسليح": ["4 T16", "2 T12", "T8 @ 15cm"], "الطول (m)": [L_b+0.4, L_b, 2*(h_b+b_b-10)/100+0.1]})

# ---------------------------------------------------------
# 4. الأعمدة (Columns)
# ---------------------------------------------------------
elif choice == "الأعمدة (Columns)":
    st.header("🏢 تفاصيل مقطع العمود")
    col1, col2 = st.columns([1, 2])
    with col1:
        c_w = st.number_input("العرض b (cm)", value=30)
        c_h = st.number_input("الارتفاع h (cm)", value=60)
        n_c = st.number_input("عدد الأسياخ", value=8)
    with col2:
        fig, ax = plt.subplots(figsize=(4, 5))
        ax.add_patch(patches.Rectangle((0, 0), c_w, c_h, color='#f9f9f9', ec='black', lw=3))
        for i in [4, c_w-4]:
            for j in np.linspace(4, c_h-4, int(n_c/2)): ax.add_patch(patches.Circle((i, j), 1.5, color='red'))
        ax.axis('off'); st.pyplot(fig)
    st.table({"المقطع": [f"{c_w}x{c_h} cm"], "التسليح": [f"{n_c} T16"], "الكانات": ["T8 @ 15cm"]})

# ---------------------------------------------------------
# 5. الأساسات (Footings)
# ---------------------------------------------------------
elif choice == "الأساسات المنفردة":
    st.header("📐 تصميم الأساس المنفرد")
    col1, col2 = st.columns([1, 2])
    with col1:
        P_f = st.number_input("الحمل (Ton)", value=120.0)
        q_s = st.number_input("إجهاد التربة (kg/cm2)", value=2.0)
    with col2:
        dim = math.sqrt((P_f*1.1)/(q_s*10))
        fig, ax = plt.subplots(); ax.add_patch(patches.Rectangle((0, 0), dim, dim, color='grey', alpha=0.3, ec='black'))
        for x in np.linspace(0.1, dim-0.1, 8):
            ax.plot([x, x], [0, dim], 'red', lw=1); ax.plot([0, dim], [x, x], 'red', lw=1)
        ax.set_aspect('equal'); ax.axis('off'); st.pyplot(fig)
    st.table({"الأبعاد": [f"{dim:.2f}x{dim:.2f} m"], "الحديد": ["T14 @ 15cm"], "الخرسانة": [f"{dim**2*0.6:.2f} m³"]})

# ---------------------------------------------------------
# 6. أساس الجار (Strap Footing)
# ---------------------------------------------------------
elif choice == "أساس الجار (Strap)":
    st.header("🏗️ تفاصيل أساس الجار والشداد")
    col1, col2 = st.columns([1, 2])
    with col1:
        s_L = st.number_input("المسافة بين العمودين (m)", value=5.0)
        s_h = st.number_input("ارتفاع الشداد (cm)", value=80)
    with col2:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.add_patch(patches.Rectangle((0, 0), 1, 1, color='grey', alpha=0.5))
        ax.add_patch(patches.Rectangle((s_L-1, 0), 1.2, 1.2, color='grey', alpha=0.5))
        ax.plot([0.5, s_L], [0.5, 0.5], color='black', lw=15) # الشداد
        ax.axis('off'); st.pyplot(fig)
    st.table({"عنصر الشداد": ["تسليح علوي", "تسليح سفلي", "كانات الشداد"], "القيمة": ["5 T18", "3 T16", "5 T10/m"]})
