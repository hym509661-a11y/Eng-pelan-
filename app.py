import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- الترويسة باسم المهندس بيلان ---
st.set_page_config(page_title="Bilan Engineering Engine", layout="wide")
st.markdown(f"<h1 style='text-align: center; color: #0047AB;'>Bilan Engineering Design Engine</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center;'>المهندس المصمم: بيلان عبدالكريم</h3>", unsafe_allow_html=True)
st.divider()

# --- مدخلات التصميم ---
with st.sidebar:
    st.header("📥 مدخلات التصميم")
    type_el = st.selectbox("العنصر الإنشائي", ["جائز (Beam)", "عمود (Column)"])
    L = st.number_input("طول البحر أو الارتفاع (m)", value=5.0)
    b = st.number_input("العرض b (cm)", value=30)
    h = st.number_input("الارتفاع h (cm)", value=60)
    w_dead = st.number_input("الحمل الميت (t/m)", value=2.0)
    w_live = st.number_input("الحمل الحي (t/m)", value=1.5)
    
    st.divider()
    st.header("🔗 خيارات التسليح")
    phi = st.selectbox("قطر السيخ المستخدم (mm)", [12, 14, 16, 18, 20, 25])
    fy = 4000  # إجهاد الخضوع للحديد

# --- المحرك الحسابي ---
w_u = 1.4 * w_dead + 1.6 * w_live
M_u = (w_u * L**2) / 8  # للعزم البسيط
As_req = (M_u * 10**5) / (0.87 * fy * (h-5)) # مساحة الحديد المطلوبة تقريبياً

# حساب عدد الأسياخ تلقائياً
area_single_bar = (np.pi * (phi/10)**2) / 4
n_bars = int(np.ceil(As_req / area_single_bar))
if n_bars < 2: n_bars = 2 # الحد الأدنى سيخان

# --- العرض البياني ---
col_graph, col_calc = st.columns([2, 1])

with col_graph:
    st.subheader("🖼️ الرسم الهندسي للعنصر")
    fig, ax = plt.subplots(figsize=(8, 4))
    
    if type_el == "جائز (Beam)":
        # رسم الجائز بمقياس رسم
        rect = patches.Rectangle((0, 0), L, h/100, linewidth=2, edgecolor='black', facecolor='#D3D3D3')
        ax.add_patch(rect)
        # رسم الأسياخ داخل المقطع
        for i in range(n_bars):
            ax.plot([0.1, L-0.1], [0.05, 0.05], color='red', lw=2)
        ax.set_xlim(-0.5, L+0.5)
        ax.set_ylim(-0.2, 1)
        ax.set_title(f"Cross Section: {b}x{h} cm | Length: {L} m")
    
    else: # عمود
        rect = patches.Rectangle((0, 0), b/100, L, linewidth=2, edgecolor='black', facecolor='#D3D3D3')
        ax.add_patch(rect)
        ax.set_xlim(-0.5, 1)
        ax.set_ylim(-0.5, L+0.5)
        ax.set_title(f"Column Section: {b}x{h} cm | Height: {L} m")

    ax.axis('off')
    st.pyplot(fig)

    # مخططات العزم والقص
    st.subheader("📉 التحليل الإنشائي (Diagrams)")
    x = np.linspace(0, L, 100)
    moments = (w_u * x / 2) * (L - x)
    
    fig2, ax2 = plt.subplots(figsize=(8, 3))
    ax2.fill_between(x, moments, color='blue', alpha=0.3)
    ax2.set_title("مخطط العزم المنعطف (Bending Moment Diagram)")
    ax2.invert_yaxis()
    st.pyplot(fig2)

with col_calc:
    st.subheader("📋 تقرير النتائج")
    st.success(f"الحمل التصميمي $W_u$: {w_u:.2f} t/m")
    st.info(f"العزم الأعظمي $M_u$: {M_u:.2f} t.m")
    
    st.divider()
    st.write("### تفاصيل التسليح المحسوبة:")
    st.metric("عدد الأسياخ المطلوب", f"{n_bars} T{phi}")
    st.write(f"المساحة المطلوبة: {As_req:.2f} cm²")
    st.write(f"المساحة المحققة: {n_bars * area_single_bar:.2f} cm²")
    
    # تحذير الكود السوري للأعمدة
    if type_el == "عمود (Column)" and (b * h) < 900:
        st.error("🚨 تحذير: مساحة المقطع أقل من 900 سم² (مخالف للكود السوري)")

# --- المذكرة الحسابية ---
st.divider()
st.subheader("📝 المذكرة الحسابية الكاملة")
with st.expander("اضغط لعرض المذكرة الجاهزة للطباعة"):
    st.write(f"**المشروع:** تصميم إنشائي آلي")
    st.write(f"**إعداد المهندس:** بيلان عبدالكريم")
    st.write(f"**تاريخ الإصدار:** 2026-02-15")
    st.write("---")
    st.latex(r"W_u = 1.4 \cdot DL + 1.6 \cdot LL")
    st.latex(r"M_u = \frac{W_u \cdot L^2}{8}")
    st.latex(r"A_s = \frac{M_u}{0.87 \cdot f_y \cdot d}")
    st.write(f"بناءً على الحسابات، يتم استخدام **{n_bars}** قضبان بقطر **{phi}** مم.")



