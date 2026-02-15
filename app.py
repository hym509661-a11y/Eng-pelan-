import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المكتب الهندسي المتكامل", layout="wide")

# --- دالة الطباعة الاحترافية ---
def add_print_button():
    st.markdown("""
        <style>
        @media print {
            .stButton, .stSelectbox, .stNumberInput, .sidebar, .stRadio { display: none !important; }
            .main { width: 100% !important; }
            header { visibility: hidden; }
        }
        </style>
        <button onclick="window.print()" style="
            background-color: #2e7d32; color: white; padding: 12px 24px;
            border: none; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%;">
            🖨️ طباعة التقرير الفني / حفظ PDF
        </button>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("🏗️ الإعدادات العامة للمواد")
    fcu = st.number_input("إجهاد البيتون fcu (MPa)", value=25)
    fy = st.number_input("إجهاد الحديد fy (MPa)", value=400)
    st.divider()
    add_print_button()

menu = ["الجوائز (Beams)", "البلاطات (Slabs)", "الأساسات الشاملة (Footings)", "الأعمدة (Columns)", "أساس الجار (Strap)"]
choice = st.selectbox("🎯 اختر العنصر المراد تصميمه:", menu)

# ---------------------------------------------------------
# 1. الجوائز (Beams) - طولي وعرضي وتفريد
# ---------------------------------------------------------
if choice == "الجوائز (Beams)":
    st.header("🔗 تصميم الجوائز (Beams Construction Detail)")
    c1, c2, c3 = st.columns(3)
    with c1:
        L = st.number_input("طول الجائز (m)", value=5.0)
        b = st.number_input("العرض b (cm)", value=25)
    with c2:
        h = st.number_input("الارتفاع h (cm)", value=60)
        wu = st.number_input("الحمولة (t/m)", value=3.5)
    with c3:
        bar_main = st.selectbox("قطر الحديد الرئيسي", [14, 16, 18, 20], index=1)
        bar_stir = st.selectbox("قطر الكانات", [8, 10], index=0)

    if st.button("تحديث الحسابات والرسم"):
        Mu = (wu * L**2) / 8
        As = (Mu * 10**5) / (0.87 * fy * (h-5))
        n = math.ceil(As / (math.pi*(bar_main/20)**2))
        
        # الرسم الطولي
        st.subheader("🖼️ الرسم الطولي وتوزيع الكانات")
        fig, ax = plt.subplots(figsize=(10, 2))
        ax.plot([0, L], [0, 0], color='#d1d1d1', lw=40, alpha=0.5)
        ax.plot([0.1, L-0.1], [-0.15, -0.15], 'red', lw=3, label=f"Main: {n}T{bar_main}")
        ax.plot([0, L], [0.15, 0.15], 'green', lw=2, label="2T12")
        for x in np.linspace(0.1, L-0.1, 18): ax.plot([x, x], [-0.25, 0.25], 'black', lw=1)
        ax.axis('off'); ax.legend(loc='lower center', ncol=3); st.pyplot(fig)

        # المقطع العرضي
        st.subheader("📐 المقطع العرضي Section A-A")
        fig2, ax2 = plt.subplots(figsize=(3, 4))
        ax2.add_patch(patches.Rectangle((0, 0), b, h, color='#f9f9f9', ec='black', lw=2))
        for i in range(n): ax2.add_patch(patches.Circle(((b/(n+1))*(i+1), 5), 1.5, color='red'))
        ax2.add_patch(patches.Circle((5, h-5), 1.2, color='green'))
        ax2.add_patch(patches.Circle((b-5, h-5), 1.2, color='green'))
        ax2.set_xlim(-5, b+5); ax2.set_ylim(-5, h+5); ax2.axis('off'); st.pyplot(fig2)

        st.table({"العنصر": ["حديد سفلي", "علاقات علوية", "كانات مغلقة"], "القطر": [f"T{bar_main}", "T12", f"T{bar_stir}"], "العدد": [n, 2, f"{int(L/0.15)}/m"]})

# ---------------------------------------------------------
# 2. البلاطات (Slabs) - هوردي ومصمتة
# ---------------------------------------------------------
elif choice == "البلاطات (Slabs)":
    st.header("🧱 تصميم البلاطات (Slabs)")
    s_type = st.radio("نوع البلاطة", ["هوردي (Ribbed)", "مصمتة (Solid)"])
    col1, col2 = st.columns(2)
    with col1:
        L_s = st.number_input("طول البحر (m)", value=5.0)
        thick = st.number_input("السماكة الكلية (cm)", value=30 if s_type=="هوردي (Ribbed)" else 15)
    with col2:
        s_bar = st.selectbox("قطر الحديد", [10, 12, 14, 16])
        load = st.number_input("الحمولة wu (t/m2)", value=0.8)

    if st.button("عرض تفاصيل البلاطة"):
        if s_type == "هوردي (Ribbed)":
            st.info("تفاصيل العصب: عرض 12سم، بلوك 40سم")
            st.table({"عنصر العصب": ["تسليح العصب", "تسليح البلاطة"], "القيمة": [f"2 T{s_bar}", "T8 @ 20cm"]})
        else:
            st.table({"عنصر البلاطة": ["تسليح الاتجاه القصير", "تسليح الاتجاه الطويل"], "القيمة": [f"T{s_bar} @ 15cm", "T10 @ 15cm"]})

# ---------------------------------------------------------
# 3. الأساسات الشاملة (Footings) - منفرد ومشترك
# ---------------------------------------------------------
elif choice == "الأساسات الشاملة (Footings)":
    st.header("📐 تصميم الأساسات المنفردة والمشتركة")
    f_mode = st.radio("اختر نوع الأساس", ["منفرد Isolated", "مشترك Combined"])
    col1, col2, col3 = st.columns(3)
    with col1:
        P_val = st.number_input("حمل العمود (Ton)", value=120.0)
        q_soil = st.number_input("تحمل التربة (kg/cm2)", value=2.0)
    with col2:
        f_depth = st.number_input("سماكة القاعدة (cm)", value=60)
        f_bar_size = st.selectbox("قطر الحديد الرئيسي", [14, 16, 18], index=1)
    with col3:
        b_col = st.number_input("عرض العمود (cm)", value=30)
        h_col = st.number_input("طول العمود (cm)", value=60)

    if st.button("تحليل ورسم القاعدة"):
        area_req = (P_val * 1.1) / (q_soil * 10)
        side = math.sqrt(area_req)
        L_final = side + (h_col-b_col)/200 if f_mode == "منفرد Isolated" else side*1.5
        B_final = area_req / L_final

        st.success(f"الأبعاد المقترحة: {L_final:.2f} m x {B_final:.2f} m")
        
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.add_patch(patches.Rectangle((0, 0), L_final, B_final, color='lightgrey', alpha=0.5, label='Concrete'))
        # رسم شبكة الحديد
        for x in np.linspace(0.2, L_final-0.2, 10): ax.plot([x, x], [0.1, B_final-0.1], 'red', lw=1, alpha=0.6)
        for y in np.linspace(0.2, B_final-0.2, 8): ax.plot([0.1, L_final-0.1], [y, y], 'red', lw=1, alpha=0.6)
        ax.set_aspect('equal'); ax.axis('off'); st.pyplot(fig)
        
        st.table({"البيانات": ["المساحة المطلوبة", "التسليح (فرش/غطاء)", "سماكة الصب"], "النتائج": [f"{area_req:.2f} m2", f"T{f_bar_size} @ 15cm", f"{f_depth} cm"]})

# ---------------------------------------------------------
# 4. الأعمدة وأساس الجار
# ---------------------------------------------------------
else:
    st.header(f"🏗️ تصميم {choice}")
    st.info("قم بإدخال المعطيات والضغط على تحديث لعرض الرسومات وجدول الكميات.")
    if st.button("عرض التفاصيل"):
        st.table({"العنصر": ["التسليح المقترح", "الكانات"], "القيمة": ["حسب الكود السوري/المصري", "T8 @ 15cm"]})
