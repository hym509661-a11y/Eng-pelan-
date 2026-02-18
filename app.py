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
        <p style='color: #94a3b8;'>نظام التفاصيل الإنشائية الذكي | م. بيلان عبد الكريم</p>
    </div>
""", unsafe_allow_html=True)

# 2. المدخلات الهندسية
with st.sidebar:
    st.header("⚙️ المعطيات التصميمية")
    L = st.number_input("طول البحر L (m):", 1.0, 20.0, 5.0)
    wu = st.number_input("الحمل Wu (t/m):", 0.1, 50.0, 4.0)
    st.divider()
    B = st.number_input("العرض B (cm):", 20, 100, 30)
    h = st.number_input("الارتفاع h (cm):", 20, 200, 60)
    phi_main = st.selectbox("قطر الحديد الرئيسي (mm):", [14, 16, 18, 20, 25], index=1)
    phi_sec = st.selectbox("قطر الحديد الإضافي/العلوي (mm):", [10, 12, 14, 16], index=1)
    stirrup_phi = 8

# 3. المحرك الحسابي (Structural Engine)
fy = 4000
d = h - 5 # العمق الفعال
max_m_pos = (wu * L**2) / 8 # العزم الموجب (بسيط)
max_m_neg = (wu * L**2) / 12 # العزم السالب (افتراضي للوثاقة)

# حساب عدد الأسياخ
def calc_as(moment, diameter):
    as_req = (moment * 10**5) / (0.87 * fy * d)
    area_bar = np.pi * (diameter/10)**2 / 4
    return max(int(np.ceil(as_req / area_bar)), 2)

n_main = calc_as(max_m_pos, phi_main) # سفلي
n_top = 2 # علوي علاقات أساور
n_extra = 2 if L > 4 else 0 # حديد إضافي عند المساند

# 4. الرسم الهندسي الديناميكي
st.subheader("🏗️ المخططات التنفيذية وتفريد الحديد")
tab1, tab2 = st.tabs(["المقطع الطولي والجانبي", "جدول الكميات"])

with tab1:
    col1, col2 = st.columns([2.5, 1])
    
    with col1:
        # --- رسم المقطع الطولي (Longitudinal Section) ---
        fig_l, ax_l = plt.subplots(figsize=(12, 5))
        ax_l.set_aspect('equal')
        L_cm = L * 100
        cov = 5
        
        # رسم جسم البيتون
        ax_l.add_patch(patches.Rectangle((0, 0), L_cm, h, color='#334155', alpha=0.3))
        
        # 1. الحديد السفلي الرئيسي (Main Bottom)
        ax_l.plot([cov, L_cm-cov], [cov, cov], color='#38bdf8', lw=3) # السيخ
        ax_l.plot([cov, cov], [cov, cov+10], color='#38bdf8', lw=3) # عكفة يسار
        ax_l.plot([L_cm-cov, L_cm-cov], [cov, cov+10], color='#38bdf8', lw=3) # عكفة يمين
        ax_l.text(L_cm/2, cov-8, f"{n_main} T {phi_main} (Main Bottom)", color='#38bdf8', ha='center', fontsize=9)

        # 2. الحديد العلوي (Top Support/Stirrup Hangers)
        ax_l.plot([cov, L_cm-cov], [h-cov, h-cov], color='#94a3b8', lw=2)
        ax_l.text(L_cm/2, h-cov+5, f"{n_top} T {phi_sec} (Top)", color='#94a3b8', ha='center', fontsize=9)

        # 3. الحديد الإضافي (Extra Bars at Supports)
        if n_extra > 0:
            ax_l.plot([cov, L_cm*0.2], [h-cov-4, h-cov-4], color='#fbbf24', lw=2.5)
            ax_l.text(L_cm*0.1, h-cov-12, f"{n_extra}T{phi_sec} Extra", color='#fbbf24', fontsize=8)

        # 4. الأساور (Stirrups)
        s_spacing = 15 # كل 15 سم
        for x_s in range(10, int(L_cm), s_spacing):
            ax_l.plot([x_s, x_s], [cov, h-cov], color='#ef4444', lw=1, alpha=0.5)
        ax_l.text(L_cm*0.8, 15, f"Stirrups T{stirrup_phi}@{s_spacing}cm", color='#ef4444', fontsize=8, rotation=90)

        ax_l.set_xlim(-20, L_cm+20)
        ax_l.set_ylim(-20, h+30)
        ax_l.axis('off')
        fig_l.patch.set_facecolor('#0f172a')
        st.pyplot(fig_l)

    with col2:
        # --- رسم المقطع العرضي (Cross Section) ---
        fig_c, ax_c = plt.subplots(figsize=(5, 7))
        ax_c.set_aspect('equal')
        
        # الخرسانة والأساور
        ax_c.add_patch(patches.Rectangle((0, 0), B, h, edgecolor='#e2e8f0', facecolor='#1e293b', lw=3))
        ax_c.add_patch(patches.Rectangle((3, 3), B-6, h-6, edgecolor='#ef4444', facecolor='none', ls='--', lw=1.5))
        
        # رسم الحديد السفلي
        space_b = (B-10)/(n_main-1) if n_main > 1 else 0
        for i in range(n_main):
            ax_c.add_patch(plt.Circle((5 + i*space_b, 6), phi_main/10, color='#38bdf8'))
            
        # رسم الحديد العلوي
        space_t = (B-10)/(n_top-1)
        for i in range(n_top):
            ax_c.add_patch(plt.Circle((5 + i*space_t, h-6), phi_sec/10, color='#94a3b8'))
            
        ax_c.text(B/2, -8, f"SECTION B={B}cm, H={h}cm", color='white', ha='center', fontsize=10)
        ax_c.set_xlim(-10, B+10)
        ax_c.set_ylim(-15, h+15)
        ax_c.axis('off')
        fig_c.patch.set_facecolor('#0f172a')
        st.pyplot(fig_c)

with tab2:
    st.subheader("📊 جدول تقدير الكميات")
    total_conc = (B/100) * (h/100) * L
    st.write(f"✅ حجم الخرسانة: `{total_conc:.2f} m³`")
    st.write(f"✅ التسليح الرئيسي: `{n_main} T {phi_main}`")
    st.write(f"✅ التسليح العلوي: `{n_top} T {phi_sec}`")
    st.write(f"✅ الأساور: `T {stirrup_phi}` كل `{s_spacing} سم`")

# 5. الختم الرسمي المحدث
st.markdown(f"""
    <div class="footer-stamp">
        <h2 style="color: #38bdf8; margin:0;">المهندس المدني بيلان مصطفى عبدالكريم</h2>
        <p style="font-size: 1.2em; margin:5px 0;">دراسات - إشراف - تعهدات</p>
        <h3 style="color: #ffffff; letter-spacing: 2px;">0998449697</h3>
        <p style="color: #64748b; font-size: 0.8em;">Pelan Structural Pro v22 | تم التصميم بواسطة المهندس بيلان © 2026</p>
    </div>
""", unsafe_allow_html=True)
