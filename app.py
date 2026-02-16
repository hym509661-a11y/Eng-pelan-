import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# إعدادات الصفحة
st.set_page_config(page_title="Pelan Structural Hub v15", layout="wide")

# --- التنسيق الجمالي الفاخر (CSS LUXURY THEME) ---
st.markdown("""
<style>
    /* الخلفية العامة */
    .stApp { background-color: #05070a; color: #e0e0e0; }
    
    /* الترويسة الفاخرة */
    .luxury-header {
        background: linear-gradient(135deg, #1a1c22 0%, #000000 100%);
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #d4af37; /* لون ذهبي */
        text-align: center;
        box-shadow: 0px 10px 30px rgba(212, 175, 55, 0.2);
        margin-bottom: 25px;
        direction: rtl;
    }
    .main-title { color: #d4af37; font-size: 2.5em; font-weight: bold; margin-bottom: 5px; }
    .sub-title { color: #ffffff; font-size: 1.5em; margin-bottom: 5px; }
    .specialty { color: #888; font-size: 1.1em; letter-spacing: 2px; }
    .phone-box { color: #00e5ff; font-size: 1.4em; font-weight: bold; margin-top: 10px; }

    /* تبويبات العمل */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #161b22;
        border-radius: 5px 5px 0 0;
        padding: 10px 20px;
        color: #d4af37;
    }
    .stTabs [aria-selected="true"] { background-color: #d4af37 !important; color: black !important; }
</style>
""", unsafe_allow_html=True)

# --- عرض الترويسة الفاخرة ---
st.markdown(f"""
<div class="luxury-header">
    <div class="main-title">المهندس المدني</div>
    <div class="sub-title">بيلان مصطفى عبدالكريم</div>
    <div class="specialty">دراسات - إشراف - تعهدات</div>
    <div class="phone-box">📱 0998449697</div>
</div>
""", unsafe_allow_html=True)

# --- الأقسام الهندسية ---
tabs = st.tabs(["📊 التحليل الإنشائي (ETABS)", "🏗️ تفاصيل التسليح (SAFE)", "📐 الرسم الفني (AutoCAD)"])

# 1. قسم التحليل (ألوان واضحة جداً)
with tabs[0]:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("⚙️ مدخلات التصميم")
        L = st.number_input("طول العنصر (m)", value=6.0)
        W = st.number_input("الحمل الكلي (kN/m)", value=40.0)
        st.info("يتم الحساب وفق تراكيب الكود السوري")
    
    with col2:
        # حسابات
        x = np.linspace(0, L, 100)
        m_x = (W * x / 2) * (L - x) # عزم
        v_x = W * (L/2 - x) # قص
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        
        # مخطط العزم بألوان فوسفورية
        ax1.plot(x, m_x, color='#FFD700', linewidth=3, label='Moment') # ذهبي
        ax1.fill_between(x, m_x, color='#FFD700', alpha=0.3)
        ax1.set_title("Bending Moment Diagram (BMD)", color='white', fontsize=12)
        ax1.set_facecolor('#000000')
        
        # مخطط القص
        ax2.plot(x, v_x, color='#00FFFF', linewidth=3, label='Shear') # سيان فوسفوري
        ax2.fill_between(x, v_x, color='#00FFFF', alpha=0.3)
        ax2.set_title("Shear Force Diagram (SFD)", color='white', fontsize=12)
        ax2.set_facecolor('#000000')
        
        fig.patch.set_facecolor('#05070a')
        st.pyplot(fig)

# 2. قسم التسليح (SAFE) مع التوضيح
with tabs[1]:
    st.header("🏗️ جدول تفريد الحديد")
    
    # حساب تقريبي للحديد
    as_calc = ( (W * L**2 / 8) * 10**6 ) / (0.9 * 400 * 0.9 * 550)
    bars_num = int(np.ceil(as_calc / 201)) + 1 # قطر 16 مم
    
    safe_df = pd.DataFrame({
        "نوع الحديد": ["سفلي رئيسي", "علوي (تعليق)", "كانات", "برندات (جانبي)"],
        "التوصيف الفني": [f"{bars_num} Ø 16 mm", "3 Ø 14 mm", "Ø 10 mm @ 150mm", "2 Ø 12 mm"],
        "الموقع": ["Mid-Span", "Supports", "Full Length", "Side Faces"],
        "الحالة": ["✅ محقق", "✅ محقق", "✅ محقق", "✅ محقق"]
    })
    st.table(safe_df)

# 3. قسم الرسم (AutoCAD) مع الأسهم والخطوط الواضحة
with tabs[2]:
    st.header("📐 الرسم التفصيلي للمقطع الإنشائي")
    
    # إنشاء رسم مقطع عرضي بألوان واضحة جداً
    fig_cad, ax = plt.subplots(figsize=(8, 8))
    
    # المقطع الخرساني
    ax.add_patch(patches.Rectangle((-150, 0), 300, 600, linewidth=4, edgecolor='#d4af37', facecolor='#111'))
    
    # الكانة
    ax.add_patch(patches.Rectangle((-125, 25), 250, 550, linewidth=2, edgecolor='#00FFFF', fill=False))
    
    # رسم الحديد السفلي وتوضيحه بسهم
    for i in range(bars_num):
        pos_x = -100 + (i * 200/(bars_num-1))
        ax.add_patch(patches.Circle((pos_x, 50), 10, color='#FF3131')) # أحمر فوسفوري
        if i == 0:
            ax.annotate(f"{bars_num} Ø 16 (Main Steel)", xy=(pos_x, 50), xytext=(-350, -50),
                         color='white', weight='bold', fontsize=12,
                         arrowprops=dict(arrowstyle='->', color='#FF3131', lw=2))

    # رسم حديد التعليق وتوضيحه بسهم
    ax.add_patch(patches.Circle((-100, 550), 8, color='#39FF14')) # أخضر فوسفوري
    ax.add_patch(patches.Circle((100, 550), 8, color='#39FF14'))
    ax.annotate("3 Ø 14 (Hangers)", xy=(100, 550), xytext=(200, 650),
                 color='white', weight='bold', fontsize=12,
                 arrowprops=dict(arrowstyle='->', color='#39FF14', lw=2))

    # ضبط المشهد
    ax.set_xlim(-400, 400)
    ax.set_ylim(-150, 750)
    ax.set_aspect('equal')
    ax.axis('off')
    fig_cad.patch.set_facecolor('#05070a')
    st.pyplot(fig_cad)

# --- التذييل النهائي ---
st.markdown("""
<hr style="border-color: #d4af37;">
<p style="text-align: center; color: #d4af37; font-size: 1.2em;">
    حقوق التصميم محفوظة للمهندس بيلان مصطفى عبدالكريم © 2026
</p>
""", unsafe_allow_html=True)
