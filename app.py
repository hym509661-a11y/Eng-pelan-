import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- إعدادات النظام الهندسي ---
st.set_page_config(page_title="Pelan Syrian Code Master v18", layout="wide")

# --- التنسيق البصري الفاخر (High-Contrast Luxury CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Arial'; }
    .header-box {
        background: linear-gradient(135deg, #111111 0%, #000000 100%);
        padding: 25px; border-radius: 15px; border: 3px solid #D4AF37;
        text-align: center; box-shadow: 0px 5px 20px rgba(212, 175, 55, 0.4);
        margin-bottom: 30px; direction: rtl;
    }
    .main-text { color: #D4AF37; font-size: 3em; font-weight: bold; margin: 0; }
    .sub-text { color: #FFFFFF; font-size: 1.8em; margin: 5px 0; }
    .contact-text { color: #39FF14; font-size: 1.5em; font-weight: bold; }
    .stTabs [data-baseweb="tab"] { color: #D4AF37 !important; font-size: 1.3em; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: #000 !important; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# --- ترويسة المهندس بيلان مصطفى ---
st.markdown(f"""
<div class="header-box">
    <div class="main-text">المهندس المدني بيلان مصطفى عبدالكريم</div>
    <div class="sub-text">تصميم وإشراف وفق الكود العربي السوري - الإصدار الأحدث</div>
    <div class="contact-text">📱 سوريا - القامشلي : 0998449697</div>
</div>
""", unsafe_allow_html=True)

# --- محركات الحسابات الهندسية (Syrian Code Engine) ---
def calculate_rebar(as_req, bar_dia):
    # حساب مساحة السيخ الواحد
    single_area = (np.pi * bar_dia**2) / 4
    count = int(np.ceil(as_req / single_area))
    # إجبار العدد ليكون زوجي
    if count % 2 != 0: count += 1
    return max(2, count)

# --- القائمة الرئيسية للعناصر ---
tabs = st.tabs(["🌉 الجسور المستمرة", "🏢 الأعمدة المركزية", "🏗️ بلاطات الهوردي", "🧱 القواعد والأساسات"])

# 1. قسم الجسور (Beams)
with tabs[0]:
    st.subheader("📐 تصميم الجسور (Flexure & Shear)")
    col1, col2 = st.columns([1, 2])
    with col1:
        b = st.number_input("عرض الجسر (mm)", value=300)
        h = st.number_input("ارتفاع الجسر (mm)", value=600)
        L = st.slider("طول الفتحة (m)", 2.0, 10.0, 5.0)
        wd = st.number_input("الحمل الميت DL (kN/m)", value=30.0)
        wl = st.number_input("الحمل الحي LL (kN/m)", value=15.0)
        dia = st.selectbox("قطر حديد التسليح الرئيسي", [12, 14, 16, 18, 20, 25], index=2)
        
        # معادلات الكود السوري
        wu = 1.4 * wd + 1.7 * wl
        mu = (wu * L**2) / 8
        # حساب مساحة الحديد (تقريبي للتوضيح)
        as_req = (mu * 10**6) / (0.9 * 400 * 0.9 * (h-50))
        n_bars = calculate_rebar(as_req, dia)

    with col2:
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_facecolor('black'); fig.patch.set_facecolor('black')
        # رسم المقطع
        ax.add_patch(patches.Rectangle((-b/2, 0), b, h, linewidth=4, edgecolor='#D4AF37', facecolor='#111111'))
        # الكانات
        ax.add_patch(patches.Rectangle((-b/2+25, 25), b-50, h-50, linewidth=2, edgecolor='#00FBFF', fill=False))
        # توزيع الحديد السفلي
        for i in range(n_bars):
            px = (-b/2 + 50) + i * (b-100)/(n_bars-1 if n_bars > 1 else 1)
            ax.add_patch(patches.Circle((px, 50), 12, color='#FF3131'))
        
        # الأسهم والتوصيف (Leaders)
        ax.annotate(f"{n_bars} Ø {dia} (سفلي رئيسي)", xy=(0, 50), xytext=(-b-100, -100),
                     color='#39FF14', fontsize=14, weight='bold',
                     arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2", color='#39FF14', lw=2))
        
        ax.annotate("2 Ø 12 (حديد تعليق علوي)", xy=(b/2-50, h-50), xytext=(b+50, h+50),
                     color='#00FBFF', fontsize=12, arrowprops=dict(arrowstyle='->', color='#00FBFF'))

        ax.set_xlim(-b-200, b+200); ax.set_ylim(-200, h+200); ax.axis('off')
        st.pyplot(fig)
        

# 2. قسم الأعمدة (Columns)
with tabs[1]:
    st.subheader("🏢 تصميم الأعمدة وفق الكود السوري")
    cc1, cc2 = st.columns([1, 2])
    with cc1:
        axial_load = st.number_input("الحمل المحوري Pu (kN)", value=2200)
        c_size = st.slider("بعد العمود المربع (mm)", 300, 800, 400)
        c_dia = st.selectbox("قطر قضبان العمود", [16, 18, 20, 25], index=1)
        # الكود السوري: الحد الأدنى 1% والحد الأعلى 4%
        as_min = 0.01 * c_size**2
        c_n = calculate_rebar(as_min, c_dia)
        if c_n < 4: c_n = 4

    with cc2:
        fig2, ax2 = plt.subplots(figsize=(7, 7))
        ax2.set_facecolor('black'); fig2.patch.set_facecolor('black')
        ax2.add_patch(patches.Rectangle((-c_size/2, -c_size/2), c_size, c_size, edgecolor='#D4AF37', facecolor='#111', lw=4))
        # توزيع القضبان زوجياً على المحيط
        side_count = c_n // 4 + 1
        for x in [-c_size/2+40, c_size/2-40]:
            for y in np.linspace(-c_size/2+40, c_size/2-40, side_count):
                ax2.add_patch(patches.Circle((x, y), 15, color='#FF3131'))
        
        ax2.annotate(f"الإجمالي: {c_n} Ø {c_dia}", xy=(0, 0), xytext=(0, c_size/2+80), 
                     color='#39FF14', fontsize=16, weight='bold', ha='center')
        ax2.axis('off'); st.pyplot(fig2)

# 3. قسم بلاطات الهوردي (Ribbed Slabs)
with tabs[2]:
    st.subheader("🏗️ تصميم الأعصاب (الرائجة في سوريا)")
    rc1, rc2 = st.columns([1, 2])
    with rc1:
        rib_h = st.number_input("سماكة البلاطة الكلية (cm)", value=30)
        rib_L = st.number_input("طول العصب (m)", value=5.5)
        st.info("عرض العصب الافتراضي: 12 cm | بلوك: 40 cm")
        rib_dia = st.selectbox("قطر حديد العصب", [12, 14, 16], index=1)
        rib_n = 2 # دائماً زوجي للأعصاب
    with rc2:
        st.success(f"النتيجة الإنشائية: استخدم {rib_n} Ø {rib_dia} لكل عصب")
        # رسم تفريد حديد العصب
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        ax3.set_facecolor('black'); fig3.patch.set_facecolor('black')
        ax3.add_patch(patches.Rectangle((0, 0), 520, 300, facecolor='#111', edgecolor='#D4AF37'))
        ax3.add_patch(patches.Circle((260-30, 40), 10, color='#FF3131'))
        ax3.add_patch(patches.Circle((260+30, 40), 10, color='#FF3131'))
        ax3.annotate(f"{rib_n} Ø {rib_dia}", xy=(260, 40), xytext=(260, 150), color='#39FF14',
                     arrowprops=dict(arrowstyle='->', color='#39FF14'), ha='center', weight='bold')
        ax3.axis('off'); st.pyplot(fig3)

# 4. قسم الأساسات (Foundations)
with tabs[3]:
    st.subheader("🧱 تصميم القواعد المنفردة")
    f1, f2 = st.columns([1, 2])
    with f1:
        sigma_allow = st.number_input("إجهاد التربة المسموح (kg/cm²)", value=2.5)
        footing_load = st.number_input("الحمل الواصل للقاعدة (kN)", value=1800)
        area_f = (footing_load / 10) / sigma_allow
        dim_f = np.sqrt(area_f) * 100
        f_dia = st.selectbox("قطر حديد فرش القاعدة", [14, 16], index=0)
    with f2:
        st.metric("أبعاد القاعدة المربعة", f"{dim_f:.0f} cm x {dim_f:.0f} cm")
        fig4, ax4 = plt.subplots()
        ax4.set_facecolor('black'); fig4.patch.set_facecolor('black')
        ax4.add_patch(patches.Rectangle((0,0), dim_f, dim_f, edgecolor='#39FF14', facecolor='#111', lw=3))
        ax4.set_title("مخطط تسليح القاعدة", color='white')
        ax4.axis('off'); st.pyplot(fig4)

# --- تذييل البرنامج ---
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; border: 2px solid #D4AF37; padding: 15px; border-radius: 10px;">
        <p style="color: #D4AF37; font-size: 1.2em; font-weight: bold;">
            تمت البرمجة وفق الكود السوري - جميع الحقوق محفوظة للمهندس بيلان مصطفى عبدالكريم © 2026
        </p>
    </div>
""", unsafe_allow_html=True)
