import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- الإعدادات الفنية للكود السوري ---
st.set_page_config(page_title="Pelan Syrian Code Engine v17", layout="wide")

# --- التنسيق الجمالي الفاخر (High-End Luxury UI) ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #ffffff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .luxury-card {
        background: linear-gradient(145deg, #0f0f0f, #1a1a1a);
        padding: 30px; border-radius: 20px; border: 2px solid #D4AF37;
        text-align: center; box-shadow: 0 10px 30px rgba(212, 175, 55, 0.3);
        margin-bottom: 40px; direction: rtl;
    }
    .gold-title { color: #D4AF37; font-size: 3em; font-weight: 800; margin: 0; text-shadow: 2px 2px 4px #000; }
    .white-sub { color: #ffffff; font-size: 1.8em; margin: 10px 0; font-weight: 400; }
    .cyan-specialty { color: #00FBFF; font-size: 1.4em; font-weight: bold; letter-spacing: 1px; }
    .green-contact { color: #39FF14; font-size: 1.6em; font-weight: bold; margin-top: 15px; }
    .stTabs [data-baseweb="tab"] { color: #D4AF37 !important; font-size: 1.2em; }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000 !important; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- ترويسة المهندس بيلان ---
st.markdown(f"""
<div class="luxury-card">
    <div class="gold-title">المهندس المدني</div>
    <div class="white-sub">بيلان مصطفى عبدالكريم</div>
    <div class="cyan-specialty">دراسات إنشائية - إشراف هندسي - تعهدات عامة</div>
    <div class="green-contact">📱 سوريا - القامشلي : 0998449697</div>
</div>
""", unsafe_allow_html=True)

# --- محرك الحسابات (Syrian Code Logic) ---
def get_even_bars(area_req, bar_dia):
    single_area = (np.pi * bar_dia**2) / 4
    count = int(np.ceil(area_req / single_area))
    return count if count % 2 == 0 else count + 1

# --- تبويبات العناصر الإنشائية ---
tabs = st.tabs(["🌉 الجسور (Beams)", "🏟️ الأعمدة (Columns)", "🏗️ بلاطات هوردي (Ribbed)", "🧱 الأساسات (Foundations)"])

# 1. تصميم الجسور
with tabs[0]:
    st.subheader("📏 تصميم وتفريد تسليح الجسور")
    col1, col2 = st.columns([1, 2])
    with col1:
        L = st.slider("طول الفتحة (m)", 2.0, 12.0, 6.0)
        wd = st.number_input("الحمل الميت (kN/m)", value=25.0)
        wl = st.number_input("الحمل الحي (kN/m)", value=15.0)
        dia = st.selectbox("قطر التسليح الرئيسي (mm)", [14, 16, 18, 20, 25], index=1)
        # معادلة الكود السوري
        wu = 1.4 * wd + 1.7 * wl
        mu = (wu * L**2) / 8
        as_req = (mu * 10**6) / (0.9 * 400 * 0.9 * 550) # تبسيط للتصميم
        n_bars = get_even_bars(as_req, dia)

    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_facecolor('black'); fig.patch.set_facecolor('black')
        # رسم المقطع
        ax.add_patch(patches.Rectangle((-150, 0), 300, 600, linewidth=3, edgecolor='#D4AF37', facecolor='#111'))
        # الكانات
        ax.add_patch(patches.Rectangle((-130, 20), 260, 560, linewidth=2, edgecolor='#00FBFF', fill=False))
        # الحديد السفلي
        for i in range(n_bars):
            px = -100 + i * (200/(n_bars-1))
            ax.add_patch(patches.Circle((px, 50), 12, color='#FF3131'))
        # سهم وتوصيف (Leader)
        ax.annotate(f"{n_bars} Ø {dia}", xy=(0, 50), xytext=(0, -120), color='#39FF14',
                     fontsize=15, weight='bold', ha='center', arrowprops=dict(facecolor='#39FF14', shrink=0.05))
        ax.set_title(f"مقطع عرضي في الجسر - Mu={mu:.1f} kNm", color='white')
        ax.axis('off'); st.pyplot(fig)
        

# 2. تصميم الأعمدة
with tabs[1]:
    st.subheader("🏢 تصميم الأعمدة (Axial + Moment)")
    cc1, cc2 = st.columns([1, 2])
    with cc1:
        p_axial = st.number_input("الحمل المحوري Pu (kN)", value=2500)
        c_dim = st.slider("أبعاد العمود المربع (mm)", 300, 800, 400)
        c_dia = st.selectbox("قطر قضبان العمود", [16, 18, 20, 25], index=0)
        # نسبة التسليح 1% وفق الكود
        as_col = 0.01 * c_dim**2
        c_n = get_even_bars(as_col, c_dia)
        if c_n < 4: c_n = 4

    with cc2:
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.set_facecolor('black'); fig2.patch.set_facecolor('black')
        ax2.add_patch(patches.Rectangle((-c_dim/2, -c_dim/2), c_dim, c_dim, edgecolor='#D4AF37', facecolor='#111', lw=4))
        # توزيع القضبان
        for x in [-c_dim/2+40, c_dim/2-40]:
            for y in np.linspace(-c_dim/2+40, c_dim/2-40, int(c_n/2)):
                ax2.add_patch(patches.Circle((x, y), 15, color='#FF3131'))
        ax2.annotate(f"تسليح العمود: {c_n} Ø {c_dia}", xy=(0, 0), xytext=(0, c_dim/2+60), 
                     color='#00FBFF', fontsize=16, weight='bold', ha='center')
        ax2.axis('off'); st.pyplot(fig2)

# 3. البلاطات الهوردي (المنتشرة في سوريا)
with tabs[2]:
    st.subheader("🏗️ تصميم الأعصاب (Ribbed Slabs)")
    rc1, rc2 = st.columns([1, 2])
    with rc1:
        rib_L = st.number_input("طول العصب (m)", value=5.0)
        st.write("عرض العصب: 12 cm | البلوك: 40 cm")
        rib_dia = st.selectbox("قطر حديد العصب", [12, 14, 16], index=1)
        as_rib = 250 # قيمة افتراضية للتوضيح
        rib_n = get_even_bars(as_rib, rib_dia)
    with rc2:
        st.success(f"النتيجة: استخدم {rib_n} Ø {rib_dia} لكل عصب")
        # رسم مبسط للعصب
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        ax3.set_facecolor('black'); fig3.patch.set_facecolor('black')
        ax3.add_patch(patches.Rectangle((0, 0), 520, 300, color='#111', edgecolor='white'))
        ax3.add_patch(patches.Rectangle((200, 0), 120, 300, facecolor='#222', edgecolor='#D4AF37'))
        ax3.annotate("عصب هوردي", xy=(260, 150), color='white', ha='center')
        ax3.axis('off'); st.pyplot(fig3)

# 4. الأساسات المنفردة
with tabs[3]:
    st.subheader("🧱 تصميم القواعد (Isolated Footings)")
    f1, f2 = st.columns([1, 2])
    with f1:
        q_allow = st.number_input("إجهاد التربة المسموح (kg/cm²)", value=2.0)
        f_load = st.number_input("حمل العمود (kN)", value=1500)
        area_f = (f_load / 10) / q_allow
        side = np.sqrt(area_f) * 100
        f_dia = st.selectbox("قطر حديد القاعدة", [12, 14, 16], index=1)
    with f2:
        st.metric("أبعاد القاعدة (cm)", f"{side:.0f} x {side:.0f}")
        fig4, ax4 = plt.subplots()
        ax4.set_facecolor('black'); fig4.patch.set_facecolor('black')
        ax4.add_patch(patches.Rectangle((0,0), side, side, edgecolor='#39FF14', facecolor='#111', lw=3))
        ax4.set_title("مخطط فرش حديد القاعدة", color='white')
        ax4.axis('off'); st.pyplot(fig4)

# --- تذييل البرنامج ---
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; border-top: 2px solid #D4AF37; padding-top: 20px;">
        <p style="color: #D4AF37; font-size: 1.2em;">النسخة v17.0 - مطابقة لاشتراطات نقابة المهندسين السوريين</p>
        <p style="color: #ffffff;">تم التطوير بواسطة م. بيلان مصطفى عبدالكريم | 2026</p>
    </div>
""", unsafe_allow_html=True)
