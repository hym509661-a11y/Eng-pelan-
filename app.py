import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

# --- إعدادات التطبيق ---
st.set_page_config(page_title="المصمم الإنشائي - نسخة الطباعة", layout="wide")

# --- دالة زر الطباعة (JavaScript) ---
def add_print_button():
    st.markdown(
        """
        <button onclick="window.print()" style="
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 20px;">
            🖨️ طباعة الصفحة / حفظ كـ PDF
        </button>
        """,
        unsafe_allow_html=True
    )

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("⚙️ معطيات المواد")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)
    st.divider()
    add_print_button() # زر الطباعة في القائمة الجانبية أيضاً

menu = ["الجوائز (Beams)", "البلاطات الهوردي (Ribbed)", "الأساسات (Footings)", "الأعمدة (Columns)"]
choice = st.selectbox("🎯 اختر العنصر المطلوب:", menu)

# ---------------------------------------------------------
# 1. الجوائز (Beams) - رسم طولي + مقطع عرضي + طباعة
# ---------------------------------------------------------
if choice == "الجوائز (Beams)":
    st.header("🔗 تفاصيل تسليح الجوائز والكانات")
    
    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        L = st.number_input("الطول L (m)", value=5.0)
        b = st.number_input("العرض b (cm)", value=25)
    with col_in2:
        h = st.number_input("الارتفاع h (cm)", value=60)
        wu = st.number_input("الحمولة wu (t/m)", value=3.5)
    with col_in3:
        bar_size = st.selectbox("قطر الحديد (T)", [12, 14, 16, 18, 20], index=2)
        stirrup_size = st.selectbox("قطر الكانات (T)", [8, 10], index=0)

    if st.button("تحديث الحسابات والرسوم"):
        add_print_button() # زر الطباعة يظهر بعد الحساب أيضاً
        
        # الحسابات الإنشائية
        Mu = (wu * L**2) / 8
        As_req = (Mu * 10**5) / (0.87 * fy * (h-5))
        bar_area = (math.pi * (bar_size/10)**2) / 4
        n_bars = math.ceil(As_req / bar_area)
        
        # --- رسم 1: التفريد الطولي ---
        st.subheader("🖼️ التفريد الطولي (Longitudinal Detail)")
        fig, ax = plt.subplots(figsize=(12, 3))
        ax.plot([0, L], [0, 0], color='#E0E0E0', lw=50, alpha=0.5) # خرسانة
        ax.plot([0.05, L-0.05], [-0.18, -0.18], 'red', lw=4, label=f"Main: {n_bars} T{bar_size}")
        ax.plot([0, L], [0.18, 0.18], 'green', lw=2, label="Hangers: 2 T12")
        for x in np.linspace(0.1, L-0.1, 20):
            ax.plot([x, x], [-0.25, 0.25], 'black', lw=1, alpha=0.7) # كانات
        ax.set_ylim(-0.8, 0.8); ax.axis('off'); ax.legend(loc='lower center', ncol=3)
        st.pyplot(fig)

        # --- رسم 2: المقطع العرضي (الذي طلبته) ---
        st.subheader("📐 المقطع العرضي (Section A-A)")
        fig_sec, ax_sec = plt.subplots(figsize=(4, 5))
        # رسم الكانة (المستطيل الخارجي)
        rect = patches.Rectangle((0, 0), b, h, linewidth=2, edgecolor='black', facecolor='#F5F5F5')
        ax_sec.add_patch(rect)
        # رسم الأسياخ السفلية
        for i in range(n_bars):
            pos_x = (b/ (n_bars + 1)) * (i + 1)
            circle = patches.Circle((pos_x, 5), 1.5, color='red')
            ax_sec.add_patch(circle)
        # رسم الأسياخ العلوية
        ax_sec.add_patch(patches.Circle((5, h-5), 1.2, color='green'))
        ax_sec.add_patch(patches.Circle((b-5, h-5), 1.2, color='green'))
        
        ax_sec.set_xlim(-5, b+5); ax_sec.set_ylim(-5, h+5); ax_sec.axis('off')
        st.pyplot(fig_sec)

        # --- جدول BBS ---
        st.subheader("📊 جدول تفريد الحديد (BBS)")
        st.table({
            "العنصر": ["حديد سفلي", "حديد علوي", "كانات"],
            "القطر": [f"T{bar_size}", "T12", f"T{stirrup_size}"],
            "العدد": [n_bars, 2, f"{int(L/0.15)}/m"],
            "الطول (m)": [L+0.4, L, round(2*(b+h-10)/100 + 0.1, 2)]
        })

# ---------------------------------------------------------
# 2. الأساسات (Footings)
# ---------------------------------------------------------
elif choice == "الأساسات (Footings)":
    st.header("📐 تفاصيل الأساس المنفرد")
    P = st.number_input("حمل العمود (Ton)", value=120.0)
    q = st.number_input("تحمل التربة (kg/cm2)", value=2.0)
    
    if st.button("تصميم ورسم"):
        add_print_button()
        area = (P * 1.1) / (q * 10)
        side = math.sqrt(area)
        
        st.success(f"الأبعاد المطلوبة: {side:.2f} x {side:.2f} m")
        
        fig_f, ax_f = plt.subplots(figsize=(5, 5))
        ax_f.add_patch(patches.Rectangle((0, 0), side, side, color='grey', alpha=0.3))
        # شبكة تسليح
        for i in np.linspace(0.2, side-0.2, 8):
            ax_f.plot([i, i], [0.1, side-0.1], 'red', lw=1.5)
            ax_f.plot([0.1, side-0.1], [i, i], 'red', lw=1.5)
        ax_f.axis('off'); st.pyplot(fig_f)
        
        st.table({"العنصر": ["أبعاد القاعدة", "التسليح"], "التفاصيل": [f"{side:.2f} m", "T14 @ 15cm"]})

# ---------------------------------------------------------
# 3. البلاطات الهوردي والأعمدة (تكملة بنفس النمط)
# ---------------------------------------------------------
else:
    st.info("قم بإدخال المعطيات والضغط على تحديث لعرض الرسومات وجدول BBS.")
    add_print_button()
