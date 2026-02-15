import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المكتب الهندسي المتكامل", layout="wide")

# --- تنسيق الطباعة ---
st.markdown("""
    <style>
    @media print { .stButton, .sidebar, header, .stSelectbox, .stNumberInput { display: none !important; } }
    </style>
""", unsafe_allow_html=True)

# --- القائمة الجانبية (اختيار العنصر) ---
with st.sidebar:
    st.title("🏗️ اللوحة الهندسية")
    choice = st.radio("اختر العنصر للتصميم:", 
                     ["البلاطة الهوردي (Ribbed)", "الجائز (Beam)", "الأساسات (Footings)", "الأعمدة (Columns)"])
    st.divider()
    if st.button("🖨️ اضغط للطباعة / حفظ PDF"):
        st.write("استخدم (Ctrl + P) للطباعة بعد الضغط")

# ---------------------------------------------------------
# 1. البلاطة الهوردي (Ribbed Slab) - تفاصيل كاملة
# ---------------------------------------------------------
if choice == "البلاطة الهوردي (Ribbed)":
    st.header("🧱 تفاصيل البلاطة الهوردي والأعصاب")
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.subheader("📝 إدخال المعطيات")
        b_rib = st.number_input("عرض العصب b (cm)", value=12)
        b_block = st.number_input("عرض البلوك (cm)", value=40)
        h_total = st.number_input("السماكة الكلية h (cm)", value=30)
        h_block = st.number_input("ارتفاع البلوك (cm)", value=24)
        rib_bar = st.selectbox("قطر حديد العصب", [12, 14, 16], index=1)
        
    with c2:
        spacing = b_rib + b_block
        st.subheader("📐 المقطع العرضي وتوزيع المحاور")
        fig, ax = plt.subplots(figsize=(10, 4))
        # رسم البيتون والبلوك
        ax.add_patch(patches.Rectangle((0, 0), 3*spacing, h_total, color='#f0f0f0', ec='black', lw=2))
        for i in range(3):
            x_s = i * spacing + b_rib
            ax.add_patch(patches.Rectangle((x_s, 0), b_block, h_block, color='white', ec='black', hatch='///'))
            ax.add_patch(patches.Circle((i*spacing + b_rib/2, 5), 1.2, color='red')) # حديد سفلي
        
        ax.annotate('', xy=(b_rib/2, h_total+3), xytext=(spacing+b_rib/2, h_total+3), arrowprops=dict(arrowstyle='<->'))
        ax.text(spacing/2 + b_rib/2, h_total+5, f"S = {spacing} cm", ha='center', fontweight='bold')
        ax.set_xlim(-5, 3*spacing+5); ax.set_ylim(-10, h_total+15); ax.axis('off')
        st.pyplot(fig)
        

    # جدول التفاصيل والكميات (BBS)
    st.subheader("📊 جدول تفاصيل التسليح والكميات")
    st.table({
        "العنصر": ["تسليح العصب", "تباعد المحاور c/c", "عدد البلوك / 100m²", "خرسانة العصب الواحد / m'"],
        "القطر/القياس": [f"2 T{rib_bar}", f"{spacing} cm", f"{int(100/((spacing/100)*0.2))} بلوكة", f"{(b_rib*h_total/10000):.3f} m³"]
    })

# ---------------------------------------------------------
# 2. الجوائز (Beams) - طولي وعرضي
# ---------------------------------------------------------
elif choice == "الجائز (Beam)":
    st.header("🔗 تفاصيل تسليح الجائز")
    c1, c2 = st.columns([1, 2])
    with c1:
        L = st.number_input("طول الجائز (m)", value=5.0)
        beam_h = st.number_input("الارتفاع h (cm)", value=60)
        beam_b = st.number_input("العرض b (cm)", value=25)
        main_bar = st.selectbox("الحديد الرئيسي", [14, 16, 18, 20], index=1)
    
    with c2:
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot([0, L], [0, 0], color='lightgrey', lw=40, alpha=0.4)
        ax.plot([0.1, L-0.1], [-0.15, -0.15], 'red', lw=3, label="Main Steel")
        for x in np.linspace(0.1, L-0.1, 15): ax.plot([x, x], [-0.25, 0.25], 'black', lw=1)
        ax.axis('off'); st.pyplot(fig)
        

    st.subheader("📊 جدول تفريد الحديد (BBS)")
    st.table({
        "النوع": ["سفلي رئيسي", "علوي (علاقات)", "كانات"],
        "التسليح": [f"4 T{main_bar}", "2 T12", "T8 @ 15cm"],
        "الطول التقديري": [f"{L+0.4} m", f"{L} m", f"{2*(beam_h+beam_b-10)/100 + 0.1:.2f} m"]
    })

# ---------------------------------------------------------
# 3. الأساسات (Footings)
# ---------------------------------------------------------
elif choice == "الأساسات (Footings)":
    st.header("📐 تصميم الأساسات")
    c1, c2 = st.columns([1, 2])
    with c1:
        P = st.number_input("حمل العمود (Ton)", value=120.0)
        q = st.number_input("تحمل التربة (kg/cm2)", value=2.0)
        f_bar = st.selectbox("قطر الحديد", [14, 16, 18])
    with c2:
        area = (P * 1.1) / (q * 10)
        side = math.sqrt(area)
        fig, ax = plt.subplots()
        ax.add_patch(patches.Rectangle((0, 0), side, side, color='lightgrey', ec='black'))
        for i in np.linspace(0.1, side-0.1, 8):
            ax.plot([i, i], [0.05, side-0.05], 'red', lw=1)
            ax.plot([0.05, side-0.05], [i, i], 'red', lw=1)
        ax.set_aspect('equal'); ax.axis('off'); st.pyplot(fig)
        

    st.table({"الأبعاد النهائية": [f"{side:.2f} x {side:.2f} m"], "التسليح": [f"T{f_bar} @ 15cm"], "حجم الخرسانة": [f"{area*0.6:.2f} m³"]})

# ---------------------------------------------------------
# 4. الأعمدة (Columns)
# ---------------------------------------------------------
elif choice == "الأعمدة (Columns)":
    st.header("🏢 تفاصيل تسليح العمود")
    c_b = st.number_input("العرض b (cm)", value=30)
    c_h = st.number_input("الارتفاع h (cm)", value=60)
    
    fig, ax = plt.subplots(figsize=(4, 5))
    ax.add_patch(patches.Rectangle((0, 0), c_b, c_h, color='#f0f0f0', ec='black', lw=3))
    # رسم الأسياخ
    for i in [5, c_b-5]:
        for j in np.linspace(5, c_h-5, 4):
            ax.add_patch(patches.Circle((i, j), 1.5, color='red'))
    ax.axis('off'); st.pyplot(fig)
    
    st.table({"المقطع": [f"{c_b}x{c_h} cm"], "التسليح": ["8 T16"], "الكانات": ["T8 @ 15cm"]})
