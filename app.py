import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# إعدادات هندسية متقدمة
st.set_page_config(page_title="Pelan Structural Expert v14", layout="wide")

# --- الختم الهندسي (سوريا - القامشلي) ---
def apply_syrian_stamp():
    st.sidebar.markdown(f"""
    <div style="background-color:#0f172a; padding:20px; border-radius:15px; border-right: 10px solid #ef4444; color:white; text-align:right; direction:rtl;">
        <h2 style="color:#38bdf8; margin:0;">المهندس بيلان مصطفى</h2>
        <h3 style="color:#f3f4f6; margin-top:5px;">عبدالكريم</h3>
        <p style="color:#fbbf24; font-size:1.1em; font-weight:bold; margin-top:10px;">🇸🇾 سوريا - القامشلي</p>
        <p style="color:#fbbf24; font-size:1.3em; font-weight:bold;">📱 0998449697</p>
        <hr style="border-color:#1f2937;">
        <p style="font-size:0.85em; opacity:0.8;">خبير التحليل الإنشائي وفق الكود السوري<br>AutoCAD | ETABS | SAFE | Revit</p>
    </div>
    """, unsafe_allow_html=True)

apply_syrian_stamp()

# --- محرك الحسابات التلقائي (الذكاء الإنشائي) ---
st.title("🏗️ Pelan Integrated Engineering Terminal (V14)")
st.caption("النظام المتكامل للتحليل والتصميم والتفصيل الإنشائي - مخصص للمهندس بيلان مصطفى")

tabs = st.tabs(["📊 ETABS: Analysis & Diagrams", "🏗️ SAFE: Syrian Code Design", "📐 AutoCAD: Detailing & Drafting"])

# 1. قسم الإيتابس: التحليل، القص، العزم، وردود الأفعال
with tabs[0]:
    st.header("📉 التحليل الإنشائي وردود الأفعال")
    col_in, col_diag = st.columns([1, 2])
    
    with col_in:
        st.subheader("المعطيات (Inputs)")
        L = st.number_input("طول الجسر (Span) [m]", value=6.0)
        w_d = st.number_input("الحمولات الميتة (Dead Load) [kN/m]", value=20.0)
        w_l = st.number_input("الحمولات الحية (Live Load) [kN/m]", value=10.0)
        
        st.divider()
        st.subheader("أنواع المساند (Supports)")
        support_left = st.selectbox("المسند الأيسر", ["Fixed (وثاقة)", "Pinned (مفصل)", "Roller (بسيط)"])
        support_right = st.selectbox("المسند الأيمن", ["Fixed (وثاقة)", "Pinned (مفصل)", "Roller (بسيط)"])
        
        # معادلات الكود السوري (تراكيب الأحمال)
        wu = (1.4 * w_d) + (1.7 * w_l)
        st.warning(f"الحمل التصميمي Wu = {wu:.2f} kN/m")

    with col_diag:
        # حسابات العزوم والقص وردود الأفعال بناءً على نوع المساند
        # تبسيط للحالة الأكثر شيوعاً (وثاقة من الطرفين)
        if support_left == "Fixed (وثاقة)" and support_right == "Fixed (وثاقة)":
            m_max_neg = (wu * L**2) / 12
            m_max_pos = (wu * L**2) / 24
            v_max = (wu * L) / 2
            r_total = v_max
        else: # حالة مساند بسيطة
            m_max_neg = 0
            m_max_pos = (wu * L**2) / 8
            v_max = (wu * L) / 2
            r_total = v_max

        st.subheader("مخططات القص والعزم (SFD & BMD)")
        
        # الرسم البياني
        x = np.linspace(0, L, 100)
        # دالة تقريبية للعزم بناء على النوع
        y_m = (wu * x / 2) * (L - x) - (m_max_neg) 
        y_v = wu * (L/2 - x)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        plt.subplots_adjust(hspace=0.5)
        
        # رسم العزم
        ax1.plot(x, y_m, color='yellow', label='Moment (kNm)')
        ax1.fill_between(x, y_m, color='yellow', alpha=0.2)
        ax1.set_title("Bending Moment Diagram (BMD)")
        ax1.grid(True, alpha=0.3)
        
        # رسم القص
        ax2.plot(x, y_v, color='cyan', label='Shear (kN)')
        ax2.fill_between(x, y_v, color='cyan', alpha=0.2)
        ax2.set_title("Shear Force Diagram (SFD)")
        ax2.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        # عرض ردود الأفعال
        st.success(f"Reaction R1: {r_total:.2f} kN | Reaction R2: {r_total:.2f} kN")

