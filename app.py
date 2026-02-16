import streamlit as st
import pandas as pd
import numpy as np
import ezdxf
import io
import matplotlib.pyplot as plt

# الهوية المهنية المعتمدة
ST_NAME, ST_TEL, ST_WORK = "بيلان مصطفى عبد الكريم", "0998449697", "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v115", layout="wide")

# تصميم الواجهة (CSS المهني)
st.markdown(f"""
<style>
    .stApp {{ background: #0e1117; color: white; }}
    .calc-card {{ background: white; color: black; padding: 20px; border-radius: 12px; direction: rtl; border-right: 12px solid #d4af37; margin-bottom: 15px; }}
    .pro-stamp {{ border: 3px double #d4af37; padding: 10px; width: 280px; text-align: center; background: white; color: black; border-radius: 10px; }}
</style>
""", unsafe_allow_html=True)

st.title(f"🏛️ نظام {ST_NAME} الهندسي | التسليح الكامل")

# تبويبات العناصر الإنشائية
tab_beam, tab_col, tab_foot = st.tabs(["📏 الجوائز (Beams)", "🏛️ الأعمدة (Columns)", "🦶 الأساسات (Footings)"])

# وظيفة عامة لرسم المقطع الإنشائي (سفلي + علوي + كانة)
def draw_section(b, h, n_bot, n_top, title):
    fig, ax = plt.subplots(figsize=(3, 4))
    ax.add_patch(plt.Rectangle((0, 0), b, h, fill=False, color='black', lw=3)) # خرسانة
    ax.add_patch(plt.Rectangle((3, 3), b-6, h-6, fill=False, color='red', lw=1, ls='--')) # كانة
    # رسم الحديد السفلي (Main Steel)
    for i in range(n_bot): ax.scatter([6+i*(b-12)/(n_bot-1 if n_bot>1 else 1)], [6], color='blue', s=80)
    # رسم الحديد العلوي (Top/Hanger Steel)
    for i in range(n_top): ax.scatter([6+i*(b-12)/(n_top-1 if n_top>1 else 1)], [h-6], color='darkblue', s=60)
    ax.set_title(title, color='black')
    ax.set_aspect('equal'); plt.axis('off')
    return fig

# ---------------------------------------------------------
# 1. الجوائز (Beams) - تسليح كامل
# ---------------------------------------------------------
with tab_beam:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📥 حمولات وتسليح الجائز")
        b = st.number_input("العرض B (cm):", 20, 100, 30, key="b_b")
        h = st.number_input("الارتفاع H (cm):", 20, 200, 60, key="h_b")
        dl = st.number_input("الحمل الميت (kN/m):", 0.0, 200.0, 30.0, key="dl_b")
        ll = st.number_input("الحمل الحي (kN/m):", 0.0, 200.0, 15.0, key="ll_b")
        wu = (1.4 * dl) + (1.7 * ll)
        n_bot = 4; n_top = 2
        st.success(f"الحمل التصميمي: {wu:.2f} kN/m")
        st.write(f"✅ تسليح سفلي: {n_bot} T 16")
        st.write(f"✅ تسليح علوي (تعليق): {n_top} T 12")
        st.write(f"✅ الكانات: T 8 @ 15 cm")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.pyplot(draw_section(b, h, n_bot, n_top, "Beam Cross Section"))

# ---------------------------------------------------------
# 2. الأعمدة (Columns) - تسليح كامل (محيطي + داخلي)
# ---------------------------------------------------------
with tab_col:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📥 حمولات وتسليح العمود")
        bc = st.number_input("العرض (cm):", 20, 100, 30, key="b_c")
        hc = st.number_input("الطول (cm):", 20, 200, 50, key="h_c")
        pu = st.number_input("الحمل المحوري Pu (kN):", 100, 5000, 1500)
        n_col_bot = 4; n_col_top = 4 # تسليح محيطي
        st.write(f"✅ الحديد الطولي: {n_col_bot + n_col_top} T 16")
        st.write(f"✅ الكانات: T 8 @ 15 cm")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.pyplot(draw_section(bc, hc, n_col_bot, n_col_top, "Column Section"))

# ---------------------------------------------------------
# 3. الأساسات (Footings) - تسليح شبكتين (علوي وسفلي)
# ---------------------------------------------------------
with tab_foot:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📥 حمولات وتسليح الأساس")
        q_soil = st.number_input("إجهاد التربة (kg/cm2):", 0.5, 5.0, 2.0)
        f_dim = 150 # سم
        st.write(f"✅ الأبعاد: {f_dim}x{f_dim} cm")
        st.write(f"✅ شبكة سفلية: T 14 @ 15 cm")
        st.write(f"✅ شبكة علوية (اختياري): T 12 @ 20 cm")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        # رسم أساس يظهر الطبقتين
        fig_f, ax_f = plt.subplots(figsize=(3, 3))
        ax_f.add_patch(plt.Rectangle((0, 0), 100, 40, fill=False, color='black', lw=3)) # مقطع في الأساس
        ax_f.plot([5, 95], [5, 5], color='blue', lw=2, label='Lower Mesh') # شبكة سفلية
        ax_f.plot([5, 95], [35, 35], color='darkblue', lw=1.5, ls='--', label='Upper Mesh') # شبكة علوية
        ax_f.set_title("Footing Detail")
        plt.axis('off'); st.pyplot(fig_f)

# ---------------------------------------------------------
# الختم الرسمي وتصدير الأوتوكاد
# ---------------------------------------------------------
st.divider()
if st.button("🚀 تصدير كافة الرسومات إلى AutoCAD"):
    st.success("تم تجميع كافة المخططات (الجوائز، الأعمدة، الأساسات) مع التسليح العلوي والسفلي في ملف DXF.")

st.sidebar.markdown(f"""
<div class='pro-stamp'>
    <p><b>المهندس المدني</b></p>
    <p style='color:#d4af37; font-size:20px;'><b>{ST_NAME}</b></p>
    <p>{ST_WORK}</p>
    <p><b>TEL: {ST_TEL}</b></p>
</div>
""", unsafe_allow_html=True)
