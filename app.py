import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 1. إعدادات الواجهة والختم
st.set_page_config(page_title="Pelan Structural Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #e2e8f0; }
    .header-box {
        background: linear-gradient(90deg, #1e293b, #334155);
        padding: 20px; border-radius: 15px; border: 1px solid #38bdf8;
        text-align: center; margin-bottom: 25px;
    }
    .footer-stamp {
        text-align: center; border: 2px solid #38bdf8; 
        padding: 15px; border-radius: 15px; margin-top: 50px;
        background-color: #1e293b;
    }
    </style>
    <div class="header-box">
        <h1 style='color: #38bdf8; margin:0;'>Pelan Structural Analysis Pro</h1>
        <p style='color: #94a3b8;'>نظام التصميم الإنشائي المتكامل | م. بيلان عبد الكريم</p>
    </div>
""", unsafe_allow_html=True)

# 2. القائمة الجانبية مع تحديد نوع المساند بدقة
with st.sidebar:
    st.header("⚙️ الإعدادات الهندسية")
    L = st.number_input("طول البحر L (m):", 1.0, 20.0, 5.0)
    wu = st.number_input("الحمل Wu (t/m):", 0.1, 50.0, 4.0)
    
    st.divider()
    st.subheader("📍 نمذجة المساند")
    left_support = st.selectbox("المسند الأيسر (A):", ["وثاقة (Fixed)", "مفصلي ثابت (Hinged)", "منزلق (Roller)"])
    right_support = st.selectbox("المسند الأيمن (B):", ["وثاقة (Fixed)", "مفصلي ثابت (Hinged)", "منزلق (Roller)", "ظفر (Free/Cantilever)"])
    
    st.divider()
    B = st.number_input("العرض B (cm):", 20, 100, 30)
    h = st.number_input("الارتفاع h (cm):", 20, 200, 60)
    phi_main = st.selectbox("قطر الحديد الرئيسي (mm):", [14, 16, 18, 20, 25], index=1)
    phi_sec = st.selectbox("قطر الحديد الثانوي (mm):", [10, 12, 14, 16], index=1)
    fy = 4000

# 3. منطق التحليل الإنشائي وتوزيع الحديد
d = h - 5
is_cantilever = (right_support == "ظفر (Free/Cantilever)")

# حساب العزوم بشكل تقريبي بناء على نوع الجملة
if is_cantilever:
    max_m = (wu * L**2) / 2
    iron_location = "top" # الحديد الرئيسي فوق في الكابولي
else:
    max_m = (wu * L**2) / 8
    iron_location = "bottom" # الحديد الرئيسي تحت في الجائز البسيط

def calc_n(moment, diameter):
    as_req = (abs(moment) * 10**5) / (0.87 * fy * d)
    area_bar = np.pi * (diameter/10)**2 / 4
    return max(int(np.ceil(as_req / area_bar)), 2)

n_main = calc_n(max_m, phi_main)

# 4. الرسم الهندسي
st.subheader("🏗️ المخططات الإنشائية الديناميكية")
col1, col2 = st.columns([2.5, 1])

with col1:
    fig_l, ax_l = plt.subplots(figsize=(12, 5))
    ax_l.set_aspect('equal')
    L_cm = L * 100
    cov = 5
    
    # رسم الخرسانة
    ax_l.add_patch(patches.Rectangle((0, 0), L_cm, h, color='#334155', alpha=0.3))
    
    # رسم الحديد الرئيسي (يتغير مكانه بناء على نوع الجملة)
    y_pos = (h - cov) if iron_location == "top" else cov
    ax_l.plot([cov, L_cm-cov], [y_pos, y_pos], color='#38bdf8', lw=4)
    # العكفات
    hook_dir = -15 if iron_location == "top" else 15
    ax_l.plot([cov, cov], [y_pos, y_pos + hook_dir], color='#38bdf8', lw=3)
    ax_l.plot([L_cm-cov, L_cm-cov], [y_pos, y_pos + hook_dir], color='#38bdf8', lw=3)
    ax_l.text(L_cm/2, y_pos + (10 if iron_location=="top" else -12), f"{n_main} T {phi_main} (Main {iron_location})", color='#38bdf8', ha='center', weight='bold')

    # رسم الحديد الثانوي
    y_sec = cov if iron_location == "top" else (h - cov)
    ax_l.plot([cov, L_cm-cov], [y_sec, y_sec], color='#94a3b8', lw=2)
    ax_l.text(L_cm/2, y_sec + (8 if iron_location=="bottom" else -12), f"2 T 12 (Secondary)", color='#94a3b8', ha='center')

    # رسم المساند توضيحياً
    # مسند يسار
    ax_l.plot([0, 0], [-10, h+10], color='white', lw=4 if "وثاقة" in left_support else 2)
    # مسند يمين
    if not is_cantilever:
        ax_l.plot([L_cm, L_cm], [-10, h+10], color='white', lw=4 if "وثاقة" in right_support else 2)

    # الأساور
    for x_s in range(10, int(L_cm), 20):
        ax_l.plot([x_s, x_s], [cov, h-cov], color='#ef4444', lw=1, alpha=0.4)

    ax_l.set_xlim(-50, L_cm+50)
    ax_l.set_ylim(-30, h+40)
    ax_l.axis('off')
    fig_l.patch.set_facecolor('#0f172a')
    st.pyplot(fig_l)

with col2:
    fig_c, ax_c = plt.subplots(figsize=(5, 7))
    ax_c.set_aspect('equal')
    ax_c.add_patch(patches.Rectangle((0, 0), B, h, edgecolor='white', facecolor='#1e293b', lw=3))
    ax_c.add_patch(patches.Rectangle((3, 3), B-6, h-6, edgecolor='#ef4444', facecolor='none', ls='--'))
    
    # توزيع الحديد السفلي والعلوي في المقطع
    main_y = h-6 if iron_location == "top" else 6
    sec_y = 6 if iron_location == "top" else h-6
    
    space = (B-10)/(n_main-1) if n_main > 1 else 0
    for i in range(n_main):
        ax_c.add_patch(plt.Circle((5 + i*space, main_y), phi_main/10, color='#38bdf8'))
    for i in range(2):
        ax_c.add_patch(plt.Circle((5 + i*(B-10), sec_y), 1.2/2, color='#94a3b8'))

    ax_c.axis('off')
    fig_c.patch.set_facecolor('#0f172a')
    st.pyplot(fig_c)

# 5. الختم الرسمي
st.markdown(f"""
    <div class="footer-stamp">
        <h2 style="color: #38bdf8; margin:0;">المهندس المدني بيلان مصطفى عبدالكريم</h2>
        <p style="font-size: 1.2em; margin:5px 0;">دراسات - إشراف - تعهدات</p>
        <h3 style="color: #ffffff; letter-spacing: 2px;">0998449697</h3>
        <p style="color: #64748b;">Pelan Structural Pro v22 | © 2026</p>
    </div>
""", unsafe_allow_html=True)