# 2. قسم السيف: التصميم وفق الكود السوري
with tabs[1]:
    st.header("🏗️ التصميم الإنشائي - الكود العربي السوري")
    sc1, sc2 = st.columns(2)
    
    with sc1:
        st.subheader("خصائص المواد")
        fc = st.selectbox("مقاومة الخرسانة f'c (MPa)", [20, 25, 30, 35], index=1)
        fy = st.selectbox("إجهاد الخضوع للحديد fy (MPa)", [240, 400, 420], index=1)
        b = st.number_input("عرض المقطع (b) [mm]", value=300)
        h = st.number_input("ارتفاع المقطع (h) [mm]", value=600)
    
    with sc2:
        # حساب الحديد المطلوبة (معادلات الكود السوري)
        d = h - 50 # Cover
        Rn = (m_max_pos * 10**6) / (0.9 * b * d**2)
        rho = (0.85 * fc / fy) * (1 - np.sqrt(1 - (2 * Rn / (0.85 * fc))))
        as_req = rho * b * d
        
        st.subheader("النتائج النهائية (Results)")
        st.info(f"مساحة الحديد المطلوبة: {as_req:.2f} mm²")
        
        # اختيار الأقطار تلقائياً
        bar_size = st.selectbox("اختر قطر التسليح الرئيسي [mm]", [14, 16, 18, 20, 25])
        bar_area = (np.pi * bar_size**2) / 4
        num_bars = int(np.ceil(as_req / bar_area))
        if num_bars < 2: num_bars = 2
        
        st.success(f"التسليح المقترح: {num_bars} Ø {bar_size}")

# 3. قسم الأوتوكاد: الرسم التفصيلي الدقيق مع الأسهم والتفريد
with tabs[2]:
    st.header("📐 AutoCAD Detailing (الرسم الفني والتفريد)")
    st.write("تم توليد الرسم التفصيلي بناءً على حسابات الكود السوري.")
    
    # رسم مقطع عرضي للجسر مع الأسهم والتوصيفات
    fig_cad, ax = plt.subplots(figsize=(10, 8))
    
    # 1. رسم خرسانة المقطع
    rect = patches.Rectangle((b/2*-1, 0), b, h, linewidth=3, edgecolor='white', facecolor='#262730')
    ax.add_patch(rect)
    
    # 2. رسم الكانات (Stirrups)
    stirrup = patches.Rectangle(((b/2*-1)+25, 25), b-50, h-50, linewidth=2, edgecolor='cyan', fill=False)
    ax.add_patch(stirrup)
    
    # 3. رسم الحديد السفلي (Main Bottom)
    for i in range(num_bars):
        pos_x = (b/2*-1) + 50 + (i * (b-100)/(num_bars-1 if num_bars>1 else 1))
        circle = patches.Circle((pos_x, 50), 8, color='red')
        ax.add_patch(circle)
        if i == 0: # سهم وتوصيف للحديد السفلي
            ax.annotate(f"{num_bars} Ø {bar_size} (Bottom)", xy=(pos_x, 50), xytext=(pos_x-150, -100),
                         arrowprops=dict(facecolor='white', shrink=0.05, width=1))

    # 4. رسم حديد التعليق (Hangers)
    ax.add_patch(patches.Circle(((b/2*-1)+50, h-50), 6, color='orange'))
    ax.add_patch(patches.Circle(((b/2)-50, h-50), 6, color='orange'))
    ax.annotate("2 Ø 12 (Hangers)", xy=((b/2)-50, h-50), xytext=(b/2+100, h+50),
                 arrowprops=dict(facecolor='white', shrink=0.05, width=1))

    # 5. رسم حديد البرندات (Side Bars)
    if h > 600:
        ax.add_patch(patches.Circle(((b/2*-1)+40, h/2), 5, color='green'))
        ax.add_patch(patches.Circle(((b/2)-40, h/2), 5, color='green'))
        ax.annotate("2 Ø 10 (Side Bars)", xy=((b/2)-40, h/2), xytext=(b/2+100, h/2),
                     arrowprops=dict(facecolor='white', shrink=0.05, width=1))

    # إعدادات الرسم
    ax.set_xlim(-500, 500)
    ax.set_ylim(-200, 800)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#0e1117')
    fig_cad.patch.set_facecolor('#0e1117')
    
    st.pyplot(fig_cad)
    
    

    # تصدير التقرير النهائي
    st.divider()
    st.subheader("📋 ملخص جدول الكميات (BBS)")
    final_data = {
        "نوع الحديد": ["تسليح سفلي رئيسي", "حديد تعليق علوي", "كانات مقاومة قص", "حديد برندات"],
        "العدد": [num_bars, 2, f"{int(L/0.15)}", 2 if h > 600 else 0],
        "القطر (mm)": [bar_size, 12, 10, 10],
        "التوصيف": [f"{num_bars} Ø {bar_size}", "2 Ø 12", "Ø 10 @ 150mm", "2 Ø 10"],
        "الكود": ["Syrian-Main", "Syrian-Hanger", "Syrian-Stirrup", "Syrian-Side"]
    }
    st.table(pd.DataFrame(final_data))

# --- التذييل الرسمي ---
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; border: 2px solid #38bdf8; padding: 20px; border-radius: 10px;">
        <h2 style="color:#38bdf8; margin:0;">المهندس بيلان مصطفى عبدالكريم</h2>
        <p style="font-size:1.2em;">خبير الإدارة الهندسية والتحليل الإنشائي وفق الكود العربي السوري</p>
        <p style="font-weight:bold; color:#fbbf24; font-size:1.5em;">📱 0998449697 | 📍 سوريا - القامشلي</p>
    </div>
""", unsafe_allow_html=True)
