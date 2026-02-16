import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# إعدادات الصفحة
st.set_page_config(page_title="Pelan Ultimate Engineering v16", layout="wide")

# --- التنسيق الجمالي الفاخر (High Contrast Luxury CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #ffffff; }
    
    .luxury-header {
        background: linear-gradient(135deg, #111 0%, #000 100%);
        padding: 25px;
        border-radius: 15px;
        border: 3px solid #FFD700; /* ذهبي فاقع */
        text-align: center;
        box-shadow: 0px 0px 20px rgba(255, 215, 0, 0.3);
        margin-bottom: 30px;
        direction: rtl;
    }
    .main-title { color: #FFD700; font-size: 2.8em; font-weight: bold; text-shadow: 2px 2px #000; }
    .sub-title { color: #ffffff; font-size: 1.8em; margin: 10px 0; }
    .specialty { color: #00e5ff; font-size: 1.3em; font-weight: bold; }
    .phone-box { color: #39FF14; font-size: 1.6em; font-weight: bold; margin-top: 15px; }

    /* جداول واضحة */
    .stTable { background-color: #111; border: 1px solid #444; }
    h1, h2, h3 { color: #FFD700 !important; }
</style>
""", unsafe_allow_html=True)

# --- عرض الترويسة الملكية ---
st.markdown(f"""
<div class="luxury-header">
    <div class="main-title">المهندس المدني</div>
    <div class="sub-title">بيلان مصطفى عبدالكريم</div>
    <div class="specialty">دراسات - إشراف - تعهدات</div>
    <div class="phone-box">الرقم : 0998449697</div>
</div>
""", unsafe_allow_html=True)

# --- نظام التصميم الشامل ---
tabs = st.tabs(["📏 تصميم الجسور (Beams)", "🏢 تصميم الأعمدة (Columns)", "📑 تصميم البلاطات (Slabs)"])

# وظيفة لتقريب العدد لأقرب زوجي
def round_to_even(n):
    n = int(np.ceil(n))
    return n if n % 2 == 0 else n + 1

# 1. قسم الجسور
with tabs[0]:
    st.header("📐 Analysis & Design of Beams")
    c1, c2 = st.columns([1, 2])
    with c1:
        mu = st.number_input("العزم التصميمي Mu (kN.m)", value=150.0, key="b_mu")
        b = st.number_input("عرض الجسر b (mm)", value=300)
        h = st.number_input("ارتفاع الجسر h (mm)", value=600)
        bar_d = st.selectbox("اختر قطر التسليح الرئيسي (mm)", [12, 14, 16, 18, 20, 25], index=2)
        
        # حسابات الجسور
        as_req = (mu * 10**6) / (0.9 * 400 * 0.9 * (h-50))
        bar_area = (np.pi * bar_d**2) / 4
        n_bars = round_to_even(as_req / bar_area)
        if n_bars < 2: n_bars = 2
        
    with c2:
        st.subheader("مخطط تسليح الجسر التفصيلي")
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
        # رسم الخرسانة
        ax.add_patch(patches.Rectangle((-b/2, 0), b, h, linewidth=3, edgecolor='#FFD700', facecolor='#111'))
        # رسم الحديد السفلي
        for i in range(n_bars):
            px = (-b/2 + 50) + i * (b-100)/(n_bars-1)
            ax.add_patch(patches.Circle((px, 50), 10, color='#FF3131'))
        # سهم التوصيف
        ax.annotate(f"{n_bars} Ø {bar_d}", xy=(0, 50), xytext=(0, -100), color='#39FF14',
                     fontsize=14, weight='bold', ha='center', arrowprops=dict(color='#39FF14', shrink=0.05))
        ax.set_xlim(-b, b); ax.set_ylim(-150, h+100); ax.axis('off')
        st.pyplot(fig)

# 2. قسم الأعمدة
with tabs[1]:
    st.header("🏢 Column Axial Design")
    cc1, cc2 = st.columns([1, 2])
    with cc1:
        pu = st.number_input("الحمل المحوري Pu (kN)", value=2000.0)
        c_width = st.number_input("عرض العمود (mm)", value=400)
        c_depth = st.number_input("عمق العمود (mm)", value=400)
        c_bar_d = st.selectbox("قطر قضبان العمود (mm)", [14, 16, 18, 20, 25], index=1)
        
        # حسابات الأعمدة (مينيموم 1%)
        as_min = 0.01 * c_width * c_depth
        c_bar_area = (np.pi * c_bar_d**2) / 4
        c_n_bars = round_to_even(as_min / c_bar_area)
        if c_n_bars < 4: c_n_bars = 4 # الحد الأدنى للأعمدة المستطيلة
        
    with cc2:
        st.subheader("توزيع حديد العمود")
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.set_facecolor('black'); fig2.patch.set_facecolor('black')
        ax2.add_patch(patches.Rectangle((-c_width/2, -c_depth/2), c_width, c_depth, linewidth=3, edgecolor='#00e5ff', facecolor='#111'))
        
        # توزيع القضبان على الأركان والجانبين (تبسيط للرسم)
        for x in [-c_width/2+40, c_width/2-40]:
            for y in np.linspace(-c_depth/2+40, c_depth/2-40, int(c_n_bars/2)):
                ax2.add_patch(patches.Circle((x, y), 12, color='#39FF14'))
        
        ax2.annotate(f"Total: {c_n_bars} Ø {c_bar_d}", xy=(0, 0), xytext=(0, c_depth/2 + 50), 
                     color='#FFD700', fontsize=14, weight='bold', ha='center')
        ax2.set_xlim(-c_width, c_width); ax2.set_ylim(-c_depth, c_depth); ax2.axis('off')
        st.pyplot(fig2)

# 3. قسم البلاطات
with tabs[2]:
    st.header("📑 Slab Reinforcement (Per Meter)")
    cs1, cs2 = st.columns([1, 2])
    with cs1:
        s_thick = st.number_input("سماكة البلاطة (mm)", value=150)
        s_moment = st.number_input("العزم في المتر الواحد (kN.m/m)", value=25.0)
        s_bar_d = st.selectbox("قطر حديد البلاطة (mm)", [8, 10, 12, 14], index=1)
        
        s_bar_area = (np.pi * s_bar_d**2) / 4
        as_slab = (s_moment * 10**6) / (0.9 * 400 * 0.9 * (s_thick-30))
        # حساب العدد في المتر
        n_slab = round_to_even(as_slab / s_bar_area)
        if n_slab < 5: n_slab = 6 # الحد الأدنى العملي
        spacing = 1000 / n_slab
        
    with cs2:
        st.subheader("مخطط فرش البلاطة (Section)")
        fig3, ax3 = plt.subplots(figsize=(8, 3))
        ax3.set_facecolor('black'); fig3.patch.set_facecolor('black')
        ax3.add_patch(patches.Rectangle((0, 0), 1000, s_thick, edgecolor='#ffffff', facecolor='#111'))
        for i in range(n_slab):
            ax3.add_patch(patches.Circle((i*spacing + spacing/2, 25), 6, color='#FF3131'))
        
        st.pyplot(fig3)
        st.success(f"النتيجة: استخدم {n_slab} Ø {s_bar_d} كل متر (التباعد: {spacing:.1f} مم)")

# --- تذييل الصفحة ---
st.markdown(f"""
<hr style="border: 1px solid #FFD700;">
<div style="text-align: center; color: #FFD700; font-size: 1.2em; direction: rtl;">
    تم التصميم والبرمجة خصيصاً للمكتب الهندسي - م. بيلان مصطفى عبدالكريم © 2026
</div>
""", unsafe_allow_html=True)
